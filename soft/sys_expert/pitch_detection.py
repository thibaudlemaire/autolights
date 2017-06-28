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
BUFFER_SIZE = 200           # Number of frames to store in the buffer (40 -> 1s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
PITCH_CHANGE_THRESHOLD = 5


# This class provide a thread for the SE module
class PitchDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.last_pitch = 0
        self.counter = 0
        self.frames = None
        self.manager = manager

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting Pitch detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                pitches, magnitudes = librosa.piptrack(self.frames, SAMPLE_RATE)
                # Select out pitches with high energy
                pitches = pitches[magnitudes > np.median(magnitudes)]
                new_tuning = int(50+100*librosa.pitch_tuning(pitches))
                if np.abs(self.last_pitch - new_tuning) > PITCH_CHANGE_THRESHOLD:
                    self.last_pitch = new_tuning
                    self.manager.new_tuning(new_tuning)
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
