#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import cherrypy
from ws4py.messaging import TextMessage
from logging.handlers import RotatingFileHandler


class WSConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        cherrypy.engine.publish('websocket-broadcast', TextMessage(msg + '\n'))


def config_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    # First handler : file
    file_handler = RotatingFileHandler('log/activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Second handler : console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    steam_handler.setFormatter(formatter)
    logger.addHandler(steam_handler)

    # Third handler : console
    ws_handler = WSConsoleHandler()
    ws_handler.setLevel(logging.DEBUG)
    ws_handler.setFormatter(formatter)
    logger.addHandler(ws_handler)

    # Fourth handler : file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../log/current.log')
    os.remove(filename)
    current_file_handler = RotatingFileHandler('log/current.log', 'a', 1000000, 1)
    current_file_handler.setLevel(logging.DEBUG)
    current_file_handler.setFormatter(formatter)
    logger.addHandler(current_file_handler)
