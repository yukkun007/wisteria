#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import pytest
from unittest.mock import MagicMock, patch
from kbot.kbot import KBot
from kbot.book.common import BookSearchQuery
from kbot.book.rakuten_books import RakutenBooksService, RakutenBooks, RakutenBook, RakutenBooksQuery


class TestRakutenBooksService:

    def setup(self):
        KBot('wisteria')

    def test_get_one_book(self):
        RakutenBooksService._RakutenBooksService__request = MagicMock()
        json_str = '''
            { "Items": [
                    {"Item": {"title": "hoge"}},
                    {"Item": {"title": "hogehoge"}}]
            }
        '''
        RakutenBooksService._RakutenBooksService__request.return_value = json.loads(
            json_str)
        query = BookSearchQuery()
        rakuten_book = RakutenBooksService.get_one_book(query)
        assert RakutenBooksService._RakutenBooksService__request.called
        assert rakuten_book.title == 'hoge'

    def test_search_book(self):
        query = BookSearchQuery()
        query.set('title', 'カンブリア')
        rakuten_books = RakutenBooksService.search_books(query)
        print(rakuten_books.slice(0, 5).get_books_select_line_carousel_mseeage())

    @patch('kbot.book.rakuten_books.requests')
    def test_request(self, mock_requests):
        mock_response = MagicMock()
        mock_response.json.return_value = ['test']
        mock_requests.get.return_value = mock_response
        # TODO:
        # query = BookSearchQuery()
        # json_data = RakutenBooksService._RakutenBooksService__request(query)
        # assert mock_requests.get.called
        # assert mock_response.json.called
        # assert json_data == ['test']


class TestRakutenBooksQuery:

    def test_adjust_query(self):
        query = BookSearchQuery()
        RakutenBooksQuery.adjust_query(query)
        assert query.dict().get(
            'applicationId') == os.environ['RAKUTEN_APP_ID']
        assert query.dict().get('sort') == 'sales'


class TestRakutenBooks:

    @pytest.fixture()
    def books1(request):
        json_str = '''
            { "Items": [
                {"Item": {"title": "hoge"}},
                {"Item": {"title": "hogehoge"}}]
            }
        '''
        rakuten_book = RakutenBooks(json.loads(json_str))
        return rakuten_book

    def setup(self):
        KBot('wisteria')

    def test_new(self, books1):
        assert isinstance(books1, RakutenBooks)
        assert books1.length() == 2

    def test_new_empty(self):
        rakuten_book = RakutenBooks(json.loads('{"Items": []}'))
        assert isinstance(rakuten_book, RakutenBooks)
        assert rakuten_book.length() == 0

    def test_new_from_list(self):
        rakuten_book = RakutenBooks(['', ''])
        assert isinstance(rakuten_book, RakutenBooks)
        assert rakuten_book.length() == 2

    def test_new_from_list_empty(self):
        rakuten_book = RakutenBooks([])
        assert isinstance(rakuten_book, RakutenBooks)
        assert rakuten_book.length() == 0

    def test_new_from_illegal_source(self):
        with pytest.raises(RuntimeError):
            RakutenBooks('hoge')

    def test_slice(self, books1):
        rakuten_book = books1.slice(0, 0)
        assert rakuten_book.length() == 0

    def test_slice_one(self, books1):
        rakuten_book = books1.slice(0, 1)
        assert rakuten_book.length() == 1

    def test_get(self, books1):
        book = books1.get(0)
        assert isinstance(book, RakutenBook)
        assert book.title == 'hoge'
