#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from kbot.library.rental_book import RentalBook
from kbot.library.rental_books import RentalBooks
from kbot.log import Log

class HtmlParser(object):

    def __init__(self, html):
        self.html = html

    def get_rental_books(self):
        soup  = BeautifulSoup(self.html, "html.parser")

        table = soup.findAll("table")[7]
        rows  = table.findAll("tr")

        rental_books = RentalBooks()
        for row in rows:
            tds = row.findAll(['td', 'th'])

            first_cell = tds[0].get_text().strip()
            last_cell  = tds[-1].get_text().strip()

            #print('first:{}'.format(first_cell))
            #print('last:{}'.format(last_cell))

            if first_cell.isnumeric() is False:
                continue

            # タイトル
            title                     = tds[2].get_text().strip()
            # 返却期限日
            expire_date               = tds[7].get_text().strip()
            # 貸出更新
            can_extend_period         = self.__can_extend_period(tds[1].get_text().strip())
            # 更新ボタンの名前
            extend_period_button_name = 'L(' + first_cell + ')'

            rental_book = RentalBook(
                title,
                expire_date,
                can_extend_period,
                extend_period_button_name
            )
            Log.info(rental_book.to_string())
            rental_books.append(rental_book)

        return rental_books

    def __can_extend_period(self, text):
        if '更新' in text:
            return False
        return True

