#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
from threading import Thread
import time


# This class provide a thread for the Manager module
class ManagerModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.current_bpm = 120

    # Thread linking audio features to light features
    def run(self):
        logging.info("Starting Manager thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            time.sleep(1)
            # Write here non-blocking code (use timeout...)

    # Method called to stop the thread
    def stop(self):
        self.terminated = True

    def new_bpm(self, new_bpm):
        self.current_bpm = new_bpm
        logging.info("New BPM : " + str(new_bpm))

    def drop(self):
        logging.info("Drop ! ")

