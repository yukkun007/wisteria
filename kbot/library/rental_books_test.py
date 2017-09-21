#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.rental_book import RentalBook
from kbot.library.rental_books import RentalBooks
from kbot.library.filter import Filter

class TestRentalBooks:

    def test_basic(self):
        books = RentalBooks()
        books.append(RentalBook("test1", "2017/01/01", True, "hoge"))
        books.append(RentalBook("test2", "9999/01/02", True, "hoge"))
        assert books.length() == 2
        assert len(books.list()) == 2

    def test_filter_to_rental_books_expired(self):
        books = RentalBooks()
        book = RentalBook("test1", "2017/01/01", True, "hoge")
        books.append(book)
        books.append(RentalBook("test2", "9999/01/02", True, "hoge"))
        books.append(RentalBook("test3", "9999/01/07", True, "hoge"))
        books.do_filter(Filter(Filter.FILTER_EXPIRED))
        assert books.length() == 1
        assert books.list()[0] == book # メモリ比較

    def test_filter_to_rental_books_expire_in_xdays(self):
        books = RentalBooks()
        book = RentalBook("test1", "2017/01/02", True, "hoge")
        books.append(book)
        books.append(RentalBook("test2", "2017/01/03", True, "hoge"))
        books.append(RentalBook("test3", "2017/01/05", True, "hoge"))
        books.do_filter(Filter(Filter.FILTER_EXPIRE, 5))
        assert books.length() == 3
        assert books.list()[0] == book # メモリ比較

    def test_sort(self):
        books = RentalBooks()
        books.append(RentalBook("test3", "2017/01/05", True, "hoge"))
        books.append(RentalBook("test1", "2017/01/03", True, "hoge"))
        book = RentalBook("test1", "2017/01/02", True, "hoge")
        books.append(book)
        books.do_filter(Filter(Filter.FILTER_EXPIRE, 5))
        assert books.length() == 3
        assert books.list()[0] == book # メモリ比較

