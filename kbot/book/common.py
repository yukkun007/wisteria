# -*- coding: utf-8 -*-
# from __future__ import unicode_literals


class BookSearchQuery(object):

    def __init__(self):
        self.query = {}

    def set(self, key, value):
        self.query[key] = value

    def get(self, key):
        return self.query.get(key)

    def dict(self):
        return self.query
