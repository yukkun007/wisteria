#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.library.user import User, Users


class TestUsers:

    def test_users(self):
        KBot('wisteria')

        data_json = os.environ['USER_TEST']
        users = Users([
            User(data_json)
        ])
        for user in users.list:
            assert user.name == 'test'
        users.filter('1')
        for user in users.list:
            assert user.name == 'test2'


class TestUser:

    def test_user(self):
        KBot('wisteria')

        data_json = os.environ['USER_TEST']
        user = User(data_json)
        assert user.name == 'test'
