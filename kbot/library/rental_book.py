#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date, timedelta
from dateutil.parser import parse
from collections import defaultdict
from kbot.message import Message
from kbot.log import Log


class FilterSetting(object):

    FILTER_NONE = "none"
    FILTER_EXPIRED = "expired"
    FILTER_EXPIRE = "expire"

    def __init__(self):
        self.type = FilterSetting.FILTER_NONE
        self.xdays = -1


class ExpiredFilterSetting(FilterSetting):
    def __init__(self):
        self.type = FilterSetting.FILTER_EXPIRED
        self.xdays = -1


class ExpireFilterSetting(FilterSetting):
    def __init__(self, xdays):
        self.type = FilterSetting.FILTER_EXPIRE
        self.xdays = xdays


class RentalBooks(object):

    TEMPLATE_RENTAL = "rental.tpl"
    TEMPLATE_EXPIRED = "expired.tpl"
    TEMPLATE_EXPIRE = "expire.tpl"
    TEMPLATE_BOOK_LIST = "book_list.tpl"

    def __init__(self, source):
        if source is None:
            self.books = []
        else:
            self.books = source

    def append(self, book):
        self.books.append(book)

    def length(self):
        return len(self.books)

    def list(self):
        return self.books

    def get_filtered_books(self, filter_setting):
        if filter_setting.type == FilterSetting.FILTER_NONE:
            return RentalBooks(self.books)
        elif filter_setting.type == FilterSetting.FILTER_EXPIRED:
            filterd_books = filter(
                lambda book: book.is_expire_in_xdays(0), self.books)
            return RentalBooks(RentalBooks.__sort(filterd_books))
        elif filter_setting.type == FilterSetting.FILTER_EXPIRE:
            filterd_books = filter(
                lambda book: book.is_expire_in_xdays(
                    filter_setting.xdays), self.books)
            return RentalBooks(RentalBooks.__sort(filterd_books))

    @classmethod
    def __sort(cls, books):
        return sorted(books, key=lambda book: (book.expire_date, book.name))

    def get_text_message(self, user, filter_setting):
        return self.get_message(user, filter_setting, format='text')

    def get_html_message(self, user, filter_setting):
        return self.get_message(user, filter_setting, format='html')

    def get_message(self, user, filter_setting, format='text'):
        message = ''
        if self.length() > 0:
            data = {
                'user': user,
                'books_len': self.length(),
                'xdays': filter_setting.xdays}
            message += Message.create(
                RentalBooks.__get_template_path(
                    filter_setting, format), data)

            date_keyed_books_dict = self.__get_date_keyed_books_dict()
            data = {'date_keyed_books_dict': date_keyed_books_dict}
            message += Message.create(os.path.join(format,
                                                   RentalBooks.TEMPLATE_BOOK_LIST), data)
        return message

    @classmethod
    def __get_template_path(cls, filter_setting, format='text'):
        if filter_setting.type == FilterSetting.FILTER_NONE:
            template = RentalBooks.TEMPLATE_RENTAL
        elif filter_setting.type == FilterSetting.FILTER_EXPIRED:
            template = RentalBooks.TEMPLATE_EXPIRED
        elif filter_setting.type == FilterSetting.FILTER_EXPIRE:
            template = RentalBooks.TEMPLATE_EXPIRE
        return os.path.join(format, template)

    def __get_date_keyed_books_dict(self):
        date_keyed_books_dict = defaultdict(lambda: [])
        for book in self.books:
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
            text = " (延滞)"
        else:
            text = " (あと{0}日)".format(remain_days)

        return text

    def to_string(self):
        string = "name:{0} expire_date:{1} expire_date(text):{2} can_extend_period:{3} extend_period_button_name:{4}".format(
            self.name, self.expire_date, self.expire_date_text, self.can_extend_period, self.extend_period_button_name)
        return string
