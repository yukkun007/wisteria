# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from dotenv import load_dotenv
from kbot.log import Log
from linebot.models import ButtonsTemplate,\
                           ConfirmTemplate,\
                           MessageTemplateAction,\
                           PostbackEvent,\
                           PostbackTemplateAction,\
                           URITemplateAction

class KBot(object):

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.__load_dotenv()

    def __load_dotenv(self):
        dotenv_path = os.path.join(self.root_dir, '.env')
        if os.path.exists(dotenv_path):
            print('>>>>>>>>>>>>>> find .env : {0}'.format(dotenv_path))
            load_dotenv(dotenv_path)
        else:
            print('>>>>>>>>>>>>>> not find .env : {0}'.format(dotenv_path))


    def get_kbot_command_menu(self):
        buttons_template = ButtonsTemplate(
            title   = 'kbotコマンドメニュー',
            text    = '直接メッセージを入れても反応します。',
            actions = [
                #URITemplateAction(
                    # label='図書館のサイトへ',
                    # uri='https://www.lib.nerima.tokyo.jp/opw/\
                    #                 OPW/OPWLOGINTIME.CSP?HPFLG=1&NEXT=OPWUSER\
                    #                 INFO&DB=LIB'),
                PostbackTemplateAction(
                    label = '借りてる本をﾁｪｯｸ',
                    data  = 'check_rental',
                    text  = '図書館'),
                PostbackTemplateAction(
                    label = '期限切れ本をﾁｪｯｸ',
                    data  = 'check_expired',
                    text  = '期限切れ'),
                PostbackTemplateAction(
                    label = 'X日で期限切れの本をﾁｪｯｸ',
                    data  = 'check_expire',
                    text  = '2日'),
                PostbackTemplateAction(
                    label = '反応する文字を見る',
                    data  = 'show_reply_string',
                    text  = '文字')
            ]
        )
        return buttons_template

    def is_rental_check_command(self, text):
        for key in ['図書館', '借り']:
            if key in text:
                return True
        return False

    def is_expired_check_command(self, text):
        for key in ['期限切れ', '延滞']:
            if key in text:
                return True
        return False

    def is_expire_check_command(self, text):
        if '日' in text:
            return True
        return False

    def is_reply_string_show_command(self, text):
        for key in ['文字', 'moji']:
            if key in text:
                return True
        return False

    def is_search_book_command(self, text):
        if '本？' in text:
            return True
        return False

    def get_xdays(self, text):
        default = 2
        num_str = text.replace('日', '')
        try:
            return int(num_str)
        except ValueError:
            return default

    def get_reply_string(self):
        message = '''
次の言葉に反応します。

*借りてる本
　→図書館/本
*期限切れ
　→期限切れ/延滞
*期限まで後少し
　→2日/5日
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

