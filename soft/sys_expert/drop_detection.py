#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:20:10 2017

@author: Jane
"""
import logging
import math
import numpy as np
from threading import Thread
from .bibliotheque import energie

# Constants
BUFFER_SIZE = 20           # Number of frames to store in the buffer (20 -> 0.5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
BASS_ENERGY_CHANGE_THRESHOLD = 0
HIGH_ENERGY_CHANGE_THRESHOLD = 0
BASS_THRESHOLD = 50
SWEEP_THRESHOLD = 60


# This class provide a thread for the SE module
class DropDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # FIFO Contain 20ms frames
        self.counter = 0
        self.frames = None                  # np.array containing large data frame
        self.manager = manager
        self.last_bass_energy = 0
        self.last_high_energy = 0
        self.state = 0 # State machine : 0 waiting for sweep, 1 waiting for silence, 2 waiting for bass
        self.state_timestamp = 0


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

                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter