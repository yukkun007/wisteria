# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import pytest
from kbot.image import Image
from kbot.gyazo import Gyazo
from kbot.image_magic import ImageMagic
from kbot.kbot import KBot


class TestImage(object):
    def setup(self):
        KBot("wisteria")

    def test_image(self):
        url = "https://thumbnail.image.rakuten.co.jp/@0_mall/book/cabinet/7942/79421478.jpg?_ex=200x200"
        image = Image()
        path = image.download(url)

        image_magic = ImageMagic()
        image_magic.convert(path)

        gyazo = Gyazo()
        gyazo.upload(path)

    def test_download_error(self):
        url = "https://thumbnail.image.rakuten.co.jp/hoge"
        image = Image()
        with pytest.raises(Exception):
            image.download(url)

    def test_download_error2(self):
        url = "http://www.google.co.jp"
        image = Image()
        with pytest.raises(Exception):
            image.download(url)
