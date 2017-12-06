#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kbot.kbot import KBot


class TestKBot:

    def setup(self):
        pass

    @pytest.fixture()
    def kbot1(request):
        return KBot('wisteria')

    @pytest.fixture()
    def kbot2(request):
        return KBot('')

    def test_load_dotenv(self, kbot2):
        kbot2._KBot__load_dotenv()

    def test_kbot_commnad_menu(self, kbot1):
        kbot1.get_kbot_command_menu()

    def test_get_xdays(self, kbot1):
        value = kbot1.get_xdays('2日')
        assert value == 2

    def test_is_user_reserve_check_command(self, kbot1):
        assert kbot1.is_user_reserve_check_command('予約？hoge') is True

    def test_is_user_reserve_check_command_false(self, kbot1):
        assert kbot1.is_user_reserve_check_command('予約') is False

    def test_is_reserve_check_command(self, kbot1):
        assert kbot1.is_reserve_check_command('予約') is True

    def test_is_reserve_check_command_false(self, kbot1):
        assert kbot1.is_reserve_check_command('yoyaku') is False

    def test_is_user_rental_check_command(self, kbot1):
        assert kbot1.is_user_rental_check_command('図書？hoge') is True

    def test_is_user_rental_check_command_false(self, kbot1):
        assert kbot1.is_user_rental_check_command('図書') is False

    def test_is_rental_check_command(self, kbot1):
        assert kbot1.is_rental_check_command('図書館') is True

    def test_is_rental_check_command_false(self, kbot1):
        assert kbot1.is_rental_check_command('tyosyokan') is False

    def test_is_expired_check_command(self, kbot1):
        assert kbot1.is_expired_check_command('延滞') is True

    def test_is_expired_check_command_false(self, kbot1):
        assert kbot1.is_expired_check_command('entai') is False

    def test_is_expire_check_command(self, kbot1):
        assert kbot1.is_expire_check_command('7日で延滞') is True

    def test_is_expire_check_command_false(self, kbot1):
        assert kbot1.is_expire_check_command('7日　延滞') is False

    def test_is_reply_string_show_command(self, kbot1):
        assert kbot1.is_reply_string_show_command('文字') is True

    def test_is_reply_string_show_command_false(self, kbot1):
        assert kbot1.is_reply_string_show_command('moji') is False

    def test_is_search_book_command(self, kbot1):
        assert kbot1.is_search_book_command('本？hoge') is True

    def test_is_search_book_command_2(self, kbot1):
        assert kbot1.is_search_book_command('著？hoge') is True

    def test_is_search_book_command_false(self, kbot1):
        assert kbot1.is_search_book_command('？hoge') is False

    def test_is_search_library_book_command(self, kbot1):
        assert kbot1.is_search_library_book_command('ほ？hoge') is True

    def test_is_search_library_book_command_false(self, kbot1):
        assert kbot1.is_search_library_book_command('ho？hoge') is False

    def test_get_reply_string(self, kbot1):
        kbot1.get_reply_string()
