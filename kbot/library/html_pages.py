#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from kbot.log import Log

class HtmlPages(object):
    LIBRALY_HOME_URL = "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWUSERCONF.CSP"

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        Log.info('webdriver.PhantomJS start')

    def finalize(self):
        self.driver.quit()
        Log.info('webdriver.PhantomJS quit')

    def fetch_html(self, user):
        self.driver.get(HtmlPages.LIBRALY_HOME_URL)

        # ログインボタン押下
        uid      = self.driver.find_element_by_name('usercardno')
        password = self.driver.find_element_by_name('userpasswd')
        uid.send_keys(user.id)
        password.send_keys(user.password)
        self.driver.find_element_by_name('Login').click()
        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)

        # driver.save_screenshot("login.png")
        html = self.driver.page_source.encode('utf-8')

        return html


