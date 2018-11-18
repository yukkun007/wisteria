#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_page import HtmlPage
from kbot.library.library import Library


class TestHtmlPages:
    def setup(self):
        KBot("wisteria")

    @pytest.fixture()
    def html_page1(request):
        return HtmlPage()

    @pytest.mark.slow
    def test_fetch_login_page(self, html_page1):
        user = User(os.environ["USER1"])
        html_page1.fetch_login_page(Library.LIBRALY_HOME_URL, user)

    @patch("kbot.library.html_page.Select")
    def test_reserve(self, html_page1):
        html_page1.reserve(
            Library.LIBRALY_HOME_URL,
            User(os.environ["USER1"]),
            Library.LIBRALY_BOOK_URL.format("11111"),
        )
