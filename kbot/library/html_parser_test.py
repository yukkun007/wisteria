#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.library.library import Library

class TestHtmlParser:

    def test_get_rental_books(self):
        KBot('wisteria')
        page = HtmlPage()
        user = User(os.environ['USER1'])
        html = page.fetch_login_page(Library.LIBRALY_HOME_URL, user)

        HtmlParser.get_rental_books(html)

