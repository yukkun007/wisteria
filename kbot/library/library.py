#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.log import Log
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks


class Library(object):

    LIBRALY_HOME_URL = "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWUSERCONF.CSP"
    LIBRALY_BOOK_URL = (
        "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWBOOK.CSP?DB="
        "LIB&MODE=1&PID2=OPWSRCH1&SRCID=1&WRTCOUNT=10&LID=1&GBID={0}&DispDB=LIB"
    )

    def __init__(self, users):
        self.users = users

    @classmethod
    def __create_empty_books(cls, books_class_name):
        if books_class_name in {"RentalBooks"}:
            return RentalBooks()
        elif books_class_name == "ReservedBooks":
            return ReservedBooks()

    def __check_books(self, book_filters):
        html_page = HtmlPage()

        first_book_filter = book_filters[0]
        print("-------------> first_book_filter.users:" + first_book_filter.users)
        target_users = self.users.filter(first_book_filter.users)
        for user in target_users.list:
            Log.info(user.name)

            html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)

            for book_filter in book_filters:
                empty_books = Library.__create_empty_books(book_filter.books_class_name)
                books = HtmlParser.get_books(html, empty_books)
                books.apply_filter(book_filter)
                user.set_books(book_filter.books_class_name, books)

        html_page.release_resource()

        return target_users

    def check_rental_and_reserved_books(self, rental_filter, reserved_filter):
        return self.__check_books([rental_filter, reserved_filter])

    def check_books(self, filter_setting):
        return self.__check_books([filter_setting])

    def reserve(self, user_num, book_id):
        html_page = HtmlPage()
        return_url = html_page.reserve(
            Library.LIBRALY_HOME_URL,
            self.users.get(int(user_num)),
            Library.LIBRALY_BOOK_URL.format(book_id),
        )
        html_page.release_resource()
        return return_url
