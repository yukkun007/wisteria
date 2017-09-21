#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.library.library import Library
from linebot.models import TemplateSendMessage,\
                           TextSendMessage,\
                           VideoSendMessage

class Line(object):

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api

    def my_push_text_message(self, message, tos):
        for to in tos:
            self.line_bot_api.push_message(
                to,
                TextSendMessage(text=message)
            )

    def my_push_template_message(self, template, tos):
        template_message = TemplateSendMessage(
            alt_text='alt text',
            template=template)
        for to in tos:
            self.line_bot_api.push_message(
                to,
                template_message
            )

    def my_reply_text_message(self, message, event):
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )

    def my_reply_template_message(self, template, event):
        template_message = TemplateSendMessage(
            alt_text='alt text',
            template=template)
        self.line_bot_api.reply_message(
            event.reply_token,
            template_message
        )

