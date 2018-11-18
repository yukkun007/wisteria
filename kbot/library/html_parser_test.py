#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch, MagicMock
from kbot.kbot import KBot
from kbot.library.user import User
from kbot.library.html_page import HtmlPage
from kbot.library.html_parser import HtmlParser
from kbot.library.library import Library
from kbot.library.rental_book import RentalBooks
from kbot.library.reserved_book import ReservedBooks
from kbot.library.searched_book import SearchedBooks


class TestHtmlParser:
    def setup(self):
        KBot("wisteria")

    @pytest.mark.slow
    def test_get_rental_books(self):
        page = HtmlPage()
        user = User(os.environ["USER1"])
        html = page.fetch_login_page(Library.LIBRALY_HOME_URL, user)
        HtmlParser.get_books(html, RentalBooks())

    @pytest.mark.parametrize(
        "books, books_class", [(RentalBooks(), RentalBooks), (ReservedBooks(), ReservedBooks)]
    )
    def test_get_books_no_table(self, books, books_class):
        with patch(
            "kbot.library.html_parser.HtmlParser._HtmlParser__get_books_table"
        ) as method, patch("kbot.library.html_parser.HtmlParser._HtmlParser__get_soup"):
            method.return_value = None
            books = HtmlParser.get_books(None, books)
            assert isinstance(books, books_class)
            assert books.len == 0

    @pytest.mark.parametrize(
        "target, table_name", [(RentalBooks(), "FormLEND"), (ReservedBooks(), "FormRSV")]
    )
    def test_get_books_table(self, target, table_name):
        with patch("kbot.library.html_parser.HtmlParser._HtmlParser__get_table") as mock:
            soup_mock = MagicMock()
            HtmlParser._HtmlParser__get_books_table(soup_mock, target)
            mock.assert_called_once_with(soup_mock, table_name)

    def test_get_books_table_searched_books(self):
        with patch(
            "kbot.library.html_parser.HtmlParser._HtmlParser__get_table_by_attribute_value"
        ) as mock:
            soup_mock = MagicMock()
            HtmlParser._HtmlParser__get_books_table(soup_mock, SearchedBooks())
            mock.assert_called_once_with(soup_mock, "rules", "none")

    def test_get_table_empty(self):
        soup = HtmlParser._HtmlParser__get_soup("<html></html>")
        result = HtmlParser._HtmlParser__get_table(soup, "empty")
        assert result is None

    def test_get_table_by_attribute_value_empty(self):
        soup = HtmlParser._HtmlParser__get_soup("<html></html>")
        result = HtmlParser._HtmlParser__get_table_by_attribute_value(soup, "empty", "empty")
        assert result is None
