#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.library.user import User, Users
from kbot.library.library import Library
from kbot.library.rental_book import RentalBookFilter, RentalBookExpireFilter, RentalBookExpiredFilter


class TestLibrary:

    def setup(self):
        KBot('wisteria')

    @pytest.fixture()
    def library1(request):
        users = Users([User(os.environ['USER1'])])
        return Library(users)

    def test_check_rental_books(self, library1):
        target_users = library1.check_rental_books(RentalBookFilter())
        short_message = target_users.get_rental_books_text_message()
        print(short_message)

    def test_check_rental_books_expired(self, library1):
        target_users = library1.check_rental_books(RentalBookExpiredFilter())
        short_message = target_users.get_rental_books_text_message()
        print(short_message)

    def test_check_rental_books_expire(self, library1):
        xdays = 2
        target_users = library1.check_rental_books(RentalBookExpireFilter(xdays=xdays))
        short_message = target_users.get_rental_books_text_message()
        print(short_message)
