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
from scipy.signal import *

# Constants
BUFFER_SIZE = 1           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
T=0.25                      #temps de moyennage de l'énergie pour le calcul du seuil
N = int(T/0.023)            #nombre de samples qu'on considère donc
A = np.exp(-1.0/(3*N))      #le "A" correspondant de la moyenne glissante

# This class provide a thread for the SE module
class synchro(Thread):
    def __init__(self, audio_frames):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 5ms frames
        self.counter = 0
        self.frames = None
        self.Ei = 0
        self.M = 0

    # Thread processing synchro
    def run(self):
        logging.info("Synchro")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.audio_frames.get() # Get new frame (blocking)
            new_event_and_moy_raw= bibliotheque.drop.sync_test(new_frame,Ei,M)
            new_event_and_moy = round(new__and_moy_raw)
            new_event= new_event_and_moy[0]
            new_moy= new_event_and_moy[1]
            M=M*A+new_moy*(1-A)
            
            
            self.counter = 0
            
    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
