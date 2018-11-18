#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kbot.kbot import KBot
from kbot.google.youtube import YouTube


class TestYouTube:
    @pytest.mark.slow
    def test_youtube(self):
        KBot("wisteria")
        youtube = YouTube()
        youtube.get_youtube_movie()
