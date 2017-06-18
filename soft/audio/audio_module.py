#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import alsaaudio
from threading import Thread
from tools.listeners import Listeners


# This class provide a thread for the audio module
class AudioModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False  # Stop flag
        self.listeners = Listeners()  # Create the listeners list of functions to call on update

        # Open the soundCard in normal (blocking) mode, chanel 2 for mic
        self.input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'Device', 2)

        # Set attributes
        self.input.setchannels(1)                       # Mono
        self.input.setrate(8000)                        # 8000 Hz
        self.input.setformat(alsaaudio.PCM_FORMAT_U8)   # 8 bits
        # Set the number of frames per second
        self.input.setperiodsize(1) # TODO Check if this is efficent. If not, increase value and replace listeners to fill queue in a loop

    # Thread recording audio in
    def run(self):
        logging.info("Starting audio_record thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            # Read data from device, blocking
            l, data = self.input.read()
            # Notify all listening module data new data is available
            self.listeners.notify_event(data)   # TODO Chose a common audio format Float32 ? PCM 8 ? PCM 16 ?
            # TODO Chose where to proccess conversion : this thread, another thread --> speed

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
