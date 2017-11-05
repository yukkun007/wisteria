# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests
from time import sleep
from kbot.log import Log
from kbot.book.book import Book


class Calil(object):

    CALIL_BASE_URL = 'http://api.calil.jp/check'

    def __init__(self):
        pass

    def get_book(self, isbn):
        query = {}
        query['isbn'] = isbn
        query['appkey'] = os.environ['CALIL_APP_KEY']
        query['systemid'] = 'Tokyo_Nerima,Special_Jil'
        query['format'] = 'json'
        query['callback'] = 'no'

        json_dict = requests.get(Calil.CALIL_BASE_URL, params=query).json()
        Log.info(json.dumps(json_dict, sort_keys=True, indent=4))

        while json_dict['continue'] == 1:
            sleep(2)
            query = {}
            query['session'] = json_dict['session']
            json_dict = self.__re_query(query)
            # is_continue = json_dict['continue']

        nerima = json_dict['books'][isbn]['Tokyo_Nerima']
        jil = json_dict['books'][isbn]['Special_Jil']

        status1 = nerima.get('status')
        status2 = jil.get('status')
        if status1 != 'OK' and status1 != 'Cache':
            return []
        if status2 != 'OK' and status2 != 'Cache':
            return []

        book = Book(nerima)
        book.add_reserve_info(jil)

        return book

    def __re_query(self, query):
        query['appkey'] = os.environ['CALIL_APP_KEY']
        query['format'] = 'json'
        response = requests.get(Calil.CALIL_BASE_URL, params=query)

        # ２回目移行のレスポンスはJSONP固定になるため
        json_string = response.text[9:-2]
        json_dict = json.loads(json_string)
        Log.info(json_dict)

        return json_dict
