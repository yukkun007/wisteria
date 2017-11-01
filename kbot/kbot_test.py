#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.kbot import KBot


class TestKBot:

    def test_get_xdays(self):
        kbot = KBot('wisteria')
        value = kbot.get_xdays('2日')
        assert value == 2
