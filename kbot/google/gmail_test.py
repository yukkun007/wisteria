#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.google.gmail import GMail


class TestGMail:
    def setup(self):
        KBot("wisteria")

    @pytest.fixture()
    def gmail1(self):
        return GMail()

    @pytest.mark.slow
    def test_gmail(self, gmail1):
        gmail1.send_message_multi([os.environ["GMAIL_SEND_ADDRESS1"]], "this is test.", "test")

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "query",
        [("from:info@keishicho.metro.tokyo.jp"), ("from:info@keishicho.metro.tokyo.jp is:unread")],
    )
    def test_gmail_get_message(self, gmail1, query):
        gmail1.get_messages(query)

    def test_get_formatted_date(self, gmail1):
        formatted_date = gmail1._get_formatted_date("Fri, 05 Oct 2018 05:26:30 +0900")
        assert formatted_date == "2018/10/05 05:26:30"
