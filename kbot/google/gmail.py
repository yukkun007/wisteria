#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
from datetime import datetime, timezone, timedelta
from kbot.google.gmail_api import GmailApi


class GMail(object):
    def __init__(self):
        self.storage_path = "/tmp/st_test.txt"
        self.secret_path = "/tmp/sc_test.txt"

        st = open(self.storage_path, "w")
        storage = os.environ["GMAIL_AUTH_STORAGE"]
        st.write(storage)
        st.close()

        # sc = open(self.secret_path, 'w')
        # secret = os.environ['GMAIL_CLIENT_SECRET']
        # sc.write(secret)
        # sc.close()
        # secret_file = open(self.secret_path)
        auth_info = ""  # json.load(secret_file)

        # 初回実行時は認証が求められます
        self.api = GmailApi(auth_info, self.storage_path)

    def __send_message(self, to, subject, message):
        user = "me"
        message = self.api.createMessage(user, to, subject, message)
        self.api.sendMessage(user, message)

    def send_message_multi(self, tos, subject, message):
        for to in tos:
            self.__send_message(to, subject, message)

    def get_messages(self, query):
        # test = self.api.getMailList("me", "from:info@keishicho.metro.tokyo.jp is:unread")
        test = self.api.getMailList("me", query)
        if test.get("messages") is None:
            print("no messages.")
            return []

        send_messages = []
        for message in test["messages"]:
            id = message.get("id")
            print("message.id=" + id)
            message = self.api.getMailMessage("me", id)
            subject = self.api.getSubject(message)
            print("subject=" + subject)
            date = message.get("Date")
            formatted_date = self._get_formatted_date(date)
            print("Date=" + formatted_date)
            body = self.api.getBody(message)
            print("body=" + body)

            send_message = """􀀵めーるけいしちょう 転送

 {0}
 {1}
---------------------------

{2}""".format(
                subject, formatted_date, body
            )
            send_messages.append(send_message)

        return send_messages

    def _get_formatted_date(self, date):
        split_date = date.split()

        # 日時情報を生成（タイムゾーン情報なし）
        ts = ""
        for s in split_date[1:5]:
            ts += s
        # 取得した日付情報から naive な datetime オブジェクトを生成
        d = datetime.strptime(ts, "%d%b%Y%H:%M:%S")

        # タイムゾーン情報を文字列から取得
        tzs = split_date[5]
        if tzs[0] == "+":
            sign = 1
        else:
            sign = -1
        h = int(tzs[1:3])
        m = int(tzs[3:])

        # タイムゾーン情報を生成
        TZ = timezone(timedelta(hours=(sign * h), minutes=(sign * m)))
        # 生成済みの naive な datetime とタイムゾーン情報から aware な datetime オブジェクトを生成
        dt = datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, 0, tzinfo=TZ)

        return dt.strftime("%Y/%m/%d %H:%M:%S")
