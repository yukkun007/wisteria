# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests
from kbot.book.book import Book

class Books(object):

    def __init__(self, source):
        self.books = []
        if isinstance(source, dict):
            self.__set_books_from_dict(source)
        elif isinstance(source, list):
            self.books = source
        else:
            self.__raise_exception(source)

    def __set_books_from_dict(self, source_dict):
        for item in source_dict.get('Items'):
            self.books.append(Book(item.get('Item')))

    def __raise_exception(self, source):
        message = 'new [' + str(type(self)) + '] illegal source: ' + str(type(source))
        print(message)
        raise RuntimeError(message)

    def length(self):
        return len(self.books)

    def slice(self, start, end):
        return Books(self.books[start:end])

    def get(self, index):
        return self.books[index]


class BookSearchQuery(object):

    def __init__(self):
        self.query = {}

    def set(self, key, value):
        self.query[key] = value

    def dict(self):
        return self.query


class RakutenBooksService(object):

    RAKUTEN_BASE_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    @classmethod
    def get_one_book(cls, query):
        json_data = RakutenBooksService.__request(query)
        books     = Books(json_data)
        if books.length() <= 0:
            return Book()
        return books.get(0)

    @classmethod
    def search_books(cls, query):
        json_data = RakutenBooksService.__request(query)
        return Books(json_data)

    @classmethod
    def __request(cls, query):
        response = requests.get(RakutenBooksService.RAKUTEN_BASE_URL, params=RakutenBooksService.__adjust_query(query))
        json_data = response.json() # TODO:nullチェック
        return json_data

    @classmethod
    def __adjust_query(cls, query):
        query.set('applicationId', os.environ['RAKUTEN_APP_ID'])
        query.set('sort', 'sales')
        return query.dict()

