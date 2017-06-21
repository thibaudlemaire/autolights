#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
from threading import Thread
from sys_expert.bpm_detection import BpmDetector


# This class provide a thread for the SE module
class SeModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.bpm_detect_queue = queue.Queue() # FIFO for BPM Detector
        self.bpm_detector = BpmDetector(self.bpm_detect_queue)

    # Thread processing System Expert
    def run(self):
        logging.info("Starting System Expert thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        self.bpm_detector.start()
        self.bpm_detector.join()

    # Method called to stop the thread
    def stop(self):
        self.terminated = True

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        self.bpm_detect_queue.put(audio_frames)  # Put new frames in the FIFO
