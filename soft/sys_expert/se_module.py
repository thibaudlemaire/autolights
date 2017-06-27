#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
from threading import Thread
from sys_expert.bpm_detection import BpmDetector
from sys_expert.drop_detection import DropDetector


# This class provide a thread for the SE module
class SeModule(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.audio_queue = queue.Queue() # Audio frames FIFO
        self.bpm_detect_queue = queue.Queue() # FIFO for BPM Detector
        self.drop_detect_queue = queue.Queue() # FIFO for Drop Detector
        self.bpm_detector = BpmDetector(self.bpm_detect_queue, manager)
        self.drop_detector = DropDetector(self.drop_detect_queue, manager)

    # Thread processing System Expert
    def run(self):
        logging.info("Starting System Expert thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        self.bpm_detector.start()
        self.drop_detector.start()
        self.bpm_detector.join()
        self.drop_detector.join()

    # Method called to stop the thread
    def stop(self):
        self.bpm_detector.stop()
        self.drop_detector.stop()


    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        self.bpm_detect_queue.put(audio_frames)  # Put new frames in the FIFO
        self.drop_detect_queue.put(audio_frames)  # Put new frames in the FIFO