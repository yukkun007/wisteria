#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from datetime import date, timedelta
from kbot.library.rental_book import RentalBook, RentalBooks
from kbot.library.rental_book_filter import RentalBookExpiredFilter, RentalBookExpireFilter


class TestRentalBooks:
    def test_basic(self):
        books = RentalBooks([])
        books.append(RentalBook("test1", "2017/01/01", True, "hoge"))
        books.append(RentalBook("test2", "9999/01/02", True, "hoge"))
        assert books.len == 2

    def test_filter_to_rental_books_expired(self):
        books = RentalBooks([])
        book = RentalBook("test1", "2017/01/01", True, "hoge")
        books.append(book)
        books.append(RentalBook("test2", "9999/01/02", True, "hoge"))
        books.append(RentalBook("test3", "9999/01/07", True, "hoge"))
        books.apply_filter(RentalBookExpiredFilter())
        assert books.len == 1
        assert books.get(0) == book  # メモリ比較

    def test_filter_to_rental_books_expire_in_xdays(self):
        books = RentalBooks([])
        book = RentalBook("test1", "2017/01/02", True, "hoge")
        books.append(book)
        books.append(RentalBook("test2", "2017/01/03", True, "hoge"))
        books.append(RentalBook("test3", "2017/01/05", True, "hoge"))
        books.apply_filter(RentalBookExpireFilter(xdays="5"))
        assert books.len == 3
        assert books.get(0) == book  # メモリ比較

    def test_sort(self):
        books = RentalBooks([])
        books.append(RentalBook("test3", "2017/01/05", True, "hoge"))
        books.append(RentalBook("test1", "2017/01/03", True, "hoge"))
        book = RentalBook("test1", "2017/01/02", True, "hoge")
        books.append(book)
        books.apply_filter(RentalBookExpireFilter(xdays="5"))
        assert books.len == 3
        assert books.get(0) == book  # メモリ比較


class TestRentalBook:
    def test_is_expired_true(self):
        book = RentalBook("test", "2017/01/01", True, "hoge")
        assert book.is_expired()

    def test_is_expired_false(self):
        book = RentalBook("test", "9999/01/1", False, "hoge")
        assert book.is_expired() is False

    @pytest.mark.parametrize("delta, result", [(-1, True), (1, False), (0, False)])
    def test_is_expired(self, delta, result):
        d = date.today() + timedelta(days=delta)
        book = RentalBook("test", d.strftime("%Y/%m/%d"), True, "hoge")
        assert book.is_expired() is result

    # -日前：期限切れの本
    # 返却0日前：返却日まで1日切ってる本：今日が返却日
    # 返却1日前：返却日まで2日切ってる本：今日・明日が返却日
    # 返却2日前：返却日まで3日切ってる本：今日・明日・明後日が返却日
    # 返却3日前：返却日まで4日切ってる本：今日・明日・明後日・明々後日が返却日
    # 返却4日前：返却日まで5日切ってる本

    @pytest.mark.parametrize(
        "delta, xdays, result",
        [(2, 3, True), (3, 3, True), (0, 0, True), (0, 3, True), (5, 3, False)],
    )
    def test_is_expire_in_xdays(self, delta, xdays, result):
        d = date.today() + timedelta(days=delta)
        book = RentalBook("test", d.strftime("%Y/%m/%d"), True, "hoge")
        assert book.is_expire_in_xdays(xdays) is result

    @pytest.mark.parametrize(
        "delta, expected_text", [(5, " (あと5日)"), (0, " (今日ﾏﾃﾞ)"), (1, " (明日ﾏﾃﾞ)"), (-5, " (延滞)")]
    )
    def test_get_expire_text_from_today(self, delta, expected_text):
        d = date.today() + timedelta(days=delta)
        book = RentalBook("test", d.strftime("%Y/%m/%d"), True, "hoge")
        assert book.get_expire_text_from_today() == expected_text
