#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from kbot.log import Log


class HtmlParser(object):

    @classmethod
    def get_books(cls, html, books):
        soup = HtmlParser.__get_soup(html)
        table = HtmlParser.__get_books_table(soup, books)
        if table is None:
            return books

        tds_list = HtmlParser.__get_target_tds_list(table)
        for tds in tds_list:
            books.create_and_append(tds)

        Log.info('number of {0}:{1}'.format(books.__class__.__name__, books.len))

        return books

    @classmethod
    def __get_soup(cls, html):
        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def __get_books_table(cls, soup, books):
        type_string = books.__class__.__name__
        if type_string in {'RentalBooks'}:
            table = HtmlParser.__get_table(soup, 'FormLEND')
        elif type_string == 'ReservedBooks':
            table = HtmlParser.__get_table(soup, 'FormRSV')
        elif type_string == 'SearchedBooks':
            table = HtmlParser.__get_table_by_attribute_value(soup, 'rules', 'none')
        return table

    @classmethod
    def __get_table(cls, soup, id_string):
        table = soup.select("form[name='" + id_string + "'] > table[border]")

        if len(table) <= 0:
            Log.info('table not found.')
            return None

        return table

    @classmethod
    def __get_table_by_attribute_value(cls, soup, attribute, value):
        css_selector = "table[" + attribute + "=\"" + value + "\"]"
        print(css_selector)
        table = soup.select(css_selector)

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
