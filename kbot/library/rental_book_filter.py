#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from kbot.library.common import BookFilter


class RentalBookFilter(BookFilter):

    _FILTER_RENTAL_PERIOD_NONE: str = "none"
    _FILTER_RENTAL_PERIOD_EXPIRED: str = "expired"
    _FILTER_RENTAL_PERIOD_EXPIRE: str = "expire"

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL) -> None:
        super(RentalBookFilter, self).__init__(users=users)
        self._rental_period: str = RentalBookFilter._FILTER_RENTAL_PERIOD_NONE
        self._books_class_name: str = "RentalBooks"
        self._xdays: int = 2

    @property
    def xdays(self) -> int:
        return self._xdays

    @xdays.setter
    def xdays(self, xdays: int) -> None:
        raise ValueError()

    @property
    def is_type_none(self) -> bool:
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_NONE

    @property
    def is_type_expired(self) -> bool:
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRED

    @property
    def is_type_expire(self) -> bool:
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRE

    def execute(self, rental_books) -> None:
        rental_books.list = self.sort(rental_books.list)

    def sort(self, rental_book_list: List) -> List:
        new_rental_book_list = sorted(
            rental_book_list, key=lambda book: (book.expire_date, book.name)
        )
        return new_rental_book_list


class RentalBookExpiredFilter(RentalBookFilter):
    def __init__(self, *, users: str = BookFilter.FILTER_USERS_ALL) -> None:
        super(RentalBookExpiredFilter, self).__init__(users=users)
        self._rental_period: str = RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRED

    def execute(self, rental_books) -> None:
        filterd_books = list(filter(lambda book: book.is_expired(), rental_books.list))
        rental_books.list = self.sort(filterd_books)


class RentalBookExpireFilter(RentalBookFilter):
    def __init__(self, *, users: str = BookFilter.FILTER_USERS_ALL, xdays: str = "2") -> None:
        super(RentalBookExpireFilter, self).__init__(users=users)
        self._rental_period: str = RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRE
        self._xdays: int = self.__convert_xdays(xdays)

    def execute(self, rental_books) -> None:
        filterd_books = list(
            filter(lambda book: book.is_expire_in_xdays(self.xdays), rental_books.list)
        )
        rental_books.list = self.sort(filterd_books)

    def __convert_xdays(self, target: str) -> int:
        default = 2

        try:
            return int(target)
        except ValueError:
            try:
                index = target.find("日で延滞")
                num_str = target[index - 1 : index + 4]
                num_str = num_str.replace("日で延滞", "")
                return int(num_str)
            except ValueError:
                return default
