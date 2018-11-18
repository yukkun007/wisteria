#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

from typing import List
from kbot.message import Message
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks


class User(object):

    TEMPLATE_ONE_USER_RESERVED_BOOKS: str = "one_user_reserved_books.tpl"

    def __init__(self, data_json: str) -> None:
        data = json.loads(data_json)

        self.num: str = data.get("num")
        self.name: str = data.get("name")
        self.id: str = data.get("id")
        self.password: str = data.get("password")
        self.rental_books_count: int = 0
        self.reserved_books_count: int = 0
        self.rental_books: RentalBooks = RentalBooks()
        self.reserved_books: ReservedBooks = ReservedBooks()

    def set_books(self, books_class_name: str, books) -> None:
        if books_class_name == "RentalBooks":
            self.__set_rental_books(books)
        elif books_class_name == "ReservedBooks":
            self.__set_reserved_books(books)

    def __set_rental_books(self, rental_books: RentalBooks) -> None:
        self.rental_books = rental_books
        self.rental_books_count = rental_books.len

    def __set_reserved_books(self, reserved_books: ReservedBooks) -> None:
        self.reserved_books = reserved_books
        self.reserved_books_count = reserved_books.len

    def get_rental_books_message(self, format: str = "text") -> str:
        message = ""
        date_keyed_books_dict = RentalBooks.get_date_keyed_books_dict(self.rental_books)
        data = {"user": self, "date_keyed_books_dict": date_keyed_books_dict}
        message += Message.create(os.path.join(format, RentalBooks.TEMPLATE_RENTAL_BOOKS), data)
        return message

    def get_reserved_books_message(self, format: str = "text") -> str:
        message = ""
        data = {"user": self, "is_prepared": self.reserved_books.is_prepared_reserved_book()}
        message += Message.create(os.path.join(format, ReservedBooks.TEMPLATE_RESERVED_BOOKS), data)

        return message

    def get_rental_and_reserved_books_message(self, format: str = "text") -> str:
        sub_message1 = ""
        sub_message1 += self.get_rental_books_message(format)
        sub_message2 = ""
        sub_message2 += self.get_reserved_books_message(format)

        message = ""
        data = {"sub_message1": sub_message1, "sub_message2": sub_message2}
        message += Message.create(os.path.join(format, User.TEMPLATE_ONE_USER_RESERVED_BOOKS), data)

        return message

    def is_prepared_reserved_book(self) -> bool:
        if self.reserved_books.is_prepared_reserved_book():
            return True
        return False


class Users(object):

    TEMPLATE_USER_RENTAL_BOOKS: str = "user_rental_books.tpl"
    TEMPLATE_USER_RESERVED_BOOKS: str = "user_reserved_books.tpl"

    def __init__(self, users: List[User]) -> None:
        self._users: List = users

    @property
    def list(self) -> List:
        return self._users

    def get(self, index: int) -> User:
        return self._users[index]

    def filter(self, user_filter: str):
        if user_filter == "all":  # BookFilter.FILTER_USERS_ALL:
            return self

        new_users = []
        nums = user_filter.split(",")
        for num in nums:
            user_num = int(num)
            if 0 <= user_num < len(self._users):
                new_users.append(self._users[user_num])

        return Users(new_users)

    def get_user_num(self, text: str) -> str:
        user_name = text[3:]
        filterd_users = list(filter(lambda user: user.name == user_name, self._users))
        if len(filterd_users) == 1:
            return filterd_users[0].num
        else:
            return "0"

    def is_rental_books_exist(self) -> bool:
        all_rental_books_count = 0
        for user in self._users:
            all_rental_books_count += user.rental_books_count
        if all_rental_books_count > 0:
            return True
        return False

    def get_check_books_text_message(self, books_kind: str) -> str:
        return self.__get_check_books_message(books_kind, format="text")

    def get_check_books_html_message(self, books_kind: str) -> str:
        return self.__get_check_books_message(books_kind, format="html")

    def __get_check_books_message(self, books_kind: str, format: str = "text") -> str:
        message = ""
        if books_kind == "RentalBooks":
            message = self.__get_all_users_rental_books_message(format=format)
        elif books_kind == "ReservedBooks":
            message = self.__get_all_users_reserved_books_message(format=format)
        return message

    def __get_all_users_rental_books_message(self, format: str = "text") -> str:
        sub_message = ""
        for user in self._users:
            sub_message += user.get_rental_books_message(format=format)

        message = ""
        data = {"sub_message": sub_message}
        message += Message.create(os.path.join(format, Users.TEMPLATE_USER_RENTAL_BOOKS), data)

        return message

    def __get_all_users_reserved_books_message(self, format: str = "text") -> str:
        sub_message = ""
        for user in self._users:
            sub_message += user.get_reserved_books_message(format=format)

        message = ""
        data = {"sub_message": sub_message, "is_prepared": self.__is_prepared_reserved_book()}
        message += Message.create(os.path.join(format, Users.TEMPLATE_USER_RESERVED_BOOKS), data)

        return message

    def __is_prepared_reserved_book(self) -> bool:
        for user in self._users:
            if user.reserved_books.is_prepared_reserved_book():
                return True
        return False
