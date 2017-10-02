# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import requests

class ImageMagic(object):

    def __init__(self):
        pass

    def convert(self, path):
        cmd = "convert {0} -background none -gravity center -extent 302x200 {0}".format(path)
        print(cmd)
        os.system(cmd);

