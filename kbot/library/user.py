#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from kbot.message import Message
# from kbot.book.common import BookFilter


class Users(object):

    TEMPLATE_USER_RENTAL_BOOKS = 'user_rental_books.tpl'
    TEMPLATE_USER_RESERVED_BOOKS = 'user_reserved_books.tpl'

    def __init__(self, users):
        self._users = users

    @property
    def list(self):
        return self._users

    def get(self, index):
        return self._users[index]

    def filter(self, user_filter):
        if user_filter == 'all':  # BookFilter.FILTER_USERS_ALL:
            return self

        new_users = []
        nums = user_filter.split(',')
        for num in nums:
            user_num = int(num)
            if 0 <= user_num < len(self._users):
                new_users.append(self._users[user_num])

        return Users(new_users)

    def get_user_num(self, text):
        user_name = text[3:]
        filterd_users = list(filter(lambda user: user.name == user_name, self._users))
        if len(filterd_users) == 1:
            return filterd_users[0].num
        else:
            return '0'

    def is_rental_books_exist(self):
        all_rental_books_count = 0
        for user in self._users:
            all_rental_books_count += user.rental_books_count
        if all_rental_books_count > 0:
            return True
        return False

    def get_rental_books_text_message(self):
        return self.__get_rental_books_message(format='text')

    def get_rental_books_html_message(self):
        return self.__get_rental_books_message(format='html')

    def __get_rental_books_message(self, format='text'):
        sub_message = ''
        for user in self._users:
            sub_message += user.rental_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message}
        message += Message.create(os.path.join(format,
                                               Users.TEMPLATE_USER_RENTAL_BOOKS), data)

        return message

    def get_reserved_books_text_message(self):
        return self.__get_reserved_books_message(format='text')

    def get_reserved_books_html_message(self):
        return self.__get_reserved_books_message(format='html')

    def __get_reserved_books_message(self, format='text'):
        sub_message = ''
        for user in self._users:
            sub_message += user.reserved_books.get_message(format)

        message = ''
        data = {'sub_message': sub_message,
                'is_prepared': self.__is_prepared_reserved_book()}
        message += Message.create(os.path.join(format,
                                               Users.TEMPLATE_USER_RESERVED_BOOKS), data)

        return message

    def __is_prepared_reserved_book(self):
        for user in self._users:
            if user.reserved_books.is_prepared_reserved_book():
                return True
        return False


class User(object):

    TEMPLATE_ONE_USER_RESERVED_BOOKS = 'one_user_reserved_books.tpl'

    def __init__(self, data_json):
        data = json.loads(data_json)

        self.num = data.get('num')
        self.name = data.get('name')
        self.id = data.get('id')
        self.password = data.get('password')
        self.rental_books_count = 0
        self.reserved_books_count = 0
        self.rental_books = None
        self.reserved_books = None

    def set_books(self, books_class_name, books):
        if books_class_name == 'RentalBooks':
            self.__set_rental_books(books)
        elif books_class_name == 'ReservedBooks':
            self.__set_reserved_books(books)

    def __set_rental_books(self, rental_books):
        rental_books.user = self
        self.rental_books = rental_books
        self.rental_books_count = rental_books.len

    def __set_reserved_books(self, reserved_books):
        reserved_books.user = self
        self.reserved_books = reserved_books
        self.reserved_books_count = reserved_books.len

    def get_rental_and_reserved_books_message(self, format='text'):
        sub_message1 = ''
        sub_message1 += self.rental_books.get_message(format)
        sub_message2 = ''
        sub_message2 += self.reserved_books.get_message(format)

        message = ''
        data = {'sub_message1': sub_message1,
                'sub_message2': sub_message2}
        message += Message.create(os.path.join(format,
                                               User.TEMPLATE_ONE_USER_RESERVED_BOOKS), data)

        return message

    def is_prepared_reserved_book(self):
        if self.reserved_books.is_prepared_reserved_book():
            return True
        return False
