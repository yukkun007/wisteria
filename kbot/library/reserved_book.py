# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from jinja2 import Environment, FileSystemLoader
from linebot.models import ButtonsTemplate,\
                           ConfirmTemplate,\
                           MessageTemplateAction,\
                           PostbackEvent,\
                           PostbackTemplateAction,\
                           URITemplateAction

class ReservedBooks(object):
    def __init__(self, source):
        if source == None:
            self.books  = []
        else:
            self.books = source

    def append(self, book):
        self.books.append(book)

    def length(self):
        return len(self.books)

    def list(self):
        return self.books

    def get_text_message(self, user):
        return self.get_message(user, format='text')

    def get_html_message(self, user):
        return self.get_message(user, format='html')

    def get_message(self, user, format='text'):
        message = ''
        if self.length() > 0:
            data      = {'user':           user,
                         'reserved_books': self.books,
                         'is_prepared':    self.prepared_reserved_book() }
            message += Message.create(os.path.join(format, 'reserved_books.tpl'), data)

        return message

    def prepared_reserved_book(self):
        for book in self.books:
            if book.status == 'ご用意できました':
                return True
        return False

class ReservedBook(object):

    def __init__(self, status, order, title, kind, yoyaku_date, torioki_date):
        self.status       = status
        self.order        = order
        self.title        = title
        self.kind         = kind
        self.yoyaku_date  = yoyaku_date
        self.torioki_date = torioki_date
        self.is_prepared  = status == 'ご用意できました'

    def is_prepared(self):
        return self.is_prepared

    def make_reserved_books_massage(root_dir, user_status):
        message = ''

        if len(user_status.reserved_books) > 0:
            env = Environment(loader=FileSystemLoader(root_dir))

            is_prepared = ReservedBook.prepared_reserved_book(user_status.reserved_books)
            template  = env.get_template('book/reserved_books.tpl')
            data      = {'user': user_status.user,
                         'reserved_books': user_status.reserved_books,
                         'is_prepared': is_prepared }
            message   = template.render(data)

        return message

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


