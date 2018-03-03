#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.log import Log
from kbot.book.common import Books
from kbot.message import Message


class SearchedBooks(Books):

    TEMPLATE_SEARCHED_BOOKS = 'searched_books.tpl'

    def __init__(self, source):
        super(SearchedBooks, self).__init__(source)

    def get_message(self, format='text'):
        message = ''
        data = {'books': self}
        message += Message.create(os.path.join(format,
                                               SearchedBooks.TEMPLATE_SEARCHED_BOOKS), data)

        return message


class SearchedBook(object):

    def __init__(self, title, author, publisher, publish_date):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        Log.info(self.to_string())
        print(self.to_string())

    def to_string(self):
        string = ('title:{0}\nauthor:{1}\npublisher:{2}\npublish_date:{3}').format(
            self.title,
            self.author,
            self.publisher,
            self.publish_date
        )
        return string
