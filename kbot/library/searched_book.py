#!/usr/bin/python
# -*- coding: utf-8 -*-

from kbot.log import Log


class SearchedBooks():

    def __init__(self):
        pass


class SearchedBook(object):

    def __init__(self):
        Log.info(self.to_string())

    def to_string(self):
        string = ('name:{0} expire_date:{1} expire_date(text):{2} '
                  'can_extend_period:{3} extend_period_button_name:{4}').format(
                      self.name,
                      self.expire_date,
                      self.expire_date_text,
                      self.can_extend_period,
                      self.extend_period_button_name)
        return string
