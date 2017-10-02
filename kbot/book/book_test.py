# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot import LineBotApi
from kbot.kbot import KBot
from kbot.book.rakuten_books import RakutenBooks
from kbot.book.book import Book
from kbot.line import Line

class TestBook(object):


    def test_search_book(self):
        KBOT         = KBot('wisteria')
        line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
        line         = Line(line_bot_api)
        line_tos     = [os.environ['LINE_SEND_GROUP_ID']]

        query          = {}
        query['title'] = 'カンブリア'
        rakuten        = RakutenBooks()
        books          = rakuten.search_books(query)
        message        = Book.get_books_select_line_carousel_mseeage(books)
        line.my_push_template_message(message, line_tos)

