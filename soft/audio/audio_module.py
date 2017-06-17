#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
from threading import Thread

from tools.listeners import Listeners


# This class provide a thread for the audio module
class AudioModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.listeners = Listeners()  # Create the listeners list of functions to call on update

    # Thread recording audio in
    def run(self):
        logging.info("Starting audio_record thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            None
            # Write here non-blocking code (use timeout...)

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
