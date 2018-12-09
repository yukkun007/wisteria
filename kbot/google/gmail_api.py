#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import email
import webbrowser
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from googleapiclient.errors import HttpError

# from oauth2client.tools import run
import httplib2


from email.mime.text import MIMEText

auth_url = "https://accounts.google.com/o/oauth2/auth?"

response_setting = {"scope": "https://mail.google.com/", "response_type": "code"}


# https://qiita.com/woody-kawagoe/items/4de3f2f0902784d34ca0
# https://github.com/TM-KNYM/How2UseGmailApiByPython/blob/master/gmailapi.py
class GmailApi:
    def reconnect(self):
        """サーバーにアクセスして認証をもう一度行う
        """
        try:
            self.service = GmailServiceFactory().createService(self.auth_info)
        except HttpError as error:
            print("An error occurred:s" % error)
            pass

    def sendMessage(self, user, message):
        """メールを送信します。messageの作り方はcreateMesage関数を参照

            Keyword arguments:
            user -- meを指定する。
            message -- createMessageで生成したオブジェクトを渡す必要があります

            Returns: None
        """
        try:
            message = self.service.users().messages().send(userId=user, body=message).execute()
            return message
        except HttpError as error:
            print("An error occurred:s" % error)

    def getMailList(self, user, qu):
        """ メールの情報をリストで取得します
          quの内容でフィルタリングする事が出来ます

           Keyword arguments:
           user -- me又はgoogleDevloperに登録されたアドレスを指定します。
           qu -- queryを設定します
                 例えばexample@gmail.comから送られてきた未読のメールの一覧を取得するには以下のように指定すればよい
                "from: example@gmail.com is:unread"
           Returns: メール情報の一覧　idとThreadIdをKeyとした辞書型のリストになる
             "messages": [
                  {
                   "id": "nnnnnnnnnnnn",
                   "threadId": "zzzzzzzzzzz"
                  },
                  {
                   "id": "aaaaaa",
                   "threadId": "bbbbbb"
                  },,,,
              }
        """
        try:
            return self.service.users().messages().list(userId=user, q=qu).execute()
        except HttpError as error:
            print("An error occurred:s" % error)
            self.reconnect()

    def getMailMessage(self, user, i):
        """指定したメールのIDからメールの内容を取得します。

                Keyword arguments:
                user -- meを指定する。
                i -- メールのId getMailList()等を使用して取得したIdを使用する

                Returns: メールの内容を辞書型で取得する
                詳細は以下
                http://developers.google.com/apis-explorer/#p/gmail/v1/gmail.users.messages.get
        """
        try:
            message = self.service.users().messages().get(userId=user, id=i, format="raw").execute()
            msg_str = base64.urlsafe_b64decode(message["raw"]).decode("utf-8")
            return email.message_from_string(msg_str)
        except HttpError as error:
            print("An error occurred:s" % error)
            self.reconnect()

    def getSubject(self, message):
        subjects = email.header.decode_header(message.get("Subject"))
        for subject in subjects:
            if isinstance(subject[0], bytes) and subject[1] is not None:
                return subject[0].decode(subject[1])
            else:
                return subject[0].decode()

    def getBody(self, message):
        if message.is_multipart():
            for payload in message.get_payload():
                if payload.get_content_type() == "text/plain":
                    charset = message.get_param("charset")
                    if charset is None:
                        return payload.get_payload(decode=True).decode("iso-2022-jp")
                    else:
                        return payload.get_payload(decode=True).decode(charset)
        else:
            charset = message.get_param("charset")
            return message.get_payload(decode=True).decode(charset)

    def doMailAsRead(self, user, i):
        """指定したメールのIDを既読にします
            Keyword arguments:
            user -- meを指定する。
            i -- メールのId getMailList()等を使用して取得したIdを使用する

            Returns:　なし
        """
        query = {"removeLabelIds": ["UNREAD"]}
        self.service.users().messages().modify(userId=user, id=i, body=query).execute()

    def createMessage(self, sender, to, subject, message_text):
        """sendMessageで送信するメールを生成します
            Keyword arguments:
            sender -- meを指定する。
            to -- メールのId getMailList()等を使用して取得したIdを使用する
            subject -- 件名
            message_text --　メールの内容

            Returns:　なし
        """
        message = MIMEText(message_text, "html", "utf-8")
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject
        byte_msg = message.as_string().encode(encoding="UTF-8")
        byte_msg_b64encoded = base64.urlsafe_b64encode(byte_msg)
        str_msg_b64encoded = byte_msg_b64encoded.decode(encoding="UTF-8")
        return {"raw": str_msg_b64encoded}

    def expMailContents(self, user, i, key):
        try:
            content = self.getMailContent(user, i)
            return ([header for header in content["payload"]["headers"] if header["name"] == key])[
                0
            ]["value"]
        except HttpError as error:
            print("An error occurred:s" % error)
            self.reconnect()

    def getMailFrom(self, user, i):
        self.__getMail(user, i, "From")

    def getMailSubject(self, user, i):
        self.__getMail(user, i, "Subject")

    def __getMail(self, user, i, key):
        try:
            return self.expMailContents(user, i, key)
        except HttpError as error:
            print("An error occurred:s" % error)
            self.reconnect()

    def __init__(self, auth_info, storage_path):
        self.auth_info = auth_info
        self.storage_path = storage_path
        self.service = GmailServiceFactory().createService(self.auth_info, self.storage_path)


class GmailServiceFactory:
    def createService(self, auth_info, storage_path):
        STORAGE = Storage(storage_path)
        credent = STORAGE.get()

        if credent is None or credent.invalid:
            info = auth_info["installed"]
            flow = OAuth2WebServerFlow(
                info["client_id"],
                info["client_secret"],
                response_setting["scope"],
                info["redirect_uris"][0],
            )
            auth_url = flow.step1_get_authorize_url()
            # ブラウザを開いて認証する
            webbrowser.open(auth_url)
            code = input("input code : ")
            credent = flow.step2_exchange(code)
            STORAGE.put(credent)
        http = httplib2.Http()
        http = credent.authorize(http)

        gmail_service = build("gmail", "v1", http=http)
        return gmail_service
