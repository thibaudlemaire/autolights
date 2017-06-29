#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import librosa
import math
import time
import numpy as np
from threading import Thread
from .bibliotheque import energie

# Constants
BUFFER_SIZE = 10           # Number of frames to store in the buffer (10 -> 0,25s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
ENERGY_SILENCE_THRESHOLD = 10   # Absolute RMS Energy threshold under which sound is concidered as silence
ENERGY_CHANGE_THRESHOLD = 5     # Delta
BASS_THRESHOLD = 2             # Relative to mean
SWEEP_THRESHOLD = 1.5             # Relative to mean
BREAK_THRESHOLD = 2.2             # Relative
INTER_STATES_TIME = 3           # Time beteween states in state machine
MEAN_NUMBER = 30                # Number of value in slincing means

# States
_STATE_WAITING = 0
_STATE_SWEEP = 1
_STATE_BREAK = 2
_STATE_DROP = 3


# This class provide a thread for the SE module
class EnergyDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.last_energy = 0                # Energy register
        self.last_bass_energy = 0
        self.last_high_energy = 0
        self.bass_mean = 30                 # Means 
        self.high_mean = 15
        self.counter = 0                    # State counter
        self.frames = None                  # Frames buffer
        self.manager = manager              # Pointer to manager
        self.state = 0  # State machine : 0 waiting for sweep, 1 waiting for silence, 2 waiting for bass
        self.state_timestamp = 0            # Time since last state change

    # Thread processing BPM Detection
    def run(self):
        logging.info("Starting RMS Energy detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            if time.time() - self.state_timestamp > INTER_STATES_TIME: self.state = _STATE_WAITING
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                # Global Energy
                energy_raw = librosa.feature.rmse(y=self.frames)    # RMS Energy calculation on full spectrum
                new_energy = np.mean(energy_raw)                    # Mean energy
                if math.isnan(new_energy):
                    logging.warning("Volume trop fort !")
                else:
                    new_energy = int(new_energy)                    # Round energy
                    if np.abs(self.last_energy - new_energy) > ENERGY_CHANGE_THRESHOLD: # Detect a change 
                        self.last_energy = new_energy                                   
                        self.manager.new_energy(new_energy)
                    if new_energy < ENERGY_SILENCE_THRESHOLD:       # Detect a silence
                        self.manager.silence()
                # High frequency energy
                new_high_energy = np.mean(energie.high_freq_energie(self.frames, SAMPLE_RATE))  # RMS Energy on high freq 
                if math.isnan(new_high_energy):
                    logging.warning("Volume trop fort !")
                else:
                    new_high_energy = int(new_high_energy)  
                    self.high_mean = (self.high_mean * MEAN_NUMBER + new_high_energy) / (1 + MEAN_NUMBER)   # Slicing mean calculation
                    if np.abs(self.last_high_energy - new_high_energy) > ENERGY_CHANGE_THRESHOLD:           # Detect high energy change
                        self.last_high_energy = new_high_energy
                        self.manager.new_high_energy(new_high_energy)
                    if new_high_energy > self.high_mean * SWEEP_THRESHOLD:      # Detect a sweep (high energy on high freq)
                        self.manager.sweep()    
                        if self.state == _STATE_SWEEP:                          # Change machine state                      
                            self.state_timestamp = time.time()
                        if self.state == _STATE_WAITING:
                            self.state_timestamp = time.time()
                            self.state = _STATE_SWEEP
                # Bass frequency energy
                new_bass_energy = np.mean(energie.low_freq_energie(self.frames, SAMPLE_RATE))               # RMS Energy on low freq
                if math.isnan(new_bass_energy):
                    logging.warning("Volume trop fort !")
                else:
                    new_bass_energy = int(new_bass_energy)
                    self.bass_mean = (self.bass_mean * MEAN_NUMBER + new_bass_energy) / (1 + MEAN_NUMBER)   # Slicing mean calculation
                    if np.abs(self.last_bass_energy - new_bass_energy) > ENERGY_CHANGE_THRESHOLD:           # Detect low energy change
                        self.last_bass_energy = new_bass_energy
                        self.manager.new_bass_energy(new_bass_energy)
                    if new_bass_energy > self.bass_mean * BASS_THRESHOLD:       # Detect high bass
                        self.manager.bass()
                        if self.state == _STATE_BREAK:                          # Change machine state
                            self.state_timestamp = time.time()
                            self.state = _STATE_DROP
                            self.manager.drop()
                    if new_bass_energy < self.bass_mean / BREAK_THRESHOLD:      # Detect break (low energy on low freq)
                        self.manager.bass_break()
                        if self.state == _STATE_BREAK:                          # Change machine state
                            self.state_timestamp = time.time()
                        if self.state == _STATE_SWEEP:
                            self.state_timestamp = time.time()
                            self.state = _STATE_BREAK
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
