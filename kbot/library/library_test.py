#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.library import Library
from kbot.library.message import Message
from kbot.library.filter import Filter

class TestLibrary:

    @pytest.fixture()
    def instance1(request):
        kbot = KBot('wisteria')
        users = [User(os.environ['USER1'])]
        library = Library('wisteria/templates/kbot/', users)
        library.fetch_status()
        return library

    def test_library_rental(self, instance1):
        instance1.do_filter(Filter(type=Filter.FILTER_NONE, xdays=-1))
        short_message = instance1.get_message(type=Message.TYPE_SHORT)
        print(short_message)

    def test_library_expired(self, instance1):
        instance1.do_filter(Filter(type=Filter.FILTER_EXPIRED, xdays=-1))
        short_message = instance1.get_message(type=Message.TYPE_SHORT)
        print(short_message)

    def test_library_expire(self, instance1):
        xdays = 2
        instance1.do_filter(Filter(type=Filter.FILTER_EXPIRE, xdays=xdays))
        short_message = instance1.get_message(type=Message.TYPE_SHORT)
        print(short_message)

