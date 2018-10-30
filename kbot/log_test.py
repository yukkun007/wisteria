#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.log import Log


class TestLog:
    def test_log(self):
        Log.info("test")

    def test_log_exception(self):
        Log.logging_exception(Exception("test"))
