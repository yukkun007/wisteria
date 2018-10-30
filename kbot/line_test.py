#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import MagicMock

from kbot.kbot import KBot
from kbot.line import Line

from linebot import LineBotApi
from linebot.models import ButtonsTemplate, URITemplateAction


class TestLine:
    def setup(self):
        KBot("wisteria")

    @pytest.fixture()
    def line1(request):
        line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN_DEBUG"])
        line = Line(line_bot_api)
        return line

    def test_1(self, line1):
        line1.my_push_message("これはテストです。", [os.environ["LINE_SEND_ID"]])

    def test_2(self, line1):
        buttons_template = ButtonsTemplate(
            title="test",
            text="this is test.",
            actions=[URITemplateAction(label="YouTubeへ", uri="https://www.youtube.com/")],
        )
        line1.my_push_message(buttons_template, [os.environ["LINE_SEND_ID"]])

    def test_my_reply_message(self, line1):
        mock_event = MagicMock()
        method = MagicMock()
        line1.line_bot_api.reply_message = method
        line1.my_reply_message("test", mock_event)
        method.assert_called_once()
