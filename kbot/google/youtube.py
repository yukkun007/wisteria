#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import httplib2
import os
import random
from datetime import datetime
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from kbot.google.movie import Movie


class YouTube(object):
    def __init__(self):
        self.secret_path = "/tmp/sc_test.txt"
        self.oauth_path = "/tmp/oa_test.txt"

        st = open(self.secret_path, "w")
        secret = os.environ["YOUTUBE_CLIENT_SECRET"]
        st.write(secret)
        st.close()

        oa = open(self.oauth_path, "w")
        contents = os.environ["YOUTUBE_OAUTH_JSON"]
        oa.write(contents)
        oa.close()

        MISSING_CLIENT_SECRETS_MESSAGE = "missing client secrets."
        YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        flow = flow_from_clientsecrets(
            self.secret_path, message=MISSING_CLIENT_SECRETS_MESSAGE, scope=YOUTUBE_READONLY_SCOPE
        )
        storage = Storage(self.oauth_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = argparser.parse_args()
            credentials = run_flow(flow, storage, flags)

        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()),
        )

    def get_youtube_movie(self):
        channels_response = self.youtube.channels().list(mine=True, part="contentDetails").execute()

        for channel in channels_response["items"]:
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
            print("Videos in list %s" % uploads_list_id)

        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=uploads_list_id, part="snippet", maxResults=50
        )

        item_list = []
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            length = len(playlistitems_list_response["items"])
            print("!!!!!!!!!!!!!! len=%d" % length)
            index = random.randint(0, length - 1)
            playlist_item = playlistitems_list_response["items"][index]
            item_list.append(playlist_item)

            playlistitems_list_request = self.youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response
            )

        index2 = random.randint(0, len(item_list) - 1)
        print("----------- len(items)=%d" % len(item_list))
        print("----------- index2=%d" % index2)
        fix_playlist_item = item_list[index2]

        title = fix_playlist_item["snippet"]["title"]
        video_id = fix_playlist_item["snippet"]["resourceId"]["videoId"]
        url = fix_playlist_item["snippet"]["thumbnails"]["high"]["url"]
        published_at = fix_playlist_item["snippet"]["publishedAt"]
        print("%s (%s) %s %s" % (title, video_id, url, published_at))

        movie = Movie(title, video_id, url, published_at)

        return movie

    def __get_compile_date_pattern(self):
        pattern = r"^2\d{3}" + datetime.now().strftime("/%m/%d")
        return re.compile(pattern)

    def __match(self, content: str) -> bool:
        pattern = self.__get_compile_date_pattern()
        if re.search(pattern, content):
            print("match ! content=" + content)
            return True
        else:
            return False

    def get_youtube_movie_match_date(self):
        channels_response = self.youtube.channels().list(mine=True, part="contentDetails").execute()

        for channel in channels_response["items"]:
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
            print("Videos in list %s" % uploads_list_id)

        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=uploads_list_id, part="snippet", maxResults=50
        )

        all_match_items = []
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            list_items = playlistitems_list_response["items"]

            match_items = list(
                filter(lambda item: self.__match(item["snippet"]["title"]), list_items)
            )
            if len(match_items) > 0:
                index = random.randint(0, len(match_items) - 1)
                print("----------- match item found ! len=%d, index=%d" % (len(match_items), index))
                all_match_items.append(match_items[index])

            playlistitems_list_request = self.youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response
            )

        if len(all_match_items) > 0:
            index = random.randint(0, len(all_match_items) - 1)
            print(
                "----------- [fix] match item found ! len=%d, index=%d"
                % (len(all_match_items), index)
            )
            fix_playlist_item = all_match_items[index]

            title = fix_playlist_item["snippet"]["title"]
            video_id = fix_playlist_item["snippet"]["resourceId"]["videoId"]
            url = fix_playlist_item["snippet"]["thumbnails"]["high"]["url"]
            published_at = fix_playlist_item["snippet"]["publishedAt"]
            print("%s (%s) %s %s" % (title, video_id, url, published_at))

            movie = Movie(title, video_id, url, published_at)
            return movie
        else:
            print("not found video.")
            return None
