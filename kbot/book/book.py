# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
from jinja2 import Template, Environment, FileSystemLoader
from linebot.models import ButtonsTemplate, CarouselTemplate, CarouselColumn
from linebot.models import URITemplateAction, PostbackTemplateAction
from kbot.log import Log
from kbot.image import Image
from kbot.gyazo import Gyazo
from kbot.image_magic import ImageMagic

class Book(object):

    def __init__(self, json):
        self.title          = json.get('title',         '')
        self.isbn           = json.get('isbn',          '')
        self.author         = json.get('author',        '')
        self.caption        = json.get('itemCaption',   '')
        self.price          = json.get('itemPrice',     '')
        self.url            = json.get('itemUrl',       '')
        self.image_url      = json.get('largeImageUrl', '')
        self.reserveurl     = json.get('reserveurl',    '')
        self.libkey         = json.get('libkey',        '')
        self.reserveurl_add = ''
        self.libkey_add     = ''

    def add_reserve_info(self, json):
        self.reserveurl_add = json.get('reserveurl')
        self.libkey_add     = json.get('libkey')

    def merge(self, book):
        self.title      = self.title if book.title == '' else book.title
        self.isbn       = self.isbn if book.isbn == '' else book.isbn
        self.author     = self.author if book.author == '' else book.author
        self.caption    = self.caption if book.caption == '' else book.caption
        self.price      = self.price if book.price == '' else book.price
        self.url        = self.url if book.url == '' else book.url
        self.image_url  = self.image_url if book.image_url == '' else book.image_url
        self.reserveurl = self.reserveurl if book.reserveurl == '' else book.reserveurl
        self.libkey     = self.libkey if book.libkey == '' else book.libkey

    def log(self):
        Log.info('title : ' + self.title)
        Log.info('isbn : ' + self.isbn)
        Log.info('author : ' + self.author)
        Log.info('caption : ' + self.caption)
        Log.info('url : ' + self.url)
        Log.info('image_url : ' + self.image_url)
        Log.info('price : ' + str(self.price))
        Log.info('reserveurl : ' + self.reserveurl)
        Log.info('libkey : ' + str(self.libkey))
        Log.info('reserveurl_add : ' + self.reserveurl_add)
        Log.info('libkey_add : ' + str(self.libkey_add))

    def get_book_info_line_text_message(root_dir, book):
        env = Environment(loader=FileSystemLoader(root_dir))

        book_id = book.reserveurl.split('=')[-1]

        template  = env.get_template('templates/kbot/book/book_info.tpl')
        data      = {'book': book, 'book_id': book_id, 'my_server_name': os.environ['MY_SERVER_NAME'] }
        message   = template.render(data)

        return message

    def get_books_select_line_carousel_mseeage(books):
        columns = []
        for book in books:

            image       = Image()
            path        = image.download(book.image_url)
            image_magic = ImageMagic()
            image_magic.convert(path)
            gyazo       = Gyazo()
            gyazo_url   = gyazo.upload(path)

            text = '著:' + book.author + '\n￥' + str(book.price) + '\nISBN:' + book.isbn
            text = text[:60]
            column = CarouselColumn(
                thumbnail_image_url = gyazo_url,
                title               = book.title[:40],
                text                = text,
                actions             = [
                    PostbackTemplateAction(
                        label = '借りる / 買う',
                        data  = 'isbn:' + book.isbn)
                ]
            )
            columns.append(column)

        carousel_template = CarouselTemplate(columns=columns)

        return carousel_template

