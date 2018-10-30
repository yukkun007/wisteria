#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from kbot.kbot import KBot
from kbot.google.gmail import GMail


class TestGMail:
    def test_gmail(self):
        KBot("wisteria")
        gmail = GMail()
        gmail.send_message_multi([os.environ["GMAIL_SEND_ADDRESS1"]], "this is test.", "test")
