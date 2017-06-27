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
BUFFER_SIZE = 40           # Number of frames to store in the buffer (40 -> 1s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
ENERGY_SILENCE_THRESHOLD = 0      # RMS Energy threshold under which sound is concidered as silence
ENERGY_CHANGE_THRESHOLD = 0
TUNING_CHANGE_THRESHOLD = 0

# This class provide a thread for the SE module
class PitchEnergyDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.last_energy = 0
        self.last_tuning = 0
        self.counter = 0
        self.frames = None
        self.manager = manager

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting Pitch and RMS Energy detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                energy_raw = librosa.feature.rmse(y=self.frames)
                new_energy = int(np.mean(energy_raw))
                if np.abs(self.last_energy - new_energy) > ENERGY_CHANGE_THRESHOLD:
                    self.last_energy = new_energy
                    self.manager.new_energy(new_energy)
                new_tuning = int(50+100*librosa.estimate_tuning(y=self.frames, sr=SAMPLE_RATE))
                if np.abs(self.last_tuning - new_tuning) > TUNING_CHANGE_THRESHOLD:
                    self.last_tuning = new_tuning
                    self.manager.new_tuning(new_tuning)
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
