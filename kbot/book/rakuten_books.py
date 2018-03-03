# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import requests
from linebot.models import CarouselTemplate, CarouselColumn
from linebot.models import PostbackTemplateAction
from kbot.log import Log
from kbot.message import Message
from kbot.image import Image
from kbot.gyazo import Gyazo
from kbot.image_magic import ImageMagic


class RakutenBooksService(object):

    RAKUTEN_BASE_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    @classmethod
    def get_one_book(cls, query):
        json_data = RakutenBooksService.__request(query)
        rakuten_books = RakutenBooks(json_data)
        if rakuten_books.length() <= 0:
            return RakutenBook({})
        return rakuten_books.get(0)

    @classmethod
    def search_books(cls, query):
        json_data = RakutenBooksService.__request(query)
        return RakutenBooks(json_data)

    @classmethod
    def __request(cls, query):
        response = requests.get(
            RakutenBooksService.RAKUTEN_BASE_URL,
            params=RakutenBooksQuery.adjust_query(query))
        json_data = response.json()  # TODO:nullチェック
        return json_data


class RakutenBooksQuery(object):

    @classmethod
    def adjust_query(cls, query):
        query.set('applicationId', os.environ['RAKUTEN_APP_ID'])
        query.set('sort', 'sales')
        return query.dict()


class RakutenBooks(object):

    def __init__(self, source):
        self.rakuten_books = []
        if isinstance(source, dict):
            self.__set_books_from_dict(source)
        elif isinstance(source, list):
            self.rakuten_books = source
        else:
            self.__raise_exception(source)

    def __set_books_from_dict(self, source_dict):
        for item in source_dict.get('Items'):
            self.rakuten_books.append(RakutenBook(item.get('Item')))

    def __raise_exception(self, source):
        message = 'new [' + str(type(self)) + \
            '] illegal source: ' + str(type(source))
        print(message)
        raise RuntimeError(message)

    def length(self):
        return len(self.rakuten_books)

    def slice(self, start, end):
        return RakutenBooks(self.rakuten_books[start:end])

    def get(self, index):
        return self.rakuten_books[index]

    def get_books_select_line_carousel_mseeage(self):

        if self.length() == 0:
            return '見つかりませんでした。。'

        columns = []
        for rakuten_book in self.rakuten_books:

            image = Image()
            path = image.download(rakuten_book.image_url)
            image_magic = ImageMagic()
            image_magic.convert(path)
            gyazo = Gyazo()
            gyazo_url = gyazo.upload(path)

            text = '著:' + rakuten_book.author +\
                   '\n￥' + str(rakuten_book.price) +\
                   '\n発売日:' + rakuten_book.sales_date
            text = text[:60]
            column = CarouselColumn(
                thumbnail_image_url=gyazo_url,
                title=rakuten_book.title[:40],
                text=text,
                actions=[
                    PostbackTemplateAction(
                        label='借りる / 買う',
                        data='isbn:' + rakuten_book.isbn)
                ]
            )
            columns.append(column)

        return CarouselTemplate(columns=columns)


class RakutenBook(object):

    def __init__(self, json):
        self.isbn = json.get('isbn', '')
        self.title = json.get('title', '')
        self.author = json.get('author', '')
        self.caption = json.get('itemCaption', '')
        self.price = json.get('itemPrice', '')
        self.url = json.get('itemUrl', '')
        self.image_url = json.get('largeImageUrl', '')
        self.sales_date = json.get('salesDate', '')

        self.log()

    def log(self):
        Log.info('isbn : ' + self.isbn)
        Log.info('title : ' + self.title)
        Log.info('author : ' + self.author)
        Log.info('caption : ' + self.caption)
        Log.info('price : ' + str(self.price))
        Log.info('url : ' + self.url)
        Log.info('image_url : ' + self.image_url)
        Log.info('sales_date : ' + self.sales_date)

    def get_text_message(self):
        return Message.create_text_by_object(self)
