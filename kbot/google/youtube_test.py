#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.kbot import KBot
from kbot.google.youtube import YouTube

class TestYouTube:

    def test_youtube(self):
        kbot = KBot('wisteria')
        youtube = YouTube('wisteria')
        movie   = youtube.get_youtube_movie()

