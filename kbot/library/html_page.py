#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from kbot.log import Log


class HtmlPage(object):

    @classmethod
    def fetch_login_page(cls, login_url, user):
        driver = HtmlPage.__start()
        HtmlPage.__login(login_url, user, driver)
        Log.info('webdriver: PhantomJS encode/start')
        html = driver.page_source.encode('utf-8')
        Log.info('webdriver: PhantomJS encode/end')
        HtmlPage.__end(driver)
        return html

    @classmethod
    def reserve(cls, login_url, user, url):
        driver = HtmlPage.__start()
        HtmlPage.__login(login_url, user, driver)
        driver.get(url)
        # 待機
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located)
        # driver.save_screenshot("login.png")
        # element = driver.find_element_by_id('library')
        element = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.ID, 'library')))
        select = Select(element)
        select.select_by_index(10)
        # driver.save_screenshot("select.png")
        # time.sleep(5)
        # submit = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "InForm")))
        submit = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'reg')))
        submit.click()
        # time.sleep(5)
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located)
        # driver.save_screenshot("button.png")
        submit = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'chkRb')))
        submit.click()
        # time.sleep(5)
        # driver.save_screenshot("finish.png")

        current_url = driver.current_url
        HtmlPage.__end(driver)

        return current_url

    @classmethod
    def __start(cls):
        Log.info('webdriver: PhantomJS create/start')
        driver = webdriver.PhantomJS()
        Log.info('webdriver: PhantomJS create/end')
        return driver

    @classmethod
    def __end(cls, driver):
        Log.info('webdriver: PhantomJS quit/start')
        driver.quit()
        Log.info('webdriver: PhantomJS quit/end')

    @classmethod
    def __login(cls, login_url, user, driver):
        Log.info(
            'login..... : user.name={0}, url={1}'.format(
                user.name, login_url))

        driver.get(login_url)
        Log.info('-----------:1')
        # 待機
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located)

        Log.info('-----------:2')
        # ログインボタン押下
        # uid      = driver.find_element_by_name('usercardno')
        # password = driver.find_element_by_name('userpasswd')
        uid = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'usercardno')))
        password = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'userpasswd')))
        uid.send_keys(user.id)
        password.send_keys(user.password)
        Log.info('-----------:3')

        # driver.find_element_by_name('Login').click()
        button = WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'Login')))
        button.click()
        Log.info('-----------:4')

        # 待機
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located)
        # ロードされたかを確認
        WebDriverWait(
            driver, 10).until(
            ec.presence_of_element_located(
                (By.NAME, 'FormLEND')))
        # driver.save_screenshot("login.png")
        Log.info('-----------:5')
