# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from kbot.image import Image
from kbot.gyazo import Gyazo
from kbot.image_magic import ImageMagic

class TestImage(object):

    def test_image(self):
        url = 'https://thumbnail.image.rakuten.co.jp/@0_mall/book/cabinet/7942/79421478.jpg?_ex=200x200'
        image = Image()
        path = image.download(url)
        print(path)

        image_magic = ImageMagic()
        image_magic.convert(path)

        gyazo = Gyazo()
        gyazo.upload(path)

