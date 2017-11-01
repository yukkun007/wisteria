# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import logging


class Log(object):

    def info(message):
        logger = logging.getLogger('command')
        logger.info(message)

    def logging_exception(e):
        Log.info('type:' + str(type(e)))
        Log.info('args:' + str(e.args))
        # Log.info('message:' + e.message)
        Log.info('e:' + str(e))
