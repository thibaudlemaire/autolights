#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
from threading import Thread


# This class provide a thread for the SE module
class SeModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False  # Stop flag

    # Thread processing System Expert
    def run(self):
        logging.info("Starting System Expert thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            None
            # Write here non-blocking code (use timeout...)

    # Method called to stop the thread
    def stop(self):
        self.terminated = True

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        None
