#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
import time
import librosa
import numpy as np
from scipy import stats
from sklearn.externals import joblib
from threading import Thread

# Constants
BUFFER_SIZE = 400           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
MODEL_PATH = 'machine_learning/data/SVClin32bits_names.pkl'         # SVM Model
MFCC_COUNT = 20             # Number of MFCC


# This class provide a thread for the ML module
class MlModule(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.queue = queue.Queue()  # Contain 5ms frames
        self.current_gender = None
        self.counter = 0
        self.frames = None
        self.manager = manager
        self.svm = joblib.load(MODEL_PATH)

    # Thread processing ML
    def run(self):
        logging.info("Starting Gender detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            new_frame = self.queue.get()  # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                logging.debug('Calcul des MFCC')
                stft = np.abs(librosa.stft(self.frames, n_fft=2048, hop_length=512))  # Èventuellement librosa.core.stft
                mel = librosa.feature.melspectrogram(sr=SAMPLE_RATE, S=stft ** 2)
                del stft
                f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)  # Èventuellement librosa.core.power_to_db
                #features = features = np.mean(f, axis=1)
                features = self.feature_stats(f)
                #mfcc = librosa.feature.mfcc(self.frames, SAMPLE_RATE, n_mfcc=MFCC_COUNT)
                #features = self.feature_stats(mfcc).reshape(1,-1)
                #features = np.mean(mfcc, axis=1).reshape(1,-1)
                logging.debug("Detection du genre")
                result = self.svm.predict(features.reshape(1,-1))
                if result[0] != self.current_gender:
                    self.current_gender = result[0]
                    self.manager.new_gender(result[0])
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.queue.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16))  # Release blocking getter

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        self.queue.put(audio_frames)  # Put new frames in the FIFO

    def feature_stats(self, values):
        '''features = np.mean(values, axis=1)  # mean
        features = np.concatenate((features, np.std(values, axis=1)))  # std
        features = np.concatenate((features, np.array(stats.skew(values, axis=1))))  # skew
        features = np.concatenate((features, np.array(stats.kurtosis(values, axis=1))))  # kurtosis
        features = np.concatenate((features, np.median(values, axis=1)))  # median
        features = np.concatenate((features, np.min(values, axis=1)))  # min
        features = np.concatenate((features, np.max(values, axis=1)))  # max'''
        features = np.array(stats.kurtosis(values, axis=1))     # kurtosis
        features = np.concatenate((features, np.max(values, axis=1))) # max
        features = np.concatenate((features, np.mean(values, axis=1))) # mean
        features = np.concatenate((features, np.median(values, axis=1))) # median
        features = np.concatenate((features, np.min(values, axis=1))) # min
        features = np.concatenate((features, np.array(stats.skew(values, axis=1)))) # skew
        features = np.concatenate((features, np.std(values, axis=1))) # std
        return features
