#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch, MagicMock
from kbot.kbot import KBot
from kbot.library.html_page import HtmlPage
from kbot.library.user import User, Users
from kbot.library.library import Library
from kbot.library.rental_book import (
    RentalBookFilter,
    RentalBookExpireFilter,
    RentalBookExpiredFilter,
)


class TestLibrary:
    def setup(self):
        KBot("wisteria")

    @pytest.fixture()
    def library1(request):
        users = Users([User(os.environ["USER1"])])
        return Library(users)

    def test_check_rental_books(self, library1):
        config = RentalBookFilter()
        target_users = library1.check_books(config)
        short_message = target_users.get_check_books_text_message(config.books_class_name)
        print(short_message)

    def test_check_books_expired(self, library1):
        config = RentalBookExpiredFilter()
        target_users = library1.check_books(config)
        short_message = target_users.get_check_books_text_message(config.books_class_name)
        print(short_message)

    def test_check_books_expire(self, library1):
        xdays = 2
        config = RentalBookExpireFilter(xdays=xdays)
        target_users = library1.check_books(config)
        short_message = target_users.get_check_books_text_message(config.books_class_name)
        print(short_message)

    def test_reserve(self, library1):
        mock = MagicMock(spec=HtmlPage)
        with patch("kbot.library.library.HtmlPage", mock):
            instance = mock.return_value
            instance.reserve.return_value = None
            library1.reserve("0", "11111")
            instance.reserve.assert_called_once()
