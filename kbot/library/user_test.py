#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User


class TestUser:

    def test_user(self):
        KBot('wisteria')

        data_json = os.environ['USER_TEST']
        user = User(data_json)
        assert user.name == 'test'
