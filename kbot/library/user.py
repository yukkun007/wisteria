#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class User(object):
    def __init__(self, data_json):
        data = json.loads(data_json)

        self.num      = data['num']
        self.name     = data['name']
        self.id       = data['id']
        self.password = data['password']


