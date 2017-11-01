# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot import LineBotApi
from kbot.kbot import KBot
from kbot.book.rakuten_books import RakutenBooksService, BookSearchQuery
from kbot.line import Line

class TestBook(object):


    def test_search_book(self):
        KBOT         = KBot('wisteria')
        line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
        line         = Line(line_bot_api)
        line_tos     = [os.environ['LINE_SEND_GROUP_ID_DEBUG']]

        query = BookSearchQuery()
        query.set('title', 'カンブリア')
        books   = RakutenBooksService.search_books(query)
        message = books.slice(0, 5).get_books_select_line_carousel_mseeage()
        line.my_push_message(message, line_tos)

