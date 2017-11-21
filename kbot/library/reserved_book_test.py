#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.reserved_book import ReservedBook


class TestReservedBook:

    def test_basic(self):
        book = ReservedBook('status', '', 'title', 'kind', 'yoyaku_date', 'torioki_date')
        num = book._ReservedBook__get_order_num(' 1 / 10')
        assert num == 1
