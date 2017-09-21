#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
from collections import defaultdict
from jinja2 import Template, Environment, FileSystemLoader
from kbot.log import Log
from kbot.library.filter import Filter

class Message(object):
    TEMPLATE_HEADER    = "header.tpl"
    TEMPLATE_RENTAL    = "rental.tpl"
    TEMPLATE_EXPIRED   = "expired.tpl"
    TEMPLATE_EXPIRE    = "expire.tpl"
    TEMPLATE_BOOK_LIST = "book_list.tpl"
    TEMPLATE_FOOTER    = "footer.tpl"

    TYPE_SHORT = "short_message"
    TYPE_LONG  = "long_message"

    def __init__(self, root_dir, user_dict, books_dict):
        self.root_dir   = root_dir
        self.user_dict  = user_dict
        self.books_dict = books_dict

    def create(self, message_type=TYPE_SHORT):
        env = Environment(loader=FileSystemLoader(self.root_dir))

        header  = env.get_template(os.path.join(message_type, Message.TEMPLATE_HEADER))
        message = header.render()

        sorted_user_nums = sorted(self.user_dict)
        all_books_count = 0
        for user_num in sorted_user_nums:
            books = self.books_dict[user_num]

            all_books_count += books.length()

            if books.length() > 0:
                user  = self.user_dict[user_num]

                template  = env.get_template(os.path.join(message_type, self.__get_template(books)))
                data      = {'user': user, 'books_len': books.length(), 'xdays': books.filter.xdays}
                message  += template.render(data)

                date_keyed_books_dict = self.__get_date_keyed_books_dict(books)

                book_list  = env.get_template(os.path.join(message_type, Message.TEMPLATE_BOOK_LIST))
                data       = {'date_keyed_books_dict': date_keyed_books_dict, 'books_org': books.list()}
                message   += book_list.render(data)

        footer   = env.get_template(os.path.join(message_type, Message.TEMPLATE_FOOTER))
        data     = {'all_books_count': all_books_count}
        message += footer.render(data)

        return message

    def __get_template(self, books):
        if books.filter.type == Filter.FILTER_NONE:
            template = Message.TEMPLATE_RENTAL
        elif books.filter.type == Filter.FILTER_EXPIRED:
            template = Message.TEMPLATE_RENTAL
        elif books.filter.type == Filter.FILTER_EXPIRE:
            template = Message.TEMPLATE_RENTAL
        return template

    def __get_date_keyed_books_dict(self, books):
        date_keyed_books_dict = defaultdict(lambda: [])
        for book in books.list():
            date_keyed_books_dict[book.expire_date_text].append(book)
        return date_keyed_books_dict

