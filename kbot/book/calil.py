# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests
from time import sleep
from kbot.log import Log
from kbot.message import Message
from kbot.book.common import BookSearchQuery


class CalilService(object):

    CALIL_BASE_URL = 'http://api.calil.jp/check'

    @classmethod
    def get_one_book(cls, query):
        systemid1 = 'Tokyo_Nerima'
        systemid2 = 'Special_Jil'
        query.set('systemid', systemid1 + ',' + systemid2)

        json_data = CalilService.__request(CalilQuery.adjust_first_query(query))
        json_data = CalilService.__polling(json_data)
        book1 = CalilService.__get_one_book_from_json(json_data, query.get('isbn'), systemid1)
        # book2 = CalilService.__get_one_book_from_json(json_data, query.get('isbn'), systemid2)

        return book1

    @classmethod
    def __polling(cls, json_data):
        while json_data['continue'] == 1:
            sleep(2)
            query = BookSearchQuery()
            query.set('session', json_data['session'])
            json_data = CalilService.__polling_request(CalilQuery.adjust_next_query(query))
        return json_data

    @classmethod
    def __get_one_book_from_json(cls, json_data, isbn, systemid):
        reserve_info = json_data['books'][isbn][systemid]
        status = reserve_info.get('status')
        if status != 'OK' and status != 'Cache':
            return CalilBook(isbn, {})
        return CalilBook(isbn, reserve_info)

    @classmethod
    def __request(cls, query):
        response = CalilService.__request_sub(query)
        json_data = response.json()  # TODO:nullチェック
        Log.info(json.dumps(json_data, sort_keys=True, indent=4))
        return json_data

    @classmethod
    def __polling_request(cls, query):
        response = CalilService.__request_sub(query)
        # 2回目以降のレスポンスはJSONP固定になるため
        json_string = response.text[9:-2]
        json_data = json.loads(json_string)
        Log.info(json.dumps(json_data, sort_keys=True, indent=4))
        return json_data

    @classmethod
    def __request_sub(cls, query):
        response = requests.get(
            CalilService.CALIL_BASE_URL,
            params=query)
        return response


class CalilQuery(object):

    @classmethod
    def __set_common(cls, query):
        query.set('appkey', os.environ['CALIL_APP_KEY'])
        query.set('format', 'json')
        return query

    @classmethod
    def adjust_first_query(cls, query):
        query = CalilQuery.__set_common(query)
        query.set('callback', 'no')
        return query.dict()

    @classmethod
    def adjust_next_query(cls, query):
        query = CalilQuery.__set_common(query)
        return query.dict()


class CalilBook(object):

    def __init__(self, isbn, json):
        self.isbn = isbn
        self.reserveurl = json.get('reserveurl', '')
        self.libkey = json.get('libkey', '')
        self.id = self.reserveurl.split('=')[-1]
        self.kbot_reserve_url = 'https://' + os.environ['MY_SERVER_NAME'] + '/kbot/library/reserve?book_id='

        self.log()

    def log(self):
        Log.info('isbn : ' + self.isbn)
        Log.info('reserveurl : ' + self.reserveurl)
        Log.info('libkey : ' + str(self.libkey))
        Log.info('id : ' + self.id)
        Log.info('kbot_reserve_url : ' + self.kbot_reserve_url)

    def get_text_message(self):
        return Message.create_text_by_object(self)
