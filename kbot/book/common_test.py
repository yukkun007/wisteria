# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import pytest
from kbot.book.common import Books, BookFilter, BookSearchQuery


class TestBooks:
    def test_init(self):
        source = None
        books = Books(source)
        assert books.list == []


class TestBookFilter:
    def test_users(self):
        filter = BookFilter()
        with pytest.raises(ValueError):
            filter.users = "test"


class TestBookSearchQuery:
    def test_query(self):
        query = BookSearchQuery()
        query.set("test", "hoge")
        assert query.dict().get("test") == "hoge"

    def test_get_from(self):
        query = BookSearchQuery.get_from("ほ？hoge")
        assert query.get("title") == "hoge"
