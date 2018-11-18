#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime


class Movie(object):
    def __init__(self, title, video_id, url, published_at):
        self.title = title
        self.past_years = self.__get_past_years(title[:4])
        self.video_id = video_id
        self.url = url
        self.published_at = published_at

    def __get_past_years(self, value: str) -> int:
        try:
            now = datetime.datetime.now()
            return now.year - int(value)
        except ValueError:
            return 0

    def to_string(self):
        string = "title:{0} video_id:{1} url:{2}, published_at:{3}".format(
            self.title, self.video_id, self.url, self.published_at
        )
        return string
