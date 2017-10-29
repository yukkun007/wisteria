#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class User(object):
    def __init__(self, data_json):
        data = json.loads(data_json)

        self.num                = data['num']
        self.name               = data['name']
        self.id                 = data['id']
        self.password           = data['password']
        self.rental_books_count = 0

    def set_rental_books(self, rental_books):
        self.rental_books       = rental_books
        self.rental_books_count = rental_books.length()

    def set_reserved_books(self, reserved_books):
        self.reserved_books       = reserved_books
        self.reserved_books_count = reserved_books.length()

