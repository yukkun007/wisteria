#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
import os
import random

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from kbot.google.movie import Movie

class YouTube(object):

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.secret_path = '/tmp/sc_test.txt'
        self.oauth_path = '/tmp/oa_test.txt'

    def get_youtube_movie(self):

        st = open(self.secret_path, 'w')
        secret = os.environ['YOUTUBE_CLIENT_SECRET']
        st.write(secret)
        st.close()

        oa = open(self.oauth_path, 'w')
        contents = os.environ['YOUTUBE_OAUTH_JSON']
        oa.write(contents)
        oa.close()

        CLIENT_SECRETS_FILE            = self.secret_path
        MISSING_CLIENT_SECRETS_MESSAGE = "missing client secrets."
        YOUTUBE_READONLY_SCOPE         = "https://www.googleapis.com/auth/youtube.readonly"
        YOUTUBE_API_SERVICE_NAME       = "youtube"
        YOUTUBE_API_VERSION            = "v3"

        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                       message=MISSING_CLIENT_SECRETS_MESSAGE,
                                       scope=YOUTUBE_READONLY_SCOPE)
        storage = Storage(self.oauth_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = argparser.parse_args()
            credentials = run_flow(flow, storage, flags)

        youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        http=credentials.authorize(httplib2.Http()))

        channels_response = youtube.channels().list(
            mine = True,
            part = "contentDetails"
        ).execute()

        for channel in channels_response["items"]:
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
            print("Videos in list %s" % uploads_list_id)

        playlistitems_list_request = youtube.playlistItems().list(
            playlistId = uploads_list_id,
            part       = "snippet",
            maxResults = 50
        )

        item_list = []
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            length = len(playlistitems_list_response["items"])
            print('!!!!!!!!!!!!!! len=%d' % length)
            index = random.randint(0, length - 1)
            playlist_item = playlistitems_list_response["items"][index]
            item_list.append(playlist_item)

            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

        index2 = random.randint(0, len(item_list) - 1)
        print('----------- len(items)=%d' % len(item_list))
        print('----------- index2=%d' % index2)
        fix_playlist_item = item_list[index2]

        # for playlist_item in playlistitems_list_response["items"]:
        title        = fix_playlist_item["snippet"]["title"]
        video_id     = fix_playlist_item["snippet"]["resourceId"]["videoId"]
        url          = fix_playlist_item["snippet"]["thumbnails"]["high"]["url"]
        published_at = fix_playlist_item["snippet"]["publishedAt"]
        print("%s (%s) %s %s" % (title, video_id, url, published_at))

        movie = Movie(title, video_id, url, published_at)

        return movie

