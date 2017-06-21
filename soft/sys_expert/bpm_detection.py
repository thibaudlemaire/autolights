#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import librosa
import numpy as np
from threading import Thread

# Constants
BUFFER_SIZE = 345           # Number of frames to store in the buffer
SAMPLE_PER_FRAME = 256      # See audio module
SAMPLE_RATE = 44100         # See audio module

# This class provide a thread for the SE module
class BpmDetector(Thread):
    def __init__(self, audio_frames):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.audio_frames = audio_frames # Contain 5ms frames
        self.last_bpm = 120
        self.frames = np.zeros(BUFFER_SIZE * SAMPLE_PER_FRAME) # Frame buffer

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting BPM detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            # Move old frames left
            self.frames[:SAMPLE_PER_FRAME * (BUFFER_SIZE-1) + 1] = self.frames[SAMPLE_PER_FRAME + 1:]
            # Fill with new frame
            self.frames[SAMPLE_PER_FRAME * (BUFFER_SIZE-1) + 1:] = new_frame
            new_bpm = round(librosa.beat.beat_track(y=self.frames, sr=SAMPLE_RATE))
            if new_bpm != self.last_bpm:
                self.last_bpm = new_bpm
                logging.info("New BPM : " + str(new_bpm))

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.frames.put(np.zeros(SAMPLE_PER_FRAME)) # Release getter
