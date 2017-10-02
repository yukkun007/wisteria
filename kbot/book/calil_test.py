# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot import LineBotApi
from kbot.kbot import KBot
from kbot.book.book import Book
from kbot.book.calil import Calil
from kbot.line import Line

class TestCalil(object):

    def test_calil(self):
        KBOT         = KBot('wisteria')
        line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
        line         = Line(line_bot_api)
        line_tos     = [os.environ['LINE_SEND_GROUP_ID']]

        calil   = Calil()
        isbn    = '9784532280208'
        book    = calil.get_book(isbn)
        message = Book.get_book_info_text_message(book)
        line.my_push_template_message(message, line_tos)

