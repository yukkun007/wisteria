# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.book.common import BookSearchQuery


class TestBookSearchQuery:

    def test_query(self):
        query = BookSearchQuery()
        query.set('test', 'hoge')
        assert query.dict().get('test') == 'hoge'
