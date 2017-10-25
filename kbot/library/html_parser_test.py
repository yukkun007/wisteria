#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_pages import HtmlPages
from kbot.library.html_parser import HtmlParser
from kbot.library.library import Library

class TestHtmlParser:

    def test_get_rental_books(self):
        kbot = KBot('wisteria')
        pages = HtmlPages()
        user = User(os.environ['USER1'])
        html = pages.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        pages.finalize()

        parser = HtmlParser(html)
        rental_books = parser.get_rental_books()

