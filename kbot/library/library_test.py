#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.library import Library
from kbot.library.rental_book import FilterSetting, ExpireFilterSetting, ExpiredFilterSetting

class TestLibrary:

    @pytest.fixture()
    def instance1(request):
        kbot = KBot('wisteria')
        users = [User(os.environ['USER1'])]
        library = Library(users)
        return library

    def test_library_rental(self, instance1):
        instance1.fetch_status(FilterSetting())
        short_message = instance1.get_text_message(FilterSetting())
        print(short_message)

    def test_library_expired(self, instance1):
        instance1.fetch_status(ExpiredFilterSetting())
        short_message = instance1.get_text_message(ExpiredFilterSetting())
        print(short_message)

    def test_library_expire(self, instance1):
        xdays = 2
        instance1.fetch_status(ExpireFilterSetting(xdays))
        short_message = instance1.get_text_message(ExpireFilterSetting(xdays))
        print(short_message)

