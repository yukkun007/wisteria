#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date, timedelta
from dateutil.parser import parse
from collections import defaultdict
from kbot.message import Message
from kbot.log import Log
from kbot.book.common import Books


class FilterSetting(object):

    _FILTER_NONE = 'none'
    _FILTER_EXPIRED = 'expired'
    _FILTER_EXPIRE = 'expire'

    def __init__(self, xdays=-1):
        self._type = FilterSetting._FILTER_NONE
        self._xdays = xdays

    @property
    def xdays(self):
        return self._xdays

    @xdays.setter
    def xdays(self, xdays):
        raise ValueError()

    @property
    def is_type_none(self):
        return self._type == FilterSetting._FILTER_NONE

    @property
    def is_type_expired(self):
        return self._type == FilterSetting._FILTER_EXPIRED

    @property
    def is_type_expire(self):
        return self._type == FilterSetting._FILTER_EXPIRE


class ExpiredFilterSetting(FilterSetting):
    def __init__(self, xdays=-1):
        super(ExpiredFilterSetting, self).__init__(xdays)
        self._type = FilterSetting._FILTER_EXPIRED


class ExpireFilterSetting(FilterSetting):
    def __init__(self, xdays=-1):
        super(ExpireFilterSetting, self).__init__(xdays)
        self._type = FilterSetting._FILTER_EXPIRE


class RentalBooks(Books):

    TEMPLATE_RENTAL_BOOKS = 'rental_books.tpl'

    def __init__(self, source, filter_setting=FilterSetting()):
        super(RentalBooks, self).__init__(source)
        self._filter_setting = filter_setting

    @property
    def filter_setting(self):
        return self._filter_setting

    def get_message(self, format='text'):
        message = ''
        if self.len > 0:
            date_keyed_books_dict = RentalBooks.__get_date_keyed_books_dict(self._books)
            data = {'books': self,
                    'date_keyed_books_dict': date_keyed_books_dict}
            message += Message.create(os.path.join(format,
                                                   RentalBooks.TEMPLATE_RENTAL_BOOKS), data)
        return message

    @classmethod
    def get_filtered_books(cls, books, filter_setting):
        books_list = books._books
        if filter_setting.is_type_none:
            return RentalBooks(books_list)
        elif filter_setting.is_type_expired:
            filterd_books = filter(
                lambda book: book.is_expire_in_xdays(0), books_list)
            return RentalBooks(RentalBooks.__sort(filterd_books), filter_setting)
        elif filter_setting.is_type_expire:
            filterd_books = filter(
                lambda book: book.is_expire_in_xdays(
                    filter_setting.xdays), books_list)
            return RentalBooks(RentalBooks.__sort(filterd_books), filter_setting)

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
