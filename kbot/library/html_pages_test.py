#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_pages import HtmlPages

class TestHtmlPages:

    def test_fetch_html(self):
        kbot = KBot('wisteria')
        pages = HtmlPages()
        user = User(os.environ['USER1'])
        html = pages.fetch_html(user)
        pages.finalize()

