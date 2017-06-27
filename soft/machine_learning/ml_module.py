#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
import time
from threading import Thread


# This class provide a thread for the ML module
class MlModule(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.audio_queue = queue.Queue() # Audio frames FIFO
        self.manager = manager

    # Thread processing ML
    def run(self):
        logging.info("Starting Machine Learning thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            time.sleep(1)
            # Write here non-blocking code (use timeout...)

    # Method called to stop the thread
    def stop(self):
        self.terminated = True

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        self.audio_queue.put(audio_frames)  # Put new frames in the FIFO
