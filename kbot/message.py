#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Template, Environment, FileSystemLoader

class Message(object):

    TEMPLATE_ROOT_DIR = 'wisteria/templates'

    def __init__(self):
        pass

    def create(template_path, data):
        env      = Environment(loader=FileSystemLoader(Message.TEMPLATE_ROOT_DIR))
        template = env.get_template(template_path)
        message  = template.render(data)
        return message

