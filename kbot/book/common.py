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

    @classmethod
    def get_from(cls, text):
        query = BookSearchQuery()
        if '本？' in text:
            book_name = text[2:]
            query.set('title', book_name)
        elif '著？' in text:
            author = text[2:]
            query.set('author', author)
        elif 'isbn' in text:
            isbn = text[5:]
            query.set('isbn', isbn)
        return query
