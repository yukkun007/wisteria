# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import requests
from linebot.models import CarouselTemplate, CarouselColumn
from linebot.models import PostbackTemplateAction
from kbot.book.book import Book
from kbot.image import Image
from kbot.gyazo import Gyazo
from kbot.image_magic import ImageMagic


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
        message = 'new [' + str(type(self)) + \
            '] illegal source: ' + str(type(source))
        print(message)
        raise RuntimeError(message)

    def length(self):
        return len(self.books)

    def slice(self, start, end):
        return Books(self.books[start:end])

    def get(self, index):
        return self.books[index]

    def get_books_select_line_carousel_mseeage(self):

        if self.length() == 0:
            return '見つかりませんでした。。'

        columns = []
        for book in self.books:

            image = Image()
            path = image.download(book.image_url)
            image_magic = ImageMagic()
            image_magic.convert(path)
            gyazo = Gyazo()
            gyazo_url = gyazo.upload(path)

            text = '著:' + book.author +\
                   '\n￥' + str(book.price) +\
                   '\n発売日:' + book.sales_date
            text = text[:60]
            column = CarouselColumn(
                thumbnail_image_url=gyazo_url,
                title=book.title[:40],
                text=text,
                actions=[
                    PostbackTemplateAction(
                        label='借りる / 買う',
                        data='isbn:' + book.isbn)
                ]
            )
            columns.append(column)

        return CarouselTemplate(columns=columns)


class BookSearchQuery(object):

    def __init__(self):
        self.query = {}

    def set(self, key, value):
        self.query[key] = value

    def get(self, key):
        return self.query.get(key)

    def dict(self):
        return self.query


class RakutenBooksService(object):

    RAKUTEN_BASE_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    @classmethod
    def get_one_book(cls, query):
        json_data = RakutenBooksService.__request(query)
        books = Books(json_data)
        if books.length() <= 0:
            return Book()
        return books.get(0)

    @classmethod
    def search_books(cls, query):
        json_data = RakutenBooksService.__request(query)
        return Books(json_data)

    @classmethod
    def __request(cls, query):
        response = requests.get(
            RakutenBooksService.RAKUTEN_BASE_URL,
            params=RakutenBooksService.__adjust_query(query))
        json_data = response.json()  # TODO:nullチェック
        return json_data

    @classmethod
    def __adjust_query(cls, query):
        query.set('applicationId', os.environ['RAKUTEN_APP_ID'])
        query.set('sort', 'sales')
        return query.dict()
