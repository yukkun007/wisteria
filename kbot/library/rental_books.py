#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.rental_book import RentalBook
from kbot.library.filter import Filter

class RentalBooks(object):

    def __init__(self):
        self.books  = []
        self.filter = Filter()

    def append(self, book):
        self.books.append(book)

    def length(self):
        return len(self.books)

    def list(self):
        return self.books

    def do_filter(self, books_filter):
        self.filter = books_filter
        if self.filter.type == Filter.FILTER_NONE:
            pass
        elif self.filter.type == Filter.FILTER_EXPIRED:
            filterd_books = filter(lambda book: book.is_expire_in_xdays(0), self.books)
            self.books    = filterd_books
            self.__sort()
        elif self.filter.type == Filter.FILTER_EXPIRE:
            filterd_books = filter(lambda book: book.is_expire_in_xdays(self.filter.xdays), self.books)
            self.books    = filterd_books
            self.__sort()

    def __sort(self):
        self.books = sorted(self.books, key=lambda book: (book.expire_date, book.name))

