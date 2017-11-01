#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from kbot.kbot import KBot
from kbot.line import Line

from linebot import LineBotApi
from linebot.models import ButtonsTemplate,\
    URITemplateAction


class TestLine:

    def test_1(self):
        KBot('wisteria')

        line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
        line = Line(line_bot_api)
        line.my_push_message('これはテストです。', [os.environ['LINE_SEND_ID']])

    def test_2(self):
        KBot('wisteria')

        line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
        line = Line(line_bot_api)
        buttons_template = ButtonsTemplate(
            title='test',
            text='this is test.',
            actions=[
                URITemplateAction(
                    label='YouTubeへ',
                    uri='https://www.youtube.com/')
            ]
        )
        line.my_push_message(buttons_template, [os.environ['LINE_SEND_ID']])
