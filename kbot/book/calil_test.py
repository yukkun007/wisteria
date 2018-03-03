# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import json
from kbot.kbot import KBot
from kbot.book.calil import CalilService
from kbot.book.common import BookSearchQuery


class TestCalilService(object):

    def setup(self):
        KBot('wisteria')

    def test_calil_service(self):
        query = BookSearchQuery()
        query.set('isbn', '9784532280208')
        calil_book = CalilService.get_one_book(query)
        print(calil_book.get_text_message())

    def test_get_one_book_from_json(self):
        json_data = json.loads('{"books": {"1111":{"system1":{"test":"hoge"}}}}')
        book = CalilService._CalilService__get_one_book_from_json(json_data, '1111', 'system1')
        assert book.isbn == '1111'
