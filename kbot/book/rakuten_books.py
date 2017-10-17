# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests
from kbot.book.book import Book

class RakutenBooks(object):

    RAKUTEN_BASE_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'
    RAKUTEN_APP_ID   = os.environ['RAKUTEN_APP_ID']

    def __init__(self):
        pass

    def get_book(self, isbn):
        query                  = {}
        query['isbn']          = isbn
        query['applicationId'] = RakutenBooks.RAKUTEN_APP_ID
        query['sort']          = 'sales'
        res = requests.get(RakutenBooks.RAKUTEN_BASE_URL, params=query).json()

        for item in res['Items']:
            book = Book(item['Item'])
            break

        book.log()

        return book

    def search_books(self, query):
        query['applicationId'] = RakutenBooks.RAKUTEN_APP_ID
        query['sort']          = 'sales'
        res = requests.get(RakutenBooks.RAKUTEN_BASE_URL, params=query).json()

        result = []
        for item in res['Items']:
            book = Book(item['Item'])
            result.append(book)
            if len(result) >=5:
                break

        return result

