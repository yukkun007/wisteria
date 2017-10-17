#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from kbot.library.rental_book import RentalBook
from kbot.library.rental_books import RentalBooks
from kbot.library.yoyaku_book import YoyakuBook
from kbot.log import Log

class HtmlParser(object):

    def __init__(self, html):
        self.html = html

    def get_yoyaku_books(self):
        books = []
        soup  = BeautifulSoup(self.html, "html.parser")

        table = soup.select("form[name='FormRSV'] > table[border]")
        if len(table) > 0:
            trs = table[0].find_all("tr")
            for tr in trs:
                tds = tr.find_all(["td", "th"])
                no           = tds[0].string.strip()
                if no.isnumeric() is False:
                    continue

                status       = tds[1].get_text().strip()
                order        = tds[2].get_text().strip()
                title        = tds[3].a.get_text().strip()
                kind         = tds[4].get_text().strip()
                yoyaku_date  = tds[6].get_text().strip()
                torioki_date = tds[7].get_text().strip()

                book = YoyakuBook(
                    status,
                    order,
                    title,
                    kind,
                    yoyaku_date,
                    torioki_date)

                Log.info('--------------- ' + no)
                books.append(book)

        return books

    def get_rental_books(self):
        rental_books = RentalBooks()
        soup  = BeautifulSoup(self.html, "html.parser")

        table = soup.select("form[name='FormLEND'] > table[border]")
        if len(table) > 0:
            trs = table[0].find_all("tr")
            Log.info('number of tr tag:{0}'.format(len(trs)))
            for tr in trs:
                tds = tr.find_all(["td", "th"])
                no  = tds[0].string.strip()
                if no.isnumeric() is False:
                    continue

                # タイトル
                title                     = tds[2].get_text().strip()
                # 返却期限日
                expire_date               = tds[7].get_text().strip()
                # 貸出更新
                can_extend_period         = self.__can_extend_period(tds[1].get_text().strip())
                # 更新ボタンの名前
                extend_period_button_name = 'L(' + no + ')'

                rental_book = RentalBook(
                    title,
                    expire_date,
                    can_extend_period,
                    extend_period_button_name
                )

                Log.info(rental_book.to_string())
                rental_books.append(rental_book)
        else:
            Log.info('table not found.')

        Log.info('number of rental_books:{0}'.format(rental_books.length()))

        return rental_books

    def __can_extend_period(self, text):
        if '更新' in text:
            return False
        return True

