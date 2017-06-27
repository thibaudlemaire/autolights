#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:20:10 2017

@author: Jane
"""
import logging
import numpy as np
from threading import Thread
from .bibliotheque.drop import detect_low_freq_event


# Constants
BUFFER_SIZE = 200           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module


# This class provide a thread for the SE module
class DropDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # FIFO Contain 20ms frames
        self.counter = 0
        self.frames = None                  # np.array containing large data frame
        self.manager = manager
        self.seuil = 1E8

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting Drop detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                is_drop, seuil = detect_low_freq_event(self.frames, 1000, 10, SAMPLE_RATE, self.seuil)
                self.seuil = seuil
                if is_drop:
                    self.manager.drop()
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter