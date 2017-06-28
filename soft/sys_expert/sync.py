#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:51:30 2017

@author: Jane
"""
import logging
import librosa
import numpy as np
from threading import Thread
from manager import manager_interface
import bibliotheque.drop

# Constants
BUFFER_SIZE = 1           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module


# This class provide a thread for the SE module
class synchro(Thread):
    def __init__(self, audio_frames):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.counter = 0
        self.frames = None
        self.Ei = 0
        self.Di = 0

    # Thread processing BPM Detection
    def run(self):
        logging.info("Synchro")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            new_event_raw = bibliotheque.drop.sync_test(new_frame,Ei, Di)
            
            new_event = round(new_event_raw)
            if new_event :
                
                manager_interface.new_bpm(new_bpm)
            self.counter = 0
            
    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
