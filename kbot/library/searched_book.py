#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.log import Log
from kbot.library.common import Books, BookFilter
from kbot.message import Message


class SearchedBookFilter(BookFilter):
    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(SearchedBookFilter, self).__init__(users=users)
        self._books_class_name = "SearchedBooks"


class SearchedBooks(Books):

    TEMPLATE_SEARCHED_BOOKS = "searched_books.tpl"

    def __init__(self):
        super(SearchedBooks, self).__init__()

    def get_message(self, format="text"):
        message = ""
        data = {"books": self}
        message += Message.create(os.path.join(format, SearchedBooks.TEMPLATE_SEARCHED_BOOKS), data)

        return message

    def create_and_append(self, data):
        title = data[2].get_text().strip()
        author = data[3].get_text().strip()
        publisher = data[4].get_text().strip()
        publish_date = data[5].get_text().strip()
        searched_book = SearchedBook(title, author, publisher, publish_date)
        self.append(searched_book)


class SearchedBook(object):
    def __init__(self, title, author, publisher, publish_date):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        Log.info(self.to_string())
        print(self.to_string())

    def to_string(self):
        string = ("title:{0}\nauthor:{1}\npublisher:{2}\npublish_date:{3}").format(
            self.title, self.author, self.publisher, self.publish_date
        )
        return string
