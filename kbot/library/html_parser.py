#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from kbot.library.rental_book import RentalBook, RentalBooks
from kbot.library.reserved_book import ReservedBook, ReservedBooks
from kbot.log import Log


class HtmlParser(object):

    @classmethod
    def get_rental_books(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        table = HtmlParser.__get_table(soup, 'FormLEND')
        if table is None:
            return RentalBooks([])

        rental_books = RentalBooks([])
        tds_list = HtmlParser.__get_target_tds_list(table)
        for tds in tds_list:
            rental_books.append(HtmlParser.__get_rental_book(tds))

        Log.info('number of rental_books:{0}'.format(rental_books.length()))

        return rental_books

    @classmethod
    def get_reserved_books(cls, html):
        soup = BeautifulSoup(html, 'html.parser')

        table = HtmlParser.__get_table(soup, 'FormRSV')
        if table is None:
            return ReservedBooks()

        reserved_books = ReservedBooks()
        tds_list = HtmlParser.__get_target_tds_list(table)
        for tds in tds_list:
            reserved_books.append(HtmlParser.__get_reserved_book(tds))

        Log.info(
            'number of reserved_books:{0}'.format(
                reserved_books.length()))

        return reserved_books

    @classmethod
    def __get_table(cls, soup, id_string):
        table = soup.select("form[name='" + id_string + "'] > table[border]")

        if len(table) <= 0:
            Log.info('table not found.')
            return None

        return table

    @classmethod
    def __get_target_tds_list(cls, table):
        trs = table[0].find_all('tr')

        target_tds_list = []
        for tr in trs:
            tds = tr.find_all(['td', 'th'])
            no = tds[0].string.strip()
            if no.isnumeric() is False:
                continue
            target_tds_list.append(tds)

        Log.info('number of target tr tag:{0}'.format(len(target_tds_list)))

        return target_tds_list

    @classmethod
    def __get_rental_book(cls, tds):
        no = tds[0].string.strip()
        # タイトル
        title = tds[2].get_text().strip()
        # 返却期限日
        expire_date = tds[7].get_text().strip()
        # 貸出更新
        can_extend_period = HtmlParser.__can_extend_period(
            tds[1].get_text().strip())
        # 更新ボタンの名前
        extend_period_button_name = 'L(' + no + ')'

        rental_book = RentalBook(
            title,
            expire_date,
            can_extend_period,
            extend_period_button_name
        )

        return rental_book

    @classmethod
    def __get_reserved_book(cls, tds):
        status = tds[1].get_text().strip()
        order = tds[2].get_text().strip()
        title = tds[3].a.get_text().strip()
        kind = tds[4].get_text().strip()
        yoyaku_date = tds[6].get_text().strip()
        torioki_date = tds[7].get_text().strip()

        reserved_book = ReservedBook(
            status,
            order,
            title,
            kind,
            yoyaku_date,
            torioki_date)

        return reserved_book

    @classmethod
    def __can_extend_period(cls, text):
        if '更新' in text:
            return False
        return True
