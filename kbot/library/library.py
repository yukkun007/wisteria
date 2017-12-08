#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.log import Log
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks


class Library(object):

    LIBRALY_HOME_URL = 'https://www.lib.nerima.tokyo.jp/opw/OPW/OPWUSERCONF.CSP'
    LIBRALY_BOOK_URL = ('https://www.lib.nerima.tokyo.jp/opw/OPW/OPWBOOK.CSP?DB='
                        'LIB&MODE=1&PID2=OPWSRCH1&SRCID=1&WRTCOUNT=10&LID=1&GBID={0}&DispDB=LIB')

    LIBRALY_SEARCH_URL = ('https://www.lib.nerima.tokyo.jp/opw/OPW/OPWSRCHLIST.CSP?'
                          'DB=LIB&FLG=SEARCH&LOCAL(%22LIB%22,%22SK41%22,1)=on&MODE=1&'
                          'PID2=OPWSRCH2&SORT=-3&opr(1)=OR&qual(1)=ALL&WRTCOUNT=100&text(1)=')

    def __init__(self, users):
        self.users = users

    @classmethod
    def search_books(cls, query):
        html_page = HtmlPage()
        html = html_page.fetch_search_result_page(Library.LIBRALY_SEARCH_URL + query.title)
        books = HtmlParser.get_searched_books(html)
        html_page.release_resource()
        return books

    def check_rental_books(self, filter_setting):
        html_page = HtmlPage()

        target_users = self.users.filter(filter_setting.users)
        for user in target_users.list:
            Log.info(user.name)
            rental_books = self.__get_rental_books(html_page, user)
            filterd_rental_books = RentalBooks.get_filtered_books(
                rental_books,
                filter_setting)
            user.set_rental_books(filterd_rental_books)

        html_page.release_resource()

        return target_users

    def __get_rental_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        books = HtmlParser.get_rental_books(html)
        return books

    def check_reserved_books(self, filter_setting):
        html_page = HtmlPage()

        target_users = self.users.filter(filter_setting.users)
        for user in target_users.list:
            Log.info(user.name)
            reserved_books = self.__get_reserved_books(html_page, user)
            filterd_reserved_books = ReservedBooks.get_filtered_books(
                reserved_books,
                filter_setting)
            user.set_reserved_books(filterd_reserved_books)

        html_page.release_resource()

        return target_users

    def __get_reserved_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        reserved_books = HtmlParser.get_reserved_books(html)
        return reserved_books

    def check_rental_and_reserved_books(self, rental_filter, reserved_filter):
        html_page = HtmlPage()

        target_users = self.users.filter(rental_filter.users)
        for user in target_users.list:
            Log.info(user.name)
            self.__set_rental_and_reserved_books(html_page, user)
            user.set_rental_books(RentalBooks.get_filtered_books(
                user.rental_books,
                rental_filter))
            user.set_reserved_books(ReservedBooks.get_filtered_books(
                user.reserved_books,
                reserved_filter))

        html_page.release_resource()

        return target_users

    def __set_rental_and_reserved_books(self, html_page, user):
        html = html_page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        HtmlParser.set_rental_and_reserved_books(html, user)

    def reserve(self, user_num, book_id):
        return HtmlPage.reserve(
            Library.LIBRALY_HOME_URL,
            self.users.all[int(user_num)],
            Library.LIBRALY_BOOK_URL.format(book_id)
        )
