#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


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
