#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.message import Message
from kbot.log import Log

class Library(object):

    LIBRALY_HOME_URL = "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWUSERCONF.CSP"
    LIBRALY_BOOK_URL = "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWBOOK.CSP?DB=LIB&MODE=1&PID2=OPWSRCH1&SRCID=1&WRTCOUNT=10&LID=1&GBID={0}&DispDB=LIB"

    TEMPLATE_HEADER              = "header.tpl"
    TEMPLATE_FOOTER              = "footer.tpl"
    TEMPLATE_USER_RESERVED_BOOKS = 'user_reserved_books.tpl'

    def __init__(self, users):
        self.users                    = users
        self.all_rental_books_count   = 0
        self.all_reserved_books_count = 0

    def yoyaku(self, user_num, book_id):
        return HtmlPage.reserve(
            Library.LIBRALY_HOME_URL,
            self.users[int(user_num) - 1],
            Library.LIBRALY_BOOK_URL.format(book_id)
        )

    def check_reserved_books(self, user_nums):
        nums = user_nums.split(',')

        for num in nums:
            user_num = int(num) - 1
            if 0 <= user_num < len(self.users):
                user = self.users[user_num]

                Log.info(user.name)
                reserved_books = self.__get_reserved_books(user)
                user.set_reserved_books(reserved_books)
                self.all_reserved_books_count += user.reserved_books_count

    def __get_reserved_books(self, user):
        html           = HtmlPage.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        reserved_books = HtmlParser.get_reserved_books(html)
        return reserved_books

    def fetch_status(self, filter_setting):
        for user in self.users:
            rental_books = self.__get_rental_books(user)
            filterd_rental_books = rental_books.get_filtered_books(filter_setting)
            user.set_rental_books(filterd_rental_books)
            self.all_rental_books_count += user.rental_books_count

    def __get_rental_books(self, user):
        html   = HtmlPage.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        books  = HtmlParser.get_rental_books(html)
        return books

    def is_target_exist(self):
        if self.all_rental_books_count > 0:
            return True
        return False

    def get_text_message(self, filter_setting):
        return self.__get_message(filter_setting, format='text')

    def get_html_message(self, filter_setting):
        return self.__get_message(filter_setting, format='html')

    def __get_message(self, filter_setting, format='text'):
        message = ''

        data      = {}
        message += Message.create(os.path.join(format, Library.TEMPLATE_HEADER), data)

        for user in self.users:
            message += user.rental_books.get_message(user, filter_setting, format)

        data     = {'all_books_count': self.all_rental_books_count}
        message += Message.create(os.path.join(format, Library.TEMPLATE_FOOTER), data)

        return message

    def get_text_reserved_books_message(self):
        return self.__get_reserved_books_message(format='text')

    def get_html_reserved_books_message(self):
        return self.__get_reserved_books_message(format='html')

    def __get_reserved_books_message(self, format='text'):
        sub_message = ''
        for user in self.users:
            sub_message += user.reserved_books.get_message(user, format)

        message = ''
        data      = { 'sub_message': sub_message,
                      'is_prepared': self.prepared_reserved_book() }
        message += Message.create(os.path.join(format, Library.TEMPLATE_USER_RESERVED_BOOKS), data)

        return message

    def prepared_reserved_book(self):
        for user in self.users:
            if user.reserved_books.prepared_reserved_book():
                return True
        return False

