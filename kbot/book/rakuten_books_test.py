#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import pytest
from unittest.mock import MagicMock, patch
from kbot.kbot import KBot
from kbot.book.rakuten_books import RakutenBooksService, BookSearchQuery, Books
from kbot.book.book import Book


class TestBooks:

    @pytest.fixture()
    def books1(request):
        json_str = '''
            { "Items": [
                {"Item": {"title": "hoge"}},
                {"Item": {"title": "hogehoge"}}]
            }
        '''
        books = Books(json.loads(json_str))
        return books

    def setup(self):
        KBot('wisteria')

    def test_new(self, books1):
        assert isinstance(books1, Books)
        assert books1.length() == 2

    def test_new_empty(self):
        books = Books(json.loads('{"Items": []}'))
        assert isinstance(books, Books)
        assert books.length() == 0

    def test_new_from_list(self):
        books = Books(['', ''])
        assert isinstance(books, Books)
        assert books.length() == 2

    def test_new_from_list_empty(self):
        books = Books([])
        assert isinstance(books, Books)
        assert books.length() == 0


    def test_new_from_illegal_source(self):
        with pytest.raises(RuntimeError):
            Books('hoge')

    def test_slice(self, books1):
        books = books1.slice(0, 0)
        assert books.length() == 0

    def test_slice_one(self, books1):
        books = books1.slice(0, 1)
        assert books.length() == 1

    def test_get(self, books1):
        book = books1.get(0)
        assert isinstance(book, Book)
        assert book.title == 'hoge'


class TestBookSearchQuery:

    def test_query(self):
        query = BookSearchQuery()
        query.set('test', 'hoge')
        assert query.dict().get('test') == 'hoge'


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
        book = RakutenBooksService.get_one_book(query)
        assert RakutenBooksService._RakutenBooksService__request.called
        assert book.title == 'hoge'

    @patch('kbot.book.rakuten_books.requests')
    def test_request(self, mock_requests):
        mock_response = MagicMock()
        mock_response.json.return_value = ['test']
        mock_requests.get.return_value = mock_response
        query = BookSearchQuery()
        json_data = RakutenBooksService._RakutenBooksService__request(query)
        assert mock_requests.get.called
        assert mock_response.json.called
        assert json_data == ['test']

    def test_adjust_query(self):
        query = BookSearchQuery()
        RakutenBooksService._RakutenBooksService__adjust_query(query)
        assert query.dict().get(
            'applicationId') == os.environ['RAKUTEN_APP_ID']
        assert query.dict().get('sort') == 'sales'
