# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import pytest
from kbot.library.common import Books, BookFilter


class TestBooks:
    def test_init(self):
        books = Books()
        assert books.list == []


class TestBookFilter:
    def test_users(self):
        filter = BookFilter()
        with pytest.raises(ValueError):
            filter.users = "test"
