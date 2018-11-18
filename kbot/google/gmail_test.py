#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from kbot.kbot import KBot
from kbot.google.gmail import GMail


class TestGMail:
    @pytest.mark.slow
    def test_gmail(self):
        KBot("wisteria")
        gmail = GMail()
        gmail.send_message_multi([os.environ["GMAIL_SEND_ADDRESS1"]], "this is test.", "test")
