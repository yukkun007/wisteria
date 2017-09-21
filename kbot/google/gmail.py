#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import json
from kbot.google.gmail_api import GmailApi

class GMail(object):
    def __init__(self, root_dir):
        self.root_dir     = root_dir
        self.storage_path = '/tmp/st_test.txt'
        self.secret_path = '/tmp/sc_test.txt'


    def send_message(self, to, subject, message):
        st = open(self.storage_path, 'w')
        storage = os.environ['GMAIL_AUTH_STORAGE']
        st.write(storage)
        st.close()

        # sc = open(self.secret_path, 'w')
        # secret = os.environ['GMAIL_CLIENT_SECRET']
        # sc.write(secret)
        # sc.close()
        # secret_file = open(self.secret_path)
        auth_info   = '' #json.load(secret_file)

        # 初回実行時は認証が求められます
        api = GmailApi(auth_info, self.storage_path)

        user = 'me'
        message = api.createMessage(user, to, subject, message)
        api.sendMessage(user, message)

    def send_message_multi(self, tos, subject, message):
        for to in tos:
            self.send_message(to, subject, message)

