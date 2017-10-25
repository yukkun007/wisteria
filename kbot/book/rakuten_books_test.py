#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
from unittest.mock import MagicMock, patch
from kbot.kbot import KBot
from kbot.book.rakuten_books import RakutenBooksService, BookSearchQuery

class TestRakutenBooksService:

    def setup(self):
        kbot = KBot('wisteria')

    @patch('kbot.book.rakuten_books.requests')
    def test_request(self, mock_requests):
        mock_response = MagicMock()
        mock_response.json.return_value = ["test"]
        mock_requests.get.return_value = mock_response
        query = BookSearchQuery()
        json_data = RakutenBooksService._RakutenBooksService__request(query)
        assert mock_requests.get.called
        assert mock_response.json.called
        assert json_data == ["test"]

    def test_convert_query(self):
        query = BookSearchQuery()
        RakutenBooksService._RakutenBooksService__convert_query(query)
        assert query.dict().get('applicationId') == os.environ['RAKUTEN_APP_ID']
        assert query.dict().get('sort') == 'sales'

    def test_query(self):
        query = BookSearchQuery()
        query.set('test', 'hoge')
        assert query.dict().get('test') == 'hoge'

