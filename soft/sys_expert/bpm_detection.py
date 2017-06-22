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
BUFFER_SIZE = 200           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module


# This class provide a thread for the SE module
class BpmDetector(Thread):
    def __init__(self, audio_frames):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.last_bpm = 120
        self.counter = 0
        self.frames = None

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting BPM detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                new_bpm_raw = librosa.beat.beat_track(y=self.frames, sr=SAMPLE_RATE)[0]
                new_bpm = round(new_bpm_raw)
                if new_bpm != self.last_bpm:
                    self.last_bpm = new_bpm
                    logging.info("New BPM : " + str(new_bpm))
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
