# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import requests


class Image(object):

    def __init__(self):
        pass

    def download(self, url):
        file_path = self.__make_file_path(url)
        image = self.__download_image(url)
        self.__save_image(file_path, image)
        return file_path

    def __download_image(self, url, timeout=10):
        response = requests.get(url, allow_redirects=False, timeout=timeout)
        if response.status_code != 200:
            e = Exception('HTTP status: ' + response.status_code)
            raise e

        content_type = response.headers['content-type']
        if 'image' not in content_type:
            e = Exception('Content-Type: ' + content_type)
            raise e

        return response.content

    def __make_file_path(self, url):
        file_name = url.rsplit('/', 1)[1].split('?')[0]
        file_path = os.path.join('/tmp/', file_name)
        return file_path

    def __save_image(self, file_path, image):
        with open(file_path, 'wb') as fout:
            fout.write(image)
