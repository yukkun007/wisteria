#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch, MagicMock
from kbot.views import (
    check_rental_state,
    check_reserve_state,
    youtube_omoide,
    library_reserve,
    _handler_maps,
)
from kbot.views import __check_rental_state as inner_check_rental_state
from kbot.views import __check_reserve_state as inner_check_reserve_state
from kbot.views import __youtube_omoide as inner_youtube_omoide
from kbot.views import __library_reserve as inner_library_reserve
from kbot.views import (
    __get_rental_book_filter_of_user_specify as inner_get_rental_book_filter_of_user_specify,
)
from kbot.views import __get_rental_book_expire_filter as inner_get_rental_book_expire_filter
from kbot.views import __call_handler as inner_call_handler
from kbot.views import __handle_text_event as inner_handle_text_event
from kbot.views import __check_books as check_books
from kbot.views import __reply_command_menu as reply_command_menu
from kbot.views import __reply_response_string as reply_response_string
from kbot.views import __search_rakuten_book as search_rakuten_book
from kbot.views import __search_library_book as search_library_book
from kbot.views import __search_book_by_isbn as search_book_by_isbn
from kbot.kbot import KBot
from kbot.library.rental_book_filter import (
    RentalBookFilter,
    RentalBookExpireFilter,
    RentalBookExpiredFilter,
)
from kbot.library.reserved_book import ReservedBookFilter


class TestViews:
    def setup(self):
        KBot("wisteria")

    @classmethod
    def __create_request_mock(cls, method):
        request_mock = MagicMock()
        request_mock.method = method
        return request_mock

    @pytest.mark.parametrize(
        "http_method, mock_method, target_method",
        [
            ("GET", "kbot.views.__check_rental_state", check_rental_state),
            ("GET", "kbot.views.__check_reserve_state", check_reserve_state),
        ],
    )
    def test_check_xxxxx_state(self, http_method, mock_method, target_method):
        with patch(mock_method) as mock, patch("kbot.views.HttpResponse"):
            target_method(TestViews.__create_request_mock(http_method))
            if http_method == "GET":
                mock.assert_called_once()

    @pytest.mark.slow
    def test_inner_check_rental_state(self):
        inner_check_rental_state("0")

    @pytest.mark.slow
    def test_inner_check_reserve_state(self):
        inner_check_reserve_state("0")

    @pytest.mark.parametrize("http_method", [("GET"), ("OTHER")])
    def test_youtube_omoide(self, http_method):
        with patch("kbot.views.__youtube_omoide") as mock, patch("kbot.views.HttpResponse"), patch(
            "kbot.views.HttpResponseBadRequest"
        ):
            youtube_omoide(TestViews.__create_request_mock(http_method))
            if http_method == "GET":
                mock.assert_called_once()

    @pytest.mark.slow
    def test_inner_youtube_omoide(self):
        inner_youtube_omoide()

    @pytest.mark.parametrize("http_method", [("GET")])
    def test_library_reserve(self, http_method):
        with patch("kbot.views.__library_reserve") as mock, patch("kbot.views.HttpResponse"):
            request_mock = TestViews.__create_request_mock(http_method)
            request_mock.GET.get.return_value = "book_id:1111"
            library_reserve(request_mock)
            if http_method == "GET":
                mock.assert_called_once()

    def test_inner_library_reserve_success(self):
        with patch("kbot.views.Library.reserve") as mock, patch("kbot.views.HttpResponseRedirect"):
            inner_library_reserve("book_id:1111")
            mock.assert_called_once()

    def test_inner_library_reserve_fail(self):
        inner_library_reserve(None)

    def test_inner_get_rental_book_filter_of_user_specify(self):
        filter = inner_get_rental_book_filter_of_user_specify("図書？test")
        assert isinstance(filter, RentalBookFilter)

    def test_inner_get_rental_book_expire_filter(self):
        filter = inner_get_rental_book_expire_filter("hoge")
        assert isinstance(filter, RentalBookExpireFilter)

    @pytest.mark.parametrize(
        "filter, filter2", [(None, None), (MagicMock(), None), (MagicMock(), MagicMock())]
    )
    def test_inner_call_handler(self, filter, filter2):
        event = MagicMock()
        event.message.text = "message"
        handler = MagicMock()
        if filter is not None:
            filter_return = MagicMock()
            filter.return_value = filter_return
        if filter2 is not None:
            filter2_return = MagicMock()
            filter2.return_value = filter2_return
        handler_map = {"handler": handler, "filter": filter, "filter2": filter2}
        inner_call_handler(event, handler_map)
        if filter is None:
            handler.assert_called_once_with(event, text=event.message.text)
        elif filter is not None and filter2 is not None:
            handler.assert_called_once_with(event, filter_return, filter2_return)
        else:
            handler.assert_called_once_with(event, filter_return)

    def test_inner_handle_text_event(self):
        event = MagicMock()
        event.message.text = "message_test"
        handler_map1 = {"keyword": "message"}
        handler_map2 = {"keyword": "message"}
        handler_maps = [handler_map1, handler_map2]
        with patch("kbot.views.__call_handler") as mock:
            inner_handle_text_event(event, handler_maps)
            mock.assert_called_once()

    @pytest.mark.parametrize(
        "event_text, is_called",
        [
            ("図書？", True),
            ("図書館", True),
            ("2日で延滞", True),
            ("延滞", True),
            ("予約", True),
            ("予約？", True),
            ("本？", True),
            ("ほ？", True),
            ("文字", True),
            ("コマンド", True),
            ("？", False),
        ],
    )
    def test_inner_handle_text_event_all(self, event_text, is_called):
        event = MagicMock()
        event.message.text = event_text
        with patch("kbot.views.__call_handler") as mock:
            inner_handle_text_event(event, _handler_maps)
            if is_called:
                mock.assert_called_once()
            else:
                mock.assert_not_called()

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "filter",
        [
            (RentalBookFilter(users="all")),
            (RentalBookExpireFilter(users="all", xdays="2")),
            (RentalBookExpiredFilter(users="all")),
        ],
    )
    def test_check_rental_books(self, filter):
        check_books(None, filter)

    def test_reply_command_menu(self):
        reply_command_menu(None)

    def test_reply_response_string(self):
        reply_response_string(None)

    @pytest.mark.slow
    @pytest.mark.parametrize("user_nums", [("0,1,2,3"), ("0,2")])
    def test_check_reserved_books(self, user_nums):
        filter_setting = ReservedBookFilter(users=user_nums)
        check_books(None, filter_setting)

    @pytest.mark.slow
    @pytest.mark.parametrize("query", [("本？坊っちゃん"), ("著？夏目漱石")])
    def test_search_rakuten_book(self, query):
        search_rakuten_book(None, text=query)

    @pytest.mark.slow
    def test_search_book_by_isbn(self):
        search_book_by_isbn(None, "isbn:9784532280208")

    @pytest.mark.slow
    @pytest.mark.parametrize("query", [("ほ？坊っちゃん"), ("ほ？あ")])
    def test_search_library_book(self, query):
        search_library_book(None, query)
