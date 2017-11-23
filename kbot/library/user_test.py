#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.library.user import User, Users


class TestUsers:

    def setup(self):
        KBot('wisteria')

    @pytest.fixture()
    def users1(request):
        users = Users([
            User(os.environ['USER_TEST']),
            User(os.environ['USER_TEST2'])
        ])
        return users

    def test_users(self, users1):
        new_users = users1.filter('1')
        for user in new_users.list:
            assert user.name == 'test2'

    def test_get_user_num(self, users1):
        num = users1.get_user_num('図書？test2')
        assert num == '1'


class TestUser:

    def test_user(self):
        KBot('wisteria')

        data_json = os.environ['USER_TEST']
        user = User(data_json)
        assert user.name == 'test'
