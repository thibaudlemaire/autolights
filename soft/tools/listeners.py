#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""


# Class used to manage listeners and to notify them on event
class Listeners(object):
    def __init__(self):
        self.listeners = []

    def add(self, listener):
        self.listeners.append(listener)
        return self

    def remove(self, listener):
        self.listeners.remove(listener)
        return self

    def notify_event(self, earg=None):
        for listener in self.listeners:
            listener(earg)

    __iadd__ = add
    __isub__ = remove
