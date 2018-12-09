#!/usr/bin/python
# -*- coding: utf-8 -*-

from linebot.models import TemplateSendMessage, TextSendMessage


class Line(object):
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api

    def __is_text_message(self, input_parameter):
        if isinstance(input_parameter, str):
            return True
        return False

    def __make_message(self, input_parameter):
        if self.__is_text_message(input_parameter):
            add_string = ""
            if len(input_parameter) > 1900:
                add_string = "....."
            message = input_parameter[:1900] + add_string
            return TextSendMessage(text=message)
        else:
            return TemplateSendMessage(alt_text=".....", template=input_parameter)

    def my_push_message(self, input_parameter, tos):
        for to in tos:
            self.line_bot_api.push_message(to, self.__make_message(input_parameter))

    def my_reply_message(self, input_parameter, event):
        if event is not None:
            self.line_bot_api.reply_message(event.reply_token, self.__make_message(input_parameter))
        else:
            # debug
            print(self.__make_message(input_parameter))
