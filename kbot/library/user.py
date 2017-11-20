#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from kbot.book.common import BookFilter


class Users(object):
    def __init__(self, users):
        self._users = users

    @property
    def list(self):
        return self._users

    def filter(self, user_filter):
        if user_filter == BookFilter.FILTER_USERS_ALL:
            return

        new_users = []
        nums = user_filter.split(',')
        for num in nums:
            user_num = int(num)
            if 0 <= user_num < len(self._users):
                new_users.append(self._users[user_num])

        self._users = new_users


class User(object):
    def __init__(self, data_json):
        data = json.loads(data_json)

        self.num = data.get('num')
        self.name = data.get('name')
        self.id = data.get('id')
        self.password = data.get('password')
        self.rental_books_count = 0

    def set_rental_books(self, rental_books):
        rental_books.user = self
        self.rental_books = rental_books
        self.rental_books_count = rental_books.len

    def set_reserved_books(self, reserved_books):
        reserved_books.user = self
        self.reserved_books = reserved_books
        self.reserved_books_count = reserved_books.len
