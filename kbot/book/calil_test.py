# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.kbot import KBot
from kbot.book.calil import CalilService
from kbot.book.common import BookSearchQuery


class TestCalilService(object):

    def test_calil_service(self):
        KBot('wisteria')
        query = BookSearchQuery()
        query.set('isbn', '9784532280208')
        calil_book = CalilService.get_one_book(query)
        print(calil_book.get_text_message())
