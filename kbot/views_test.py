#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.views import __library_check as library_check
from kbot.views import __library_check_reserve as library_check_reserve
from kbot.views import __youtube_omoide as youtube_omoide
from kbot.views import __check_rental as check_rental
from kbot.views import __check_expire as check_expire
from kbot.views import __check_expired as check_expired
from kbot.views import __show_reply_string as show_reply_string
from kbot.views import __check_reserved_books as check_reserved_books
from kbot.views import __search_book as search_book
from kbot.views import __search_library_book as search_library_book
from kbot.views import __search_book_by_isbn as search_book_by_isbn
from kbot.kbot import KBot
from kbot.library.rental_book import RentalBookFilter
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

    def test_check_rental(self):
        filter_setting = RentalBookFilter(users='all')
        check_rental(None, filter_setting)

    def test_check_expire(self):
        check_expire(None, 2)

    def test_check_expired(self):
        check_expired(None)

    def test_show_reply_string(self):
        show_reply_string(None)

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
        search_library_book(None, 'ほ？あ')
