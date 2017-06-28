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
from sys_expert.energy_detection import EnergyDetector
from sys_expert.pitch_detection import PitchDetector

# This class provide a thread for the SE module
class SeModule(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.bpm_detect_queue = queue.Queue() # FIFO for BPM Detector
        self.energy_detect_queue = queue.Queue()
        self.pitch_detect_queue = queue.Queue()
        self.drop_detect_queue = queue.Queue() # FIFO for Drop Detector
        self.bpm_detector = BpmDetector(self.bpm_detect_queue, manager)
        self.drop_detector = DropDetector(self.drop_detect_queue, manager)
        self.energy_detector = EnergyDetector(self.energy_detect_queue, manager)
        self.pitch_detector = PitchDetector(self.pitch_detect_queue, manager)


    # Thread processing System Expert
    def run(self):
        logging.info("Starting System Expert thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        self.bpm_detector.start()
        self.drop_detector.start()
        self.energy_detector.start()
        self.pitch_detector.start()
        self.bpm_detector.join()
        self.drop_detector.join()
        self.energy_detector.join()
        self.pitch_detector.join()

    # Method called to stop the thread
    def stop(self):
        self.drop_detector.stop()
        self.bpm_detector.stop()
        self.energy_detector.stop()
        self.pitch_detector.stop()

    # Method called by the audio module when new audio frames are available
    def new_audio(self, audio_frames):
        self.bpm_detect_queue.put(audio_frames)  # Put new frames in the FIFO
        self.drop_detect_queue.put(audio_frames)  # Put new frames in the FIFO
        self.energy_detect_queue.put(audio_frames)  # Put new frames in the FIFO
        self.pitch_detect_queue.put(audio_frames)  # Put new frames in the FIFO