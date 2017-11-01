# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.book.book import Book


class Amazon(object):

    def __init__(self):
        pass

    def get_book(self, isbn):
        json = {}
        book = Book(json)
        return book
