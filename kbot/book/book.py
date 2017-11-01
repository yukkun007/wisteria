# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
from kbot.log import Log
from kbot.message import Message
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
        self.sales_date     = json.get('salesDate',     '')
        self.reserveurl     = json.get('reserveurl',    '')
        self.libkey         = json.get('libkey',        '')
        self.reserveurl_add = ''
        self.libkey_add     = ''
        self.id             = self.reserveurl.split('=')[-1]

        self.log()

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
        self.sales_date = self.sales_date if book.sales_date == '' else book.sales_date
        self.reserveurl = self.reserveurl if book.reserveurl == '' else book.reserveurl
        self.libkey     = self.libkey if book.libkey == '' else book.libkey
        self.id         = self.reserveurl.split('=')[-1]

    def log(self):
        Log.info('title : ' + self.title)
        Log.info('isbn : ' + self.isbn)
        Log.info('author : ' + self.author)
        Log.info('caption : ' + self.caption)
        Log.info('price : ' + str(self.price))
        Log.info('url : ' + self.url)
        Log.info('image_url : ' + self.image_url)
        Log.info('sales_date : ' + self.sales_date)
        Log.info('reserveurl : ' + self.reserveurl)
        Log.info('libkey : ' + str(self.libkey))
        Log.info('reserveurl_add : ' + self.reserveurl_add)
        Log.info('libkey_add : ' + str(self.libkey_add))

    def get_text_info_message(self):
        data      = {'book': self, 'my_server_name': os.environ['MY_SERVER_NAME'] }
        message = Message.create('text/book_info.tpl', data)
        return message


