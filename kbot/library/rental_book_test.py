#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from kbot.library.rental_book import ExpireFilterSetting, ExpiredFilterSetting, RentalBook, RentalBooks


class TestRentalBooks:

    def test_basic(self):
        books = RentalBooks([])
        books.append(RentalBook('test1', '2017/01/01', True, 'hoge'))
        books.append(RentalBook('test2', '9999/01/02', True, 'hoge'))
        assert books.length() == 2
        assert len(books.list()) == 2

    def test_filter_to_rental_books_expired(self):
        books = RentalBooks([])
        book = RentalBook('test1', '2017/01/01', True, 'hoge')
        books.append(book)
        books.append(RentalBook('test2', '9999/01/02', True, 'hoge'))
        books.append(RentalBook('test3', '9999/01/07', True, 'hoge'))
        books = books.get_filtered_books(ExpiredFilterSetting())
        assert books.length() == 1
        assert books.list()[0] == book  # メモリ比較

    def test_filter_to_rental_books_expire_in_xdays(self):
        books = RentalBooks([])
        book = RentalBook('test1', '2017/01/02', True, 'hoge')
        books.append(book)
        books.append(RentalBook('test2', '2017/01/03', True, 'hoge'))
        books.append(RentalBook('test3', '2017/01/05', True, 'hoge'))
        books = books.get_filtered_books(ExpireFilterSetting(5))
        assert books.length() == 3
        assert books.list()[0] == book  # メモリ比較

    def test_sort(self):
        books = RentalBooks([])
        books.append(RentalBook('test3', '2017/01/05', True, 'hoge'))
        books.append(RentalBook('test1', '2017/01/03', True, 'hoge'))
        book = RentalBook('test1', '2017/01/02', True, 'hoge')
        books.append(book)
        books = books.get_filtered_books(ExpireFilterSetting(5))
        assert books.length() == 3
        assert books.list()[0] == book  # メモリ比較


class TestRentalBook:

    def test_is_expired_true(self):
        book = RentalBook('test', '2017/01/01', True, 'hoge')
        assert book.is_expired()

    def test_is_expired_false(self):
        book = RentalBook('test', '9999/01/1', False, 'hoge')
        assert book.is_expired() == False

    def test_is_expired_true_one_day_before(self):
        d = date.today() - timedelta(days=1)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expired()

    def test_is_expired_false_one_day_after(self):
        d = date.today() + timedelta(days=1)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expired() == False

    def test_is_expired_false_today(self):
        d = date.today()
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expired() == False

    # -日前：期限切れの本
    # 返却0日前：返却日まで1日切ってる本：今日が返却日
    # 返却1日前：返却日まで2日切ってる本：今日・明日が返却日
    # 返却2日前：返却日まで3日切ってる本：今日・明日・明後日が返却日
    # 返却3日前：返却日まで4日切ってる本：今日・明日・明後日・明々後日が返却日
    # 返却4日前：返却日まで5日切ってる本

    def test_is_expire_in_xdays_true(self):
        d = date.today() + timedelta(days=2)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expire_in_xdays(3)

    def test_is_expire_in_xdays_true_same_day(self):
        d = date.today() + timedelta(days=3)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expire_in_xdays(3)

    def test_is_expire_in_xdays_true_today(self):
        d = date.today()
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expire_in_xdays(0)

    def test_is_expire_in_xdays_true_today2(self):
        d = date.today()
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expire_in_xdays(3)

    def test_is_expire_in_xdays_false(self):
        d = date.today() + timedelta(days=5)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.is_expire_in_xdays(3) == False

    def test_get_expire_text_from_today(self):
        d = date.today() + timedelta(days=5)
        book = RentalBook('test', d.strftime('%Y/%m/%d'), True, 'hoge')
        assert book.get_expire_text_from_today() == ' (あと5日)'
