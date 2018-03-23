# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.library.user import User


class Books(object):

    def __init__(self, source):
        self._user = User('{}')
        if source is None:
            self._list = []
        else:
            self._list = source

    @property
    def list(self):
        return self._list

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def len(self):
        return len(self._list)

    def append(self, book):
        self._list.append(book)

    def get(self, index):
        return self._list[index]

    def slice(self, start, end):
        return self.__class__(self._list[start:end])

    def create_and_append(self, data):
        pass

    def apply_filter(self, filter_setting):
        pass


class BookFilter(object):

    FILTER_USERS_ALL = 'all'

    def __init__(self, *, users=FILTER_USERS_ALL):
        self._users = users
        self._books_class_name = 'Books'

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, users):
        raise ValueError()

    @property
    def books_class_name(self):
        return self._books_class_name

    @books_class_name.setter
    def books_class_name(self, books_class_name):
        raise ValueError()


class BookSearchQuery(object):

    def __init__(self):
        self.query = {}

    def set(self, key, value):
        self.query[key] = value

    def get(self, key):
        return self.query.get(key)

    def dict(self):
        return self.query

    @classmethod
    def get_from(cls, text):
        query = BookSearchQuery()
        if '本？' in text:
            book_name = text[2:]
            query.set('title', book_name)
        elif '著？' in text:
            author = text[2:]
            query.set('author', author)
        elif 'ほ？' in text:
            book_name = text[2:]
            query.set('title', book_name)
        elif 'isbn' in text:
            isbn = text[5:]
            query.set('isbn', isbn)
        return query
