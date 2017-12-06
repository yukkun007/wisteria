#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.reserved_book import ReservedBooks, ReservedBook


class TestReservedBooks:

    def test_is_prepared_reserved_book(self):
        book = ReservedBook('ご用意できました', '', 'title', 'kind', 'yoyaku_date', 'torioki_date')
        books = ReservedBooks(None)
        books.append(book)
        assert books.is_prepared_reserved_book() is True


class TestReservedBook:

    def test_basic(self):
        book = ReservedBook('status', '', 'title', 'kind', 'yoyaku_date', 'torioki_date')
        num = book._ReservedBook__get_order_num(' 1 / 10')
        assert num == 1
