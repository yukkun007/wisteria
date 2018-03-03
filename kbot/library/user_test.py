#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import MagicMock
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

    def test_get_user_num_miss(self, users1):
        num = users1.get_user_num('図書？test3')
        assert num == '0'

    @pytest.fixture()
    def users2(request):
        user1 = MagicMock()
        user1.reserved_books.is_prepared_reserved_book.return_value = True
        user1.rental_books.get_message.return_value = 'this is test.'
        user1.rental_books_count = 5
        user1.reserved_books.get_message.return_value = 'this is test.'
        users = Users([
            user1
        ])
        return users

    def test_is_rental_books_exist_true(self, users2):
        assert users2.is_rental_books_exist() is True

    def test_is_rental_books_exist_false(self, users1):
        assert users1.is_rental_books_exist() is False

    def test_get_rental_books_html_message(self, users2):
        users2.get_rental_books_html_message()

    def test_get_reserved_books_html_message(self, users2):
        users2.get_reserved_books_html_message()

    def test_is_prepared_reserved_book_true(self, users2):
        assert users2._Users__is_prepared_reserved_book() is True

    @pytest.fixture()
    def users3(request):
        user1 = MagicMock()
        user1.reserved_books.is_prepared_reserved_book.return_value = False
        users = Users([
            user1
        ])
        return users

    def test_is_prepared_reserved_book_false(self, users3):
        assert users3._Users__is_prepared_reserved_book() is False


class TestUser:

    def setup(self):
        KBot('wisteria')

    def test_user(self):
        data_json = os.environ['USER_TEST']
        user = User(data_json)
        assert user.name == 'test'
