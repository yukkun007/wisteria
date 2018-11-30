#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import httplib2
import os
import random
from typing import List, Union, Optional
from datetime import datetime, timedelta
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

    def __create_movie(self, playlist_item) -> Union[None, Movie]:
        if playlist_item is None:
            return None

        title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        url = playlist_item["snippet"]["thumbnails"]["high"]["url"]
        published_at = playlist_item["snippet"]["publishedAt"]

        movie = Movie(title, video_id, url, published_at)
        print("create movie: " + movie.to_string())

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

    def __is_within_one_week(self, date_str: str) -> bool:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z")
        now = datetime.now()
        one_week_ago = now - timedelta(weeks=1)
        if one_week_ago < date:
            # １週間以内ならtrue
            return True
        else:
            return False

    def get_youtube_movie(self) -> Union[None, Movie]:
        return self.__get_youtube_movie(self.__filter_non)

    def __filter_non(self, items: List) -> List:
        return items

    def get_youtube_movie_match_today(self) -> Union[None, Movie]:
        return self.__get_youtube_movie(self.__filter_match_today)

    def __filter_match_today(self, items: List) -> List:
        return list(filter(lambda item: self.__match(item["snippet"]["title"]), items))

    def get_youtube_movies_recent(self) -> List[Optional[Movie]]:
        return self.__get_youtube_movies(self.__filter_recent)

    def __filter_recent(self, items: List) -> List:
        return list(
            filter(lambda item: self.__is_within_one_week(item["snippet"]["publishedAt"]), items)
        )

    def __get_playlistitems_list_request(self):
        channels_response = self.youtube.channels().list(mine=True, part="contentDetails").execute()

        for channel in channels_response["items"]:
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
            print("Videos in list %s" % uploads_list_id)

        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=uploads_list_id, part="snippet", maxResults=50
        )

        return playlistitems_list_request

    def __get_youtube_movie(self, filter_method) -> Union[None, Movie]:
        playlistitems_list_request = self.__get_playlistitems_list_request()

        all_items = []
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            items = playlistitems_list_response["items"]
            filterd_items = filter_method(items)
            select_item = self.__select_movie_item(filterd_items)
            all_items.append(select_item)

            playlistitems_list_request = self.youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response
            )

        return self.__create_movie(self.__select_movie_item(all_items))

    def __get_youtube_movies(self, filter_method) -> List[Optional[Movie]]:
        playlistitems_list_request = self.__get_playlistitems_list_request()

        all_items: List[Movie] = []
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            items = playlistitems_list_response["items"]
            filterd_items = filter_method(items)
            all_items.extend(filterd_items)

            playlistitems_list_request = self.youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response
            )

        print("----------- recent movie items ! length=%d" % (len(all_items)))
        all_movies = []
        for item in all_items:
            all_movies.append(self.__create_movie(item))

        # 最大でも１０個まで
        return all_movies[:10]

    def __select_movie_item(self, playlist_items: List) -> Union[None, Movie]:
        items_number = len(playlist_items)
        if items_number > 0:
            index = random.randint(0, items_number - 1)
            print("----------- select movie item ! number=%d, index=%d" % (items_number, index))
            return playlist_items[index]
        else:
            print("empty playlist.")
            return None
