# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import requests

class Gyazo(object):

    URL                = 'https://upload.gyazo.com/api/upload'

    def __init__(self):
        pass

    def upload(self, path):
        image    = open(path, 'rb')
        files    = {'imagedata': ('filename.jpg', image, 'image/jpeg')}
        data     = {'access_token': os.environ['GYAZO_ACCESS_TOKEN']}
        response = requests.post(Gyazo.URL, files=files, data=data)
        url      = response.json()['url']

        return url

