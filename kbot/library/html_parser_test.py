#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from unittest.mock import MagicMock
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.library.library import Library
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks


class TestHtmlParser:

    def setup(self):
        KBot('wisteria')

    def test_get_rental_books(self):
        page = HtmlPage()
        user = User(os.environ['USER1'])
        html = page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        HtmlParser.get_rental_books(html)

    def test_get_rental_books_no_table(self):
        method = MagicMock()
        method.return_value = None
        HtmlParser._HtmlParser__get_table = method
        books = HtmlParser._HtmlParser__get_rental_books(None, None)
        assert isinstance(books, RentalBooks)
        assert books.len == 0

    def test_get_reserved_books_no_table(self):
        method = MagicMock()
        method.return_value = None
        HtmlParser._HtmlParser__get_table = method
        books = HtmlParser._HtmlParser__get_reserved_books(None, None)
        assert isinstance(books, ReservedBooks)
        assert books.len == 0
