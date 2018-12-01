#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from kbot.log import Log
from kbot.library.user import User


class HtmlPage(object):
    def __init__(self) -> None:
        Log.info("driver.create/start")
        options = ChromeOptions()
        # 必須
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # エラーの許容
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        # headlessでは不要そうな機能
        options.add_argument('--disable-desktop-notifications')
        options.add_argument("--disable-extensions")
        # UA
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"  # noqa
        options.add_argument("--user-agent=" + user_agent)
        # 言語
        options.add_argument('--lang=ja')
        # 画像を読み込まないで軽くする
        options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = Chrome(options=options)
        Log.info("driver.create/end")

    def __wait(self) -> None:
        WebDriverWait(self.driver, 10, poll_frequency=0.05).until(
            ec.presence_of_all_elements_located
        )

    def __wait_element(self, target):
        element = WebDriverWait(self.driver, 10, poll_frequency=0.05).until(
            ec.presence_of_element_located(target)
        )

        return element

    def __login(self, login_url: str, user: User) -> None:
        Log.info("login..... : user.name={0}, url={1}".format(user.name, login_url))

        self.driver.get(login_url)
        Log.info("----------- 1: [end] driver.get(url)")

        self.__wait()
        Log.info("----------- 2: [end] wait")

        # ログインボタン押下
        uid = self.__wait_element((By.NAME, "usercardno"))
        password = self.__wait_element((By.NAME, "userpasswd"))
        uid.send_keys(user.id)
        password.send_keys(user.password)
        Log.info("----------- 3: [end] sended_keys")
        button = self.__wait_element((By.NAME, "Login"))
        Log.info("----------- 4: [end] button wait")
        button.click()
        Log.info("----------- 5: [end] button.click()")

        # ロードされたかを確認
        self.__wait_element((By.NAME, "FormLEND"))
        Log.info("----------- 6: [end] wait")

    def reserve(self, login_url: str, user: User, url: str) -> str:
        self.__login(login_url, user)

        self.driver.get(url)
        self.__wait()

        element = self.__wait_element((By.ID, "library"))
        select = Select(element)
        select.select_by_index(10)

        submit = self.__wait_element((By.NAME, "reg"))
        submit.click()

        self.__wait()

        submit = self.__wait_element((By.NAME, "chkRb"))
        submit.click()

        current_url = self.driver.current_url

        return current_url

    def fetch_login_page(self, login_url: str, user: User) -> str:
        self.__login(login_url, user)
        Log.info("driver.page_source.encode/start")
        html = self.driver.page_source.encode("utf-8")
        Log.info("driver.page_source.encode/end")
        return html

    def release_resource(self) -> None:
        Log.info("driver.quit/start")
        self.driver.quit()
        Log.info("driver.quit/end")
