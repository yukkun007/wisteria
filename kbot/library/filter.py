#!/usr/bin/python
# -*- coding: utf-8 -*-

class Filter(object):

    FILTER_NONE    = "none"
    FILTER_EXPIRED = "expired"
    FILTER_EXPIRE  = "expire"

    def __init__(self, type=FILTER_NONE, xdays=-1):
        self.type  = type
        self.xdays = xdays

