#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.library.user import User, Users
from kbot.library.library import Library
from kbot.library.rental_book import RentalBookFilter, RentalBookExpireFilter, RentalBookExpiredFilter


class TestLibrary:

    @pytest.fixture()
    def instance1(request):
        KBot('wisteria')
        users = Users([User(os.environ['USER1'])])
        library = Library(users)
        return library

    def test_library_rental(self, instance1):
        instance1.check_rental_books(RentalBookFilter())
        short_message = instance1.get_text_message()
        print(short_message)

    def test_library_expired(self, instance1):
        instance1.check_rental_books(RentalBookExpiredFilter())
        short_message = instance1.get_text_message()
        print(short_message)

    def test_library_expire(self, instance1):
        xdays = 2
        instance1.check_rental_books(RentalBookExpireFilter(xdays=xdays))
        short_message = instance1.get_text_message()
        print(short_message)
