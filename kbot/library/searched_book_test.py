#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kbot.kbot import KBot
from kbot.library.searched_book import SearchedBooks, SearchedBook


class TestSearchedBooks:

    def setup(self):
        KBot('wisteria')

    @pytest.fixture()
    def books1(request):
        source = None
        return SearchedBooks(source)

    def test(self, books1):
        pass


class TestSearchedBook:

    def setup(self):
        KBot('wisteria')

    @pytest.fixture()
    def book1(request):
        return SearchedBook('title', 'author', 'publisher', 'publish_date')

    def test(self, book1):
        pass
