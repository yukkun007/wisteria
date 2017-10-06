#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from kbot.log import Log

class HtmlPages(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        Log.info('webdriver.PhantomJS start')

    def finalize(self):
        self.driver.quit()
        Log.info('webdriver.PhantomJS quit')

    def fetch_login_page(self, login_url, user):
        self.__login(login_url, user)
        html = self.driver.page_source.encode('utf-8')
        return html

    def yoyaku(self, login_url, user, url):
        self.__login(login_url, user)
        self.driver.get(url)
        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # self.driver.save_screenshot("login.png")
        # element = self.driver.find_element_by_id('library')
        element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "library")))
        select = Select(element)
        select.select_by_index(10)
        # self.driver.save_screenshot("select.png")
        # time.sleep(5)
        # submit = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "InForm")))
        submit = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "reg")))
        submit.click()
        # time.sleep(5)
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # self.driver.save_screenshot("button.png")
        submit = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "chkRb")))
        submit.click()
        # time.sleep(5)
        # self.driver.save_screenshot("finish.png")
        return self.driver.current_url

    def __login(self, login_url, user):
        self.driver.get(login_url)

        # ログインボタン押下
        uid      = self.driver.find_element_by_name('usercardno')
        password = self.driver.find_element_by_name('userpasswd')
        uid.send_keys(user.id)
        password.send_keys(user.password)
        self.driver.find_element_by_name('Login').click()
        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # driver.save_screenshot("login.png")

