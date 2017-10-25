#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_pages import HtmlPages
from kbot.library.library import Library

class TestHtmlPages:

    def test_fetch_html(self):
        kbot = KBot('wisteria')
        pages = HtmlPages()
        user = User(os.environ['USER1'])
        html = pages.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        pages.finalize()

