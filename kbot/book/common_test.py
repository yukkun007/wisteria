# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.book.common import BookSearchQuery, BookSearchQueryFactory


class TestBookSearchQuery:
    def test_query(self):
        query = BookSearchQuery()
        query.set("test", "hoge")
        assert query.dict().get("test") == "hoge"


class TestBookSearchQueryFactory:
    def test_create_hon(self):
        query = BookSearchQueryFactory.create("本？坊っちゃん")
        assert query.get("title") == "坊っちゃん"

    def test_create_cyo(self):
        query = BookSearchQueryFactory.create("著？夏目漱石")
        assert query.get("author") == "夏目漱石"

    def test_create_ho(self):
        query = BookSearchQueryFactory.create("ほ？坊っちゃん")
        assert query.get("title") == "坊っちゃん"

    def test_create_isbn(self):
        query = BookSearchQueryFactory.create("isbn:11111111")
        assert query.get("isbn") == "11111111"
