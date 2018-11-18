#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Dict
from datetime import date, timedelta
from dateutil.parser import parse
from collections import defaultdict
from kbot.log import Log
from kbot.library.common import Books
from kbot.library.rental_book_filter import RentalBookFilter


class RentalBook(object):
    def __init__(
        self,
        name: str,
        expire_date_text: str,
        can_extend_period: bool,
        extend_period_button_name: str,
    ) -> None:
        self.name: str = name
        self.expire_date: date = parse(expire_date_text).date()
        self.expire_date_text: str = expire_date_text
        self.can_extend_period: bool = can_extend_period
        self.extend_period_button_name: str = extend_period_button_name

        Log.info(self.to_string())

    def is_expired(self) -> bool:
        return self.is_expire_in_xdays(-1)

    def is_expire_in_xdays(self, xday_before: int) -> bool:
        today = date.today()
        if self.expire_date - today <= timedelta(days=xday_before):
            return True
        return False

    def get_expire_text_from_today(self) -> str:
        today = date.today()
        remain_days = (self.expire_date - today).days

        if remain_days == 1:
            text = " (明日ﾏﾃﾞ)"
        elif remain_days == 0:
            text = " (今日ﾏﾃﾞ)"
        elif remain_days < 0:
            text = " (延滞)"
        else:
            text = " (あと{0}日)".format(remain_days)

        return text

    def to_string(self) -> str:
        string = (
            "name:{0} expire_date:{1} expire_date(text):{2} "
            "can_extend_period:{3} extend_period_button_name:{4}"
        ).format(
            self.name,
            self.expire_date,
            self.expire_date_text,
            self.can_extend_period,
            self.extend_period_button_name,
        )
        return string


class RentalBooks(Books):

    TEMPLATE_RENTAL_BOOKS: str = "rental_books.tpl"

    def __init__(self, filter_setting: RentalBookFilter = RentalBookFilter()) -> None:
        super(RentalBooks, self).__init__()
        self._filter_setting: RentalBookFilter = filter_setting

    @property
    def filter_setting(self) -> RentalBookFilter:
        return self._filter_setting

    def apply_filter(self, filter_setting: RentalBookFilter) -> None:
        self._filter_setting = filter_setting
        self._filter_setting.execute(self)
        # self._list = self._filter_setting.execute(self._list)

        # if filter_setting.is_type_none:
        #     self.list: List[RentalBook] = RentalBooks.__sort(self.list)
        # elif filter_setting.is_type_expired:
        #     filterd_books = filter(lambda book: book.is_expired(), self._list)
        #     self.list: List[RentalBook] = RentalBooks.__sort(filterd_books)
        # elif filter_setting.is_type_expire:
        #     filterd_books = filter(
        #         lambda book: book.is_expire_in_xdays(filter_setting.xdays), self._list
        #     )
        #     self._list = RentalBooks.__sort(filterd_books)

    def create_and_append(self, data) -> None:
        no = data[0].string.strip()
        # タイトル
        title = data[2].get_text().strip()
        # 返却期限日
        expire_date = data[7].get_text().strip()
        # 貸出更新
        can_extend_period = RentalBooks.__can_extend_period(data[1].get_text().strip())
        # 更新ボタンの名前
        extend_period_button_name = "L(" + no + ")"

        rental_book = RentalBook(title, expire_date, can_extend_period, extend_period_button_name)

        self.append(rental_book)

    @classmethod
    def __can_extend_period(cls, text: str) -> bool:
        if "更新" in text:
            return False
        return True

    @classmethod
    def __sort(cls, books_list: List[RentalBook]) -> List[RentalBook]:
        return list(sorted(books_list, key=lambda book: (book.expire_date, book.name)))

    @classmethod
    def get_date_keyed_books_dict(cls, books: Books) -> Dict[str, List]:
        date_keyed_books_dict: Dict[str, List] = defaultdict(lambda: [])
        for book in books.list:
            date_keyed_books_dict[book.expire_date_text].append(book)
        return date_keyed_books_dict
