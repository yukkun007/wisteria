# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot.models import ButtonsTemplate,\
    PostbackTemplateAction
from kbot.message import Message


class ReservedBooks(object):
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

    def set_user(self, user):
        self.user = user

    def get_message(self, format='text'):
        message = ''
        if self.length() > 0:
            data = {'user': self.user,
                    'reserved_books': self.books,
                    'is_prepared': self.is_prepared_reserved_book()}
            message += Message.create(os.path.join(format,
                                                   'reserved_books.tpl'), data)

        return message

    def is_prepared_reserved_book(self):
        for book in self.books:
            if book.status == 'ご用意できました':
                return True
        return False


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
                                       data='check_reserve:1,2,3,4')
            ]
        )
        return buttons_template
