# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from typing import Dict


class BookSearchQuery(object):
    def __init__(self) -> None:
        self.query: Dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self.query[key] = value

    def get(self, key: str) -> str:
        return self.query.get(key, "")

    def dict(self) -> Dict[str, str]:
        return self.query


class BookSearchQueryFactory(object):
    @classmethod
    def create(cls, text: str) -> BookSearchQuery:
        query = BookSearchQuery()
        if "本？" in text:
            book_name = text[2:]
            query.set("title", book_name)
        elif "著？" in text:
            author = text[2:]
            query.set("author", author)
        elif "ほ？" in text:
            book_name = text[2:]
            query.set("title", book_name)
        elif "ちょ？" in text:
            author = text[3:]
            query.set("author", author)
        elif "isbn" in text:
            isbn = text[5:]
            query.set("isbn", isbn)
        return query
