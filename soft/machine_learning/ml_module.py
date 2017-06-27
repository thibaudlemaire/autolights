#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
<<<<<<< HEAD
import time
=======
import librosa
import numpy as np
from sklearn.externals import joblib
>>>>>>> machine_learning
from threading import Thread

# Constants
BUFFER_SIZE = 400           # Number of frames to store in the buffer (200 -> 5s)
SAMPLE_PER_FRAME = 1024     # See audio module
SAMPLE_RATE = 44100         # See audio module
MODEL_PATH = 'machine_learning/data/model.pkl'         # SVM Model
MFCC_COUNT = 130            # Number of MFCC


# This class provide a thread for the ML module
class MlModule(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
<<<<<<< HEAD
        self.audio_queue = queue.Queue() # Audio frames FIFO
        self.manager = manager
=======
        self.queue = queue.Queue()  # Contain 5ms frames
        self.current_gender = None
        self.counter = 0
        self.frames = None
        self.manager = manager
        self.svm = joblib.load(MODEL_PATH)
>>>>>>> machine_learning

    # Thread processing ML
    def run(self):
        logging.info("Starting Gender detector")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
<<<<<<< HEAD
            time.sleep(1)
            # Write here non-blocking code (use timeout...)
=======
            new_frame = self.queue.get()  # Get new frame (blocking)
            if self.counter == 0:
                self.frames = new_frame
                self.counter += 1
            elif self.counter >= BUFFER_SIZE:
                self.frames = np.append(self.frames, new_frame)
                mfcc = librosa.feature.mfcc(self.frames, SAMPLE_RATE, n_mfcc=MFCC_COUNT)
                result = self.svm.predict(mfcc)
                if result[0] != self.current_gender:
                    self.current_gender = result[0]
                    self.manager.new_gender(result[0])
                self.counter = 0
            else:
                self.frames = np.append(self.frames, new_frame)
                self.counter += 1
>>>>>>> machine_learning

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        self.audio_frames.put(np.empty(SAMPLE_PER_FRAME, dtype=np.int16))  # Release blocking getter

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
<<<<<<< HEAD
        self.audio_queue.put(audio_frames)  # Put new frames in the FIFO
=======
        self.queue.put(audio_frames)  # Put new frames in the FIFO
>>>>>>> machine_learning
