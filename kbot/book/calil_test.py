# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import json
from unittest.mock import patch, MagicMock
from kbot.kbot import KBot
from kbot.book.calil import CalilService, CalilQuery
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

    def test_polling(self):
        with patch('kbot.book.calil.CalilService._CalilService__polling_request') as mock:
            json_data = json.loads('{"continue": 1, "session": "hoge"}')
            CalilService._CalilService__polling(json_data)
            mock.assert_called_once()

    def test_polling_request(self):
        with patch('kbot.book.calil.CalilService._CalilService__request_sub') as mock:
            response_mock = MagicMock()
            response_mock.text = 'callback({"books": {"1111":{"system1":{"test":"hoge"}}}} )'
            mock.return_value = response_mock
            query = BookSearchQuery()
            result = CalilService._CalilService__polling_request(query)
            mock.assert_called_once()
            assert json.dumps(result) == '{"books": {"1111": {"system1": {"test": "hoge"}}}}'


class TestCalilQuery(object):

    def test_adjust_next_query(self):
        query = BookSearchQuery()
        query.set('foo', 'bar')
        result = CalilQuery.adjust_next_query(query)
        assert result.get('foo') == query.get('foo')
