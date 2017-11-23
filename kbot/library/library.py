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
    TEMPLATE_ONE_USER_RESERVED_BOOKS = 'one_user_reserved_books.tpl'

    def __init__(self, users):
        self.users = users
        self.all_rental_books_count = 0
        self.all_reserved_books_count = 0

    def check_rental_books(self, filter_setting):
        html_page = HtmlPage()

        new_users = self.users.filter(filter_setting.users)
        for user in new_users.list:
            Log.info(user.name)
            rental_books = self.__get_rental_books(html_page, user)
            filterd_rental_books = RentalBooks.get_filtered_books(
                rental_books,
                filter_setting)
            user.set_rental_books(filterd_rental_books)
            self.all_rental_books_count += user.rental_books_count

        html_page.release_resource()

        return new_users

    def __get_rental_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        books = HtmlParser.get_rental_books(html)
        return books

    def check_reserved_books(self, filter_setting):
        html_page = HtmlPage()

        new_users = self.users.filter(filter_setting.users)
        for user in new_users.list:
            Log.info(user.name)
            reserved_books = self.__get_reserved_books(html_page, user)
            filterd_reserved_books = ReservedBooks.get_filtered_books(
                reserved_books,
                filter_setting)
            user.set_reserved_books(filterd_reserved_books)
            self.all_reserved_books_count += user.reserved_books_count

        html_page.release_resource()

        return new_users

    def __get_reserved_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        reserved_books = HtmlParser.get_reserved_books(html)
        return reserved_books

    def check_rental_and_reserved_books(self, rental_filter, reserved_filter):
        html_page = HtmlPage()

        new_users = self.users.filter(rental_filter.users)
        for user in new_users.list:
            Log.info(user.name)
            self.__set_rental_and_reserved_books(html_page, user)
            user.set_rental_books(RentalBooks.get_filtered_books(
                user.rental_books,
                rental_filter))
            user.set_reserved_books(ReservedBooks.get_filtered_books(
                user.reserved_books,
                reserved_filter))
            self.all_rental_books_count += user.rental_books_count
            self.all_reserved_books_count += user.reserved_books_count

        html_page.release_resource()

        return new_users

    def __set_rental_and_reserved_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        HtmlParser.set_rental_and_reserved_books(html, user)

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

    def is_prepared_reserved_book(self, users):
        for user in users.list:
            if user.reserved_books.is_prepared_reserved_book():
                return True
        return False

    def is_prepared_reserved_book_at_one_user(self, user):
        if user.reserved_books.is_prepared_reserved_book():
            return True
        return False

    def get_text_message(self, users):
        return self.__get_message(users, format='text')

    def get_html_message(self, users):
        return self.__get_message(users, format='html')

    def __get_message(self, users, format='text'):
        sub_message = ''
        for user in users.list:
            sub_message += user.rental_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message}
        message += Message.create(os.path.join(format,
                                               Library.TEMPLATE_USER_RENTAL_BOOKS), data)

        return message

    def get_text_reserved_books_message(self, users):
        return self.__get_reserved_books_message(users, format='text')

    def get_html_reserved_books_message(self, users):
        return self.__get_reserved_books_message(users, format='html')

    def __get_reserved_books_message(self, users, format='text'):
        sub_message = ''
        for user in users.list:
            sub_message += user.reserved_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message,
                'is_prepared': self.is_prepared_reserved_book(users)}
        message += Message.create(os.path.join(format,
                                               Library.TEMPLATE_USER_RESERVED_BOOKS), data)

        return message

    def get_text_rental_and_reserved_books_message(self, user, format='text'):
        sub_message1 = ''
        sub_message1 += user.rental_books.get_message(format)
        sub_message2 = ''
        sub_message2 += user.reserved_books.get_message(format)

        message = ''
        data = {'sub_message1': sub_message1,
                'sub_message2': sub_message2}
        message += Message.create(os.path.join(format,
                                               Library.TEMPLATE_ONE_USER_RESERVED_BOOKS), data)

        return message
