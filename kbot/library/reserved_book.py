# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot.models import ButtonsTemplate,\
    PostbackTemplateAction
from kbot.message import Message
from kbot.book.common import Books, BookFilter
from kbot.log import Log


class ReservedBookFilter(BookFilter):

    _FILTER_RESERVED_PREPARED_NONE = 'none'
    _FILTER_RESERVED_PREPARED_YES_AND_DEREVERD = 'yes_and_dereverd'

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_NONE

    @property
    def almost_prepared(self):
        return self._prepared == ReservedBookFilter._FILTER_RESERVED_PREPARED_YES_AND_DEREVERD


class ReservedBookPreparedFilter(ReservedBookFilter):

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookPreparedFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_YES_AND_DEREVERD


class ReservedBooks(Books):

    TEMPLATE_RESERVED_BOOKS = 'reserved_books.tpl'

    def __init__(self, source):
        super(ReservedBooks, self).__init__(source)

    def get_message(self, format='text'):
        message = ''
        data = {'books': self,
                'is_prepared': self.is_prepared_reserved_book()}
        message += Message.create(os.path.join(format,
                                               ReservedBooks.TEMPLATE_RESERVED_BOOKS), data)

        return message

    def is_prepared_reserved_book(self):
        for book in self._books:
            if book.status == 'ご用意できました':
                return True
        return False

    @classmethod
    def get_filtered_books(cls, books, filter_setting):
        books_list = books._books
        if filter_setting.almost_prepared:
            filterd_books = filter(
                lambda book: book.is_prepared or book.is_dereverd, books_list)
            return ReservedBooks(ReservedBooks.__sort(filterd_books))
        else:
            return ReservedBooks(ReservedBooks.__sort(books_list))

    @classmethod
    def __sort(cls, books_list):
        return sorted(books_list, key=lambda book: (book.order_num, book.status))


class ReservedBook(object):

    def __init__(self, status, order, title, kind, yoyaku_date, torioki_date):
        self.status = status
        self.order = order
        self.order_num = self.__get_order_num(order)
        self.title = title
        self.kind = kind
        self.yoyaku_date = yoyaku_date
        self.torioki_date = torioki_date
        self.is_prepared = ReservedBook.__is_prepared(status)
        self.is_dereverd = ReservedBook.__is_dereverd(status)

        Log.info(self.to_string())

    def to_string(self):
        string = ('status:{0} order:{1} title:{2} '
                  'kind:{3} yoyaku_date:{4}').format(
                      self.status,
                      self.order,
                      self.title,
                      self.kind,
                      self.yoyaku_date)
        return string

    @classmethod
    def __is_prepared(cls, status):
        if status == 'ご用意できました':
            return True
        return False

    @classmethod
    def __is_dereverd(cls, status):
        if status == '移送中です':
            return True
        return False

    def __get_order_num(self, order):
        try:
            return int(order.split('/')[0])
        except ValueError:
            return 0

    def make_finish_reserve_message_template(user_num):
        buttons_template = ButtonsTemplate(
            title='予約完了',
            text='予約できました。',
            actions=[
                PostbackTemplateAction(label='予約状況確認',
                                       data='check_reserve:' + user_num),
                PostbackTemplateAction(label='予約状況確認(全員分)',
                                       data='check_reserve:all')
            ]
        )
        return buttons_template
