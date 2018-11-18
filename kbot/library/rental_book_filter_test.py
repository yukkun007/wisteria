#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from kbot.library.rental_book_filter import RentalBookExpireFilter


class TestRentalBookExpireFilter:
    @pytest.fixture()
    def filter1(request):
        return RentalBookExpireFilter()

    def test_xdays_setter(self, filter1):
        with pytest.raises(ValueError):
            filter1.xdays = 1

    def test_convert_xdays(self, filter1):
        value = filter1._RentalBookExpireFilter__convert_xdays("2日")
        assert value == 2
