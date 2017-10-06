#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, FileSystemLoader
from kbot.library.yoyaku_book import YoyakuBook

class UserStatus(object):

    def __init__(self, user):
        self.user = user

    def set_reserved_books(self, reserved_books):
        self.reserved_books = reserved_books

    def set_rental_books(self, rental_books):
        self.rental_books = rental_books

    def make_user_reserved_books_message(root_dir, user_status_list):
        env = Environment(loader=FileSystemLoader(root_dir))

        sub_message = ''
        for user_status in user_status_list:
            sub_message += YoyakuBook.make_reserved_books_massage(root_dir, user_status)

        is_prepared = UserStatus.prepared_reserved_book(user_status_list)
        template  = env.get_template('book/user_reserved_books.tpl')
        data      = { 'sub_message': sub_message, 'is_prepared': is_prepared }
        message   = template.render(data)

        return message

    def prepared_reserved_book(user_status_list):
        for user_status in user_status_list:
            reserved_books = user_status.reserved_books
            for book in reserved_books:
                if book.status == 'ご用意できました':
                    return True
        return False

