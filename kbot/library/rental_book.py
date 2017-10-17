#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from dateutil.parser import parse

class RentalBook(object):

    def __init__(self, name, expire_date_text, can_extend_period, extend_period_button_name):
        self.name                      = name
        self.expire_date               = parse(expire_date_text).date()
        self.expire_date_text          = expire_date_text
        self.can_extend_period         = can_extend_period
        self.extend_period_button_name = extend_period_button_name

    def is_expired(self):
        return self.is_expire_in_xdays(-1)

    def is_expire_in_xdays(self, xday_before):
        today = date.today()
        if self.expire_date - today <= timedelta(days=xday_before):
            return True
        return False

    def get_expire_text_from_today(self):
        today = date.today()
        remain_days = (self.expire_date - today).days

        if remain_days == 1:
            text = ' (明日ﾏﾃﾞ)'
        elif remain_days == 0:
            text = ' (今日ﾏﾃﾞ)'
        elif remain_days < 0:
            text = " (延滞)"
        else:
            text = " (あと{0}日)".format(remain_days)

        return text

    def to_string(self):
        string = "name:{0} expire_date:{1} expire_date(text):{2} can_extend_period:{3} extend_period_button_name:{4}".format(
            self.name,
            self.expire_date,
            self.expire_date_text,
            self.can_extend_period,
            self.extend_period_button_name
        )
        return string

