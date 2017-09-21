#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.library.html_pages import HtmlPages
from kbot.library.html_parser import HtmlParser
from kbot.library.message import Message
from kbot.library.filter import Filter

class Library(object):

    def __init__(self, root_dir, users):
        self.root_dir   = root_dir
        self.users      = users
        self.pages      = HtmlPages()
        self.is_fetched = False
        self.user_dict  = {}
        self.books_dict = {}

    def __finalize(self):
        self.pages.finalize()

    def __get_rental_books(self, user):
        html   = self.pages.fetch_html(user)
        parser = HtmlParser(html)
        books  = parser.get_rental_books()

        return books

    def __registe(self, user, books):
        self.user_dict[user.num]  = user
        self.books_dict[user.num] = books

    def fetch_status(self):
        if self.is_fetched == False:
            for user in self.users:
                books = self.__get_rental_books(user)
                self.__registe(user, books)
            self.__finalize()

        self.is_fetched = True

    def is_target_exist(self):
        all_books_count = 0
        if self.is_fetched == True:
            for user_num, user in self.user_dict.items():
                books = self.books_dict[user_num]
                all_books_count += books.length()
        if all_books_count > 0:
            return True
        return False

    def do_filter(self, books_filter):
        for user_num, user in self.user_dict.items():
            books = self.books_dict[user_num]
            books.do_filter(books_filter)

    def get_message(self, type=Message.TYPE_SHORT):
        message = Message(self.root_dir, self.user_dict, self.books_dict)
        text_message = message.create(type)

        return text_message

