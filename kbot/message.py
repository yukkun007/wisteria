#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader


class Message(object):

    TEMPLATE_ROOT_DIR = 'wisteria/templates/kbot'

    def __init__(self):
        pass

    @staticmethod
    def create(template_path, data):
        env = Environment(loader=FileSystemLoader(Message.TEMPLATE_ROOT_DIR))
        template = env.get_template(template_path)
        message = template.render(data)
        return message

    @staticmethod
    def create_text_by_object(target):
        data = {'object': target}
        message = Message.create('text/' + target.__class__.__name__ + '.tpl', data)
        return message
