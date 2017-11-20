#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.message import Message
from kbot.log import Log
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks


class Library(object):

    LIBRALY_HOME_URL = 'https://www.lib.nerima.tokyo.jp/opw/OPW/OPWUSERCONF.CSP'
    LIBRALY_BOOK_URL = ('https://www.lib.nerima.tokyo.jp/opw/OPW/OPWBOOK.CSP?DB='
                        'LIB&MODE=1&PID2=OPWSRCH1&SRCID=1&WRTCOUNT=10&LID=1&GBID={0}&DispDB=LIB')

    TEMPLATE_USER_RENTAL_BOOKS = 'user_rental_books.tpl'
    TEMPLATE_USER_RESERVED_BOOKS = 'user_reserved_books.tpl'

    def __init__(self, users):
        self.users = users
        self.all_rental_books_count = 0
        self.all_reserved_books_count = 0

    def check_rental_books(self, filter_setting):
        html_page = HtmlPage()

        self.users.filter(filter_setting.users)
        for user in self.users.list:
            Log.info(user.name)
            rental_books = self.__get_rental_books(html_page, user)
            filterd_rental_books = RentalBooks.get_filtered_books(
                rental_books,
                filter_setting)
            user.set_rental_books(filterd_rental_books)
            self.all_rental_books_count += user.rental_books_count

        html_page.release_resource()

    def __get_rental_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        books = HtmlParser.get_rental_books(html)
        return books

    def check_reserved_books(self, filter_setting):
        html_page = HtmlPage()

        self.users.filter(filter_setting.users)
        for user in self.users.list:
            Log.info(user.name)
            reserved_books = self.__get_reserved_books(html_page, user)
            filterd_reserved_books = ReservedBooks.get_filtered_books(
                reserved_books,
                filter_setting)
            user.set_reserved_books(filterd_reserved_books)
            self.all_reserved_books_count += user.reserved_books_count

        html_page.release_resource()

    def __get_reserved_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        reserved_books = HtmlParser.get_reserved_books(html)
        return reserved_books

    def reserve(self, user_num, book_id):
        return HtmlPage.reserve(
            Library.LIBRALY_HOME_URL,
            self.users.all[int(user_num)],
            Library.LIBRALY_BOOK_URL.format(book_id)
        )

    def is_rental_books_exist(self):
        if self.all_rental_books_count > 0:
            return True
        return False

    def is_prepared_reserved_book(self):
        for user in self.users.all:
            if user.reserved_books.is_prepared_reserved_book():
                return True
        return False

    def get_text_message(self):
        return self.__get_message(format='text')

    def get_html_message(self):
        return self.__get_message(format='html')

    def __get_message(self, format='text'):
        sub_message = ''
        for user in self.users.list:
            sub_message += user.rental_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message,
                'all_books_count': self.all_rental_books_count}
        message += Message.create(os.path.join(format,
                                               Library.TEMPLATE_USER_RENTAL_BOOKS), data)

        return message

    def get_text_reserved_books_message(self):
        return self.__get_reserved_books_message(format='text')

    def get_html_reserved_books_message(self):
        return self.__get_reserved_books_message(format='html')

    def __get_reserved_books_message(self, format='text'):
        sub_message = ''
        for user in self.users.list:
            sub_message += user.reserved_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message,
                'is_prepared': self.is_prepared_reserved_book()}
        message += Message.create(os.path.join(format,
                                               Library.TEMPLATE_USER_RESERVED_BOOKS), data)

        return message
