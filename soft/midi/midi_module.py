#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import queue
import pygame.midi as pm
from threading import Thread

# Constants
_MIDI_OUT_DEVICE_ID = 2
_MIDI_STATUS_NOTE_ON = 0x90     # Official MIDI Status code
_MIDI_STATUS_NOTE_OFF = 0x80
_MIDI_STATUS_CC = 0xb0


# This class provide a thread for the MIDI module
class MidiModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.terminated = False     # Stop flag
        self.message_queue = queue.Queue()

    def init(self):
        pm.init()  # Init Pygame Midi Module
        # Creation of the midi out object
        self.midi_output = pm.Output(_MIDI_OUT_DEVICE_ID)

    # Thread generating MIDI
    def run(self):
        logging.info("Starting MIDI thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            message = self.message_queue.get()     # Get MIDI message in FIFO
            if message[0] == _MIDI_STATUS_CC:
                self.midi_output.write_short(_MIDI_STATUS_CC, message[1], message[2])
            elif message[0] == _MIDI_STATUS_NOTE_ON:
                self.midi_output.note_on(message[1])
            elif message[0] == _MIDI_STATUS_NOTE_OFF:
                self.midi_output.note_off(message[1])

    # Method called to stop the thread
    def stop(self):
        self.terminated = True
        pm.quit()                           # Release midi interface
        self.message_queue.put({0,0,0})     # Release the queue getter if needed

    # Method to send a note_on message
    def note_on(self, note):
        logging.info("Sending note " + str(note) + " on")
        self.message_queue.put({_MIDI_STATUS_NOTE_ON, note})

    # Method to send a note_off message
    def note_off(self, note):
        logging.info("Sending note " + str(note) + " off")
        self.message_queue.put({_MIDI_STATUS_NOTE_OFF, note})

    # Method to send a Control Change (CC) message
    def control_change(self, control, value):
        logging.info("Sending value " + str(value) + " on CC " + str(control))
        self.message_queue.put({_MIDI_STATUS_CC, control, value})
