# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from linebot.models import ButtonsTemplate, PostbackTemplateAction
from kbot.library.common import Books, BookFilter
from kbot.log import Log


class ReservedBookFilter(BookFilter):

    _FILTER_RESERVED_PREPARED_NONE = "none"
    _FILTER_RESERVED_PREPARED_YES_AND_DEREVERD = "yes_and_dereverd"

    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_NONE
        self._books_class_name = "ReservedBooks"

    @property
    def almost_prepared(self):
        return self._prepared == ReservedBookFilter._FILTER_RESERVED_PREPARED_YES_AND_DEREVERD


class ReservedBookPreparedFilter(ReservedBookFilter):
    def __init__(self, *, users=BookFilter.FILTER_USERS_ALL):
        super(ReservedBookPreparedFilter, self).__init__(users=users)
        self._prepared = ReservedBookFilter._FILTER_RESERVED_PREPARED_YES_AND_DEREVERD


class ReservedBooks(Books):

    TEMPLATE_RESERVED_BOOKS = "reserved_books.tpl"

    def __init__(self):
        super(ReservedBooks, self).__init__()

    def create_and_append(self, data):
        status = data[1].get_text().strip()
        order = data[2].get_text().strip()
        title = data[3].get_text().strip()
        kind = data[4].get_text().strip()
        yoyaku_date = data[6].get_text().strip()
        torioki_date = data[7].get_text().strip()
        receive_lib = data[8].get_text().strip()

        reserved_book = ReservedBook(
            status, order, title, kind, yoyaku_date, torioki_date, receive_lib
        )

        self.append(reserved_book)

    def is_prepared_reserved_book(self):
        for book in self._list:
            if book.status == "ご用意できました":
                return True
        return False

    def apply_filter(self, filter_setting):
        if filter_setting.almost_prepared:
            filterd_books = filter(lambda book: book.is_prepared or book.is_dereverd, self._list)
            self._list = ReservedBooks.__sort(filterd_books)
        else:
            self._list = ReservedBooks.__sort(self._list)

    @classmethod
    def __sort(cls, books_list):
        return sorted(books_list, key=lambda book: (book.order_num, book.status))


class ReservedBook(object):
    def __init__(self, status, order, title, kind, yoyaku_date, torioki_date, receive_lib):
        self.status = status
        self.order = order
        self.order_num = self.__get_order_num(order)
        self.title = title
        self.kind = kind
        self.yoyaku_date = yoyaku_date
        self.torioki_date = torioki_date
        self.receive_lib = receive_lib
        self.is_prepared = ReservedBook.__is_prepared(status)
        self.is_dereverd = ReservedBook.__is_dereverd(status)

        Log.info(self.to_string())

    def to_string(self):
        string = (
            "status:{0} order:{1} title:{2} " "kind:{3} yoyaku_date:{4} receive_lib:{5}"
        ).format(self.status, self.order, self.title, self.kind, self.yoyaku_date, self.receive_lib)
        return string

    @classmethod
    def __is_prepared(cls, status):
        if status == "ご用意できました":
            return True
        return False

    @classmethod
    def __is_dereverd(cls, status):
        if status == "移送中です":
            return True
        return False

    def __get_order_num(self, order):
        try:
            return int(order.split("/")[0])
        except ValueError:
            return 0

    @staticmethod
    def make_finish_reserve_message_template(user_num):
        buttons_template = ButtonsTemplate(
            title="予約完了",
            text="予約できました。",
            actions=[
                PostbackTemplateAction(label="予約状況確認", data="check_reserve:" + user_num),
                PostbackTemplateAction(label="予約状況確認(全員分)", data="check_reserve:all"),
            ],
        )
        return buttons_template
