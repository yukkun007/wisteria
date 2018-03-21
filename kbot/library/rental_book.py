#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date, timedelta
from dateutil.parser import parse
from collections import defaultdict
from kbot.message import Message
from kbot.log import Log
from kbot.book.common import Books, BookFilter


class RentalBookFilter(BookFilter):

    _FILTER_RENTAL_PERIOD_NONE = 'none'
    _FILTER_RENTAL_PERIOD_EXPIRED = 'expired'
    _FILTER_RENTAL_PERIOD_EXPIRE = 'expire'

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(RentalBookFilter, self).__init__(users=users)
        self._rental_period = RentalBookFilter._FILTER_RENTAL_PERIOD_NONE
        self._books_class_name = 'RentalBooks'
        self._xdays = 2

    @property
    def xdays(self):
        return self._xdays

    @xdays.setter
    def xdays(self, xdays):
        raise ValueError()

    @property
    def is_type_none(self):
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_NONE

    @property
    def is_type_expired(self):
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRED

    @property
    def is_type_expire(self):
        return self._rental_period == RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRE


class RentalBookExpiredFilter(RentalBookFilter):
    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(RentalBookExpiredFilter, self).__init__(users=users)
        self._rental_period = RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRED


class RentalBookExpireFilter(RentalBookFilter):
    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL, xdays='2'):
        super(RentalBookExpireFilter, self).__init__(users=users)
        self._rental_period = RentalBookFilter._FILTER_RENTAL_PERIOD_EXPIRE
        self._xdays = self.__convert_xdays(xdays)

    def __convert_xdays(self, target):
        default = 2

        try:
            return int(target)
        except ValueError:
            try:
                index = target.find('日で延滞')
                num_str = target[index - 1:index + 4]
                num_str = num_str.replace('日で延滞', '')
                return int(num_str)
            except ValueError:
                return default


class RentalBooks(Books):

    TEMPLATE_RENTAL_BOOKS = 'rental_books.tpl'

    def __init__(self, source, filter_setting=RentalBookFilter()):
        super(RentalBooks, self).__init__(source)
        self._filter_setting = filter_setting

    @property
    def filter_setting(self):
        return self._filter_setting

    def get_message(self, format='text'):
        message = ''
        date_keyed_books_dict = RentalBooks.__get_date_keyed_books_dict(self._list)
        data = {'books': self,
                'date_keyed_books_dict': date_keyed_books_dict}
        message += Message.create(os.path.join(format,
                                               RentalBooks.TEMPLATE_RENTAL_BOOKS), data)
        return message

    def apply_filter(self, filter_setting):
        # books_list = books._list
        self._filter_setting = filter_setting
        if filter_setting.is_type_none:
            self._list = RentalBooks.__sort(self._list)
            # return RentalBooks(RentalBooks.__sort(books_list), filter_setting)
        elif filter_setting.is_type_expired:
            filterd_books = filter(
                lambda book: book.is_expired(), self._list)
            self._list = RentalBooks.__sort(filterd_books)
            # return RentalBooks(RentalBooks.__sort(filterd_books), filter_setting)
        elif filter_setting.is_type_expire:
            filterd_books = filter(
                lambda book: book.is_expire_in_xdays(
                    filter_setting.xdays), self._list)
            self._list = RentalBooks.__sort(filterd_books)
            # return RentalBooks(RentalBooks.__sort(filterd_books), filter_setting)

    def create_and_append(self, data):
        no = data[0].string.strip()
        # タイトル
        title = data[2].get_text().strip()
        # 返却期限日
        expire_date = data[7].get_text().strip()
        # 貸出更新
        can_extend_period = RentalBooks.__can_extend_period(
            data[1].get_text().strip())
        # 更新ボタンの名前
        extend_period_button_name = 'L(' + no + ')'

        rental_book = RentalBook(
            title,
            expire_date,
            can_extend_period,
            extend_period_button_name
        )

        self.append(rental_book)

    @classmethod
    def __can_extend_period(cls, text):
        if '更新' in text:
            return False
        return True

    @classmethod
    def __sort(cls, books_list):
        return sorted(books_list, key=lambda book: (book.expire_date, book.name))

    @classmethod
    def __get_date_keyed_books_dict(cls, books_list):
        date_keyed_books_dict = defaultdict(lambda: [])
        for book in books_list:
            date_keyed_books_dict[book.expire_date_text].append(book)
        return date_keyed_books_dict


class RentalBook(object):

    def __init__(
            self,
            name,
            expire_date_text,
            can_extend_period,
            extend_period_button_name):
        self.name = name
        self.expire_date = parse(expire_date_text).date()
        self.expire_date_text = expire_date_text
        self.can_extend_period = can_extend_period
        self.extend_period_button_name = extend_period_button_name

        Log.info(self.to_string())

    def is_expired(self):
        return self.is_expire_in_xdays(-1)

    def is_expire_in_xdays(self, xday_before):
        today = date.today()
        if self.expire_date - today <= timedelta(days=xday_before):
            return True
        return False

    def get_expire_text_from_today(self):
        today = date.today()
        remain_days = (self.expire_date - today).days

        if remain_days == 1:
            text = ' (明日ﾏﾃﾞ)'
        elif remain_days == 0:
            text = ' (今日ﾏﾃﾞ)'
        elif remain_days < 0:
            text = ' (延滞)'
        else:
            text = ' (あと{0}日)'.format(remain_days)

        return text

    def to_string(self):
        string = ('name:{0} expire_date:{1} expire_date(text):{2} '
                  'can_extend_period:{3} extend_period_button_name:{4}').format(
                      self.name,
                      self.expire_date,
                      self.expire_date_text,
                      self.can_extend_period,
                      self.extend_period_button_name)
        return string
