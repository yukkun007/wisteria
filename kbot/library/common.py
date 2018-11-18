# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from typing import List


class Books(object):
    def __init__(self) -> None:
        self._list: List = []

    @property
    def list(self) -> List:
        return self._list

    @list.setter
    def list(self, list: List) -> None:
        self._list = list

    @property
    def len(self) -> int:
        return len(self._list)

    def append(self, book) -> None:
        self._list.append(book)

    def get(self, index: int):
        return self._list[index]

    def slice(self, start: int, end: int) -> None:
        new_list = self._list[start:end]
        self.list = new_list

    def create_and_append(self, data):
        pass

    def apply_filter(self, filter_setting):
        pass


class BookFilter(object):

    FILTER_USERS_ALL: str = "all"

    def __init__(self, *, users: str = FILTER_USERS_ALL) -> None:
        self._users: str = users
        self._books_class_name: str = "Books"

    @property
    def users(self) -> str:
        return self._users

    @users.setter
    def users(self, users: str) -> None:
        raise ValueError()

    @property
    def books_class_name(self) -> str:
        return self._books_class_name

    @books_class_name.setter
    def books_class_name(self, books_class_name: str) -> None:
        raise ValueError()
