#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.views import __library_check as library_check
from kbot.views import __library_check_reserve as library_check_reserve
from kbot.views import __youtube_omoide as youtube_omoide
from kbot.views import __check_rental_books as check_rental_books
from kbot.views import __reply_command_menu as reply_command_menu
from kbot.views import __reply_response_string as reply_response_string
from kbot.views import __check_reserved_books as check_reserved_books
from kbot.views import __search_book as search_book
from kbot.views import __search_library_book as search_library_book
from kbot.views import __search_book_by_isbn as search_book_by_isbn
from kbot.kbot import KBot
from kbot.library.rental_book import RentalBookFilter, RentalBookExpireFilter, RentalBookExpiredFilter
from kbot.library.reserved_book import ReservedBookFilter


class TestViews:

    def setup(self):
        KBot('wisteria')

    def test_library_check(self):
        library_check()

    def test_library_check_reserve(self):
        library_check_reserve()

    def test_youtube_omoide(self):
        youtube_omoide()

    def test_check_rental_books(self):
        filter_setting = RentalBookFilter(users='all')
        check_rental_books(None, filter_setting)

    def test_check_rental_books_expire(self):
        filter_setting = RentalBookExpireFilter(users='all', xdays=2)
        check_rental_books(None, filter_setting)

    def test_check_rental_books_expired(self):
        filter_setting = RentalBookExpiredFilter(users='all')
        check_rental_books(None, filter_setting)

    def test_reply_command_menu(self):
        reply_command_menu(None)

    def test_reply_response_string(self):
        reply_response_string(None)

    def test_check_reserved_books(self):
        filter_setting = ReservedBookFilter(users='0,1,2,3')
        check_reserved_books(None, filter_setting)

    def test_check_reserved_books2(self):
        filter_setting = ReservedBookFilter(users='0,2')
        check_reserved_books(None, filter_setting)

    def test_search_book_title(self):
        search_book(None, '本？坊っちゃん')

    def test_search_book_author(self):
        search_book(None, '著？夏目漱石')

    def test_search_book_by_isbn(self):
        search_book_by_isbn(None, 'isbn:9784532280208')

    def test_search_library_book(self):
        search_library_book(None, 'ほ？坊っちゃん')

    def test_search_library_book_no_hit(self):
        search_library_book(None, 'ほ？あ')
