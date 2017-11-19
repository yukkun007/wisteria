# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
from linebot.models import ButtonsTemplate,\
    PostbackTemplateAction
from kbot.message import Message
from kbot.book.common import Books


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
