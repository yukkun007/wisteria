# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests
from kbot.book.book import Book

class BookSearchQuery(object):
    def __init__(self):
        self.query = {}

    def set(self, key, value):
        self.query[key] = value

    def dict(self):
        return self.query


class RakutenBooksService(object):

    RAKUTEN_BASE_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    def __init__(self):
        pass

    def get_one_book(self, query):
        json_data = __request(query)

        book = Book(json_data['Items']['Item']) # TODO:nullチェック
        # for item in res['Items']:
        #     book = Book(item['Item'])
        #     break

        book.log()

        return book

    def search_books(self, query):
        json_data = RakutenBooksService.__request(query)

        books = []
        for item in json_data['Items']:
            book = Book(item['Item'])
            books.append(book)
            if len(books) >=5:
                break

        return books

    @classmethod
    def __request(cls, query):
        response = requests.get(RakutenBooksService.RAKUTEN_BASE_URL, params=RakutenBooksService.__convert_query(query))
        json_data = response.json() # TODO:nullチェック
        return json_data

    @classmethod
    def __convert_query(cls, query):
        query.set('applicationId', os.environ['RAKUTEN_APP_ID'])
        query.set('sort', 'sales')
        return query.dict()

