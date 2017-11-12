#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from kbot.log import Log


class HtmlPage(object):

    def fetch_login_page(self, login_url, user):
        self.__login(login_url, user)
        Log.info('webdriver: PhantomJS encode/start')
        html = self.driver.page_source.encode('utf-8')
        Log.info('webdriver: PhantomJS encode/end')
        return html

    def reserve(self, login_url, user, url):
        self.__login(login_url, user)
        self.driver.get(url)
        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # self.driver.save_screenshot("login.png")
        # element = self.driver.find_element_by_id('library')
        element = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.ID, 'library')))
        select = Select(element)
        select.select_by_index(10)
        # self.driver.save_screenshot("select.png")
        # time.sleep(5)
        # submit = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "InForm")))
        submit = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'reg')))
        submit.click()
        # time.sleep(5)
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # self.driver.save_screenshot("button.png")
        submit = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'chkRb')))
        submit.click()
        # time.sleep(5)
        # self.driver.save_screenshot("finish.png")

        current_url = self.driver.current_url
        HtmlPage.__end(self.driver)

        return current_url

    def __init__(self):
        Log.info('webdriver: PhantomJS create/start')
        self.driver = webdriver.PhantomJS()
        Log.info('webdriver: PhantomJS create/end')

    def release_resource(self):
        Log.info('webdriver: PhantomJS quit/start')
        self.driver.quit()
        Log.info('webdriver: PhantomJS quit/end')

    def __login(self, login_url, user):
        Log.info(
            'login..... : user.name={0}, url={1}'.format(
                user.name, login_url))

        self.driver.get(login_url)
        Log.info('-----------:1')
        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)

        Log.info('-----------:2')
        # ログインボタン押下
        # uid      = self.driver.find_element_by_name('usercardno')
        # password = self.driver.find_element_by_name('userpasswd')
        uid = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'usercardno')))
        password = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'userpasswd')))
        uid.send_keys(user.id)
        password.send_keys(user.password)
        Log.info('-----------:3')

        # self.driver.find_element_by_name('Login').click()
        button = WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'Login')))
        button.click()
        Log.info('-----------:4')

        # 待機
        WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located)
        # ロードされたかを確認
        WebDriverWait(
            self.driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'FormLEND')))
        # self.driver.save_screenshot("login.png")
        Log.info('-----------:5')
