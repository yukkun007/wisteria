# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from dotenv import load_dotenv
from kbot.log import Log
from linebot.models import ButtonsTemplate,\
    ConfirmTemplate,\
    MessageTemplateAction,\
    PostbackTemplateAction,\
    URITemplateAction


class KBot(object):

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.__load_dotenv()

    def __load_dotenv(self):
        dotenv_path = os.path.join(self.root_dir, '.env')
        if os.path.exists(dotenv_path):
            Log.info('>>>>>>>>>>>>>> find .env : {0}'.format(dotenv_path))
            load_dotenv(dotenv_path)
        else:
            Log.info('>>>>>>>>>>>>>> not find .env : {0}'.format(dotenv_path))

    def get_kbot_command_menu(self):
        buttons_template = ButtonsTemplate(
            title='kbotコマンドメニュー',
            text='直接メッセージを入れても反応します!',
            actions=[
                # URITemplateAction(
                # label='図書館のサイトへ',
                # uri='https://www.lib.nerima.tokyo.jp/opw/\
                #                 OPW/OPWLOGINTIME.CSP?HPFLG=1&NEXT=OPWUSER\
                #                 INFO&DB=LIB'),
                PostbackTemplateAction(
                    label='借りてる本をﾁｪｯｸ',
                    data='check_rental',
                    text='図書館'),
                PostbackTemplateAction(
                    label='延滞本をﾁｪｯｸ',
                    data='check_expired',
                    text='延滞'),
                PostbackTemplateAction(
                    label='X日で延滞の本をﾁｪｯｸ',
                    data='check_expire',
                    text='2日で延滞'),
                PostbackTemplateAction(
                    label='反応する文字を見る',
                    data='show_reply_string',
                    text='文字')
            ]
        )
        return buttons_template

    def is_check_reserve_command(self, text):
        for key in ['予約？']:
            if key in text:
                return True
        return False

    def is_rental_check_command(self, text):
        for key in ['図書館']:
            if key in text:
                return True
        return False

    def is_expired_check_command(self, text):
        for key in ['延滞']:
            if key in text:
                return True
        return False

    def is_expire_check_command(self, text):
        for key in ['日で延滞']:
            if key in text:
                return True
        return False

    def is_reply_string_show_command(self, text):
        for key in ['文字']:
            if key in text:
                return True
        return False

    def is_search_book_command(self, text):
        if '本？' in text:
            return True
        elif '著？' in text:
            return True
        return False

    def get_xdays(self, text):
        default = 2
        index = text.find('日で延滞')
        num_str = text[index - 1:index + 4]
        num_str = num_str.replace('日で延滞', '')
        try:
            return int(num_str)
        except ValueError:
            return default

    def get_reply_string(self):
        message = '''次の言葉に反応します。

──────
図書館
──────
■貸出状況ﾁｪｯｸ
　◎図書館
■期限切れの本ﾁｪｯｸ
　◎延滞
■期限間近の本ﾁｪｯｸ
　◎2日で延滞 (X日で延滞)
■予約状況ﾁｪｯｸ
　◎予約？

──────
本
──────
■ﾀｲﾄﾙで本を探す
　◎本？坊っちゃん
■著者名で本を探す
　◎著？夏目漱石
        '''
        return message

    def get_confirm_template_sample(self):
        confirm_template = ConfirmTemplate(
            text='Do it?', actions=[
                MessageTemplateAction(label='Yes',
                                      text='Yes!'),
                MessageTemplateAction(label='No',
                                      text='No!'),
            ]
        )
        return confirm_template

    def get_buttons_template_sample(self):
        buttons_template = ButtonsTemplate(
            title='My buttons sample',
            text='Hello, my buttons',
            actions=[
                URITemplateAction(
                    label='Go to line.me',
                    uri='https://line.me'),
                PostbackTemplateAction(label='ping',
                                       data='ping'),
                PostbackTemplateAction(
                    label='ping with text',
                    data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice',
                                      text='米')
            ]
        )
        return buttons_template
