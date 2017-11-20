# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot.models import ButtonsTemplate,\
    PostbackTemplateAction
from kbot.message import Message
from kbot.book.common import Books, BookFilter


class ReservedBookFilter(BookFilter):

    _FILTER_RESERVED_PREPARED_NONE = 'none'
    _FILTER_RESERVED_PREPARED_YES = 'yes'

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_NONE

    @property
    def prepared(self):
        return self._prepared == ReservedBookFilter._FILTER_RESERVED_PREPARED_YES


class ReservedBookPreparedFilter(ReservedBookFilter):
    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookPreparedFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_YES


class ReservedBooks(Books):

    TEMPLATE_RESERVED_BOOKS = 'reserved_books.tpl'

    def __init__(self, source):
        super(ReservedBooks, self).__init__(source)

    def get_message(self, format='text'):
        message = ''
        if self.len > 0:
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
        if filter_setting.prepared:
            filterd_books = filter(
                lambda book: book.is_prepared(), books_list)
            return ReservedBooks(ReservedBooks.__sort(filterd_books))
        else:
            return ReservedBooks(ReservedBooks.__sort(books))

    @classmethod
    def __sort(cls, books_list):
        return sorted(books_list, key=lambda book: (book.order, book.title))


class ReservedBook(object):

    def __init__(self, status, order, title, kind, yoyaku_date, torioki_date):
        self.status = status
        self.order = order
        self.title = title
        self.kind = kind
        self.yoyaku_date = yoyaku_date
        self.torioki_date = torioki_date
        self.is_prepared = status == 'ご用意できました'

    def is_prepared(self):
        return self.is_prepared

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
