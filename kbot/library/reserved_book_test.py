#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kbot.kbot import KBot
from kbot.library.reserved_book import ReservedBooks, ReservedBook


class TestReservedBooks:
    @pytest.fixture()
    def books1(request):
        KBot("wisteria")
        return ReservedBooks()

    def test_is_prepared_reserved_book_true(self, books1):
        book = ReservedBook("ご用意できました", "", "title", "kind", "yoyaku_date", "torioki_date")
        books1.append(book)
        assert books1.is_prepared_reserved_book() is True

    def test_is_prepared_reserved_book_false(self, books1):
        book = ReservedBook("status", "", "title", "kind", "yoyaku_date", "torioki_date")
        books1.append(book)
        assert books1.is_prepared_reserved_book() is False


class TestReservedBook:
    def test_basic(self):
        book = ReservedBook("status", "", "title", "kind", "yoyaku_date", "torioki_date")
        num = book._ReservedBook__get_order_num(" 1 / 10")
        assert num == 1

    def test_is_prepared_true(self):
        assert ReservedBook._ReservedBook__is_prepared("ご用意できました") is True

    def test_is_prepared_false(self):
        assert ReservedBook._ReservedBook__is_prepared("status") is False

    def test_is_dereverd_true(self):
        assert ReservedBook._ReservedBook__is_dereverd("移送中です") is True

    def test_is_dereverd_false(self):
        assert ReservedBook._ReservedBook__is_dereverd("status") is False

    def test_make_finish_reserve_message_template(self):
        ReservedBook.make_finish_reserve_message_template("1")
