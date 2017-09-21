#!/usr/bin/python
# -*- coding: utf-8 -*-

class Movie(object):
    def __init__(self, title, video_id, url, published_at):
        self.title = title
        self.video_id = video_id
        self.url = url
        self.published_at = published_at

    def to_string(self):
        string = "title:{0} video_id:{1} url:{2}, published_at:{3}".format(
            self.title,
            self.video_id,
            self.url,
            self.published_at)
        return string

