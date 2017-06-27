#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:55:20 2017

@author: Jane
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
<<<<<<< Updated upstream
import librosa

filename ='drop_6.wav'
#mambo number five commence après 8*fe échantillons
## ouverture d'une fichier wav et création de l'array de temps correspondant

fe, snd = wavfile.read(filename) 
ech = snd.shape[0] #nombre d'échantillons que l'on possède
signal = snd[:,1] # nsd.shape[1]==2, on prend que un des canaux
time =np.arange(len(signal))/fe  # on recalibre l'échelle des temps

#wavfile.write('Catpeur16.wav', int(fe) , signal[250000:])


    ##BPM
a = librosa.beat.beat_track(y=signal[8*fe: 8*fe + int(0.2*fe*5)], sr=fe)#, onset_envelope=None, hop_length=512, start_bpm=120.0, tightness=100, trim=True, bpm=None, units='frames')
#il faut prendre au moins 4 fois le temps par beat pour avoir le même BPM sur l'ensemble du signal

print("the BPM is " + str(a[0]))

    ##MFCC
mfcc = librosa.feature.mfcc(y=signal[8*fe:], hop_length=int(0.010*sr))#, n_mfcc =  20)
=======
from threading import Thread

# Constants
BUFFER_SIZE = 200           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module


# This class provide a thread for the SE module
class BpmDetector(Thread):
    def __init__(self, audio_frames, manager):
        Thread.__init__(self)
        self.terminated = False             # Stop flag
        self.audio_frames = audio_frames    # Contain 20ms frames
        self.last_bpm = 120
        self.counter = 0
        self.frames = None
        self.manager = manager

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
                    self.manager.new_bpm(new_bpm)
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16)) # Release blocking getter
>>>>>>> Stashed changes
