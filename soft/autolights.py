#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""

import logging
import sys

from audio.audio_module import AudioModule
from machine_learning.ml_module import MlModule
from manager.manager_module import ManagerModule
from midi.midi_module import MidiModule
from sys_expert.se_module import SeModule
from tools import log
from user_interface.web_server import WebServerModule

"""
This is the main script of the autolight project.
It start all threads and wait for the end.
"""

# Constants
WEB_SERVER = True
ML_MODULE = False
SE_MODULE = False
MIDI_MODULE = False
AUDIO_MODULE = False
MANAGER_MODULE = False


# Main function of the project
def main():
    # Start logging system
    log.config_logger()
    logging.info("##### Autolights is starting, hi ! #####")

    # Start audio acquisition thread
    if (AUDIO_MODULE):
        logging.info("Building the audio acquisition thread")
        audio_recorder = AudioModule()
        audio_recorder.start()

    # Start MIDI out thread
    if (MIDI_MODULE):
        logging.info("Building the MIDI controler")
        midi_generator = MidiModule()
        midi_generator.start()

    if (SE_MODULE):
        # Start System Expert module
        logging.info("Building System Expert module")
        se = SeModule()
        se.start()

    if (ML_MODULE):
        # Start Machine Learning module
        logging.info("Building the Machine Learning module")
        ml = MlModule()
        ml.start()

    if (MANAGER_MODULE):
        # Start Manager module
        logging.info("Building the Manager module")
        manager = ManagerModule()
        manager.start()

    if (WEB_SERVER):
        # Start Manager module
        logging.info("Building the Web Server module")
        server = WebServerModule()
        server.start()


    # Setup listeners
    if (AUDIO_MODULE):  audio_recorder.listeners += se.new_audio
    if (ML_MODULE):     audio_recorder.listeners += ml.new_audio

    try:
        # Join all threads
        if (WEB_SERVER):        server.join()
        if (MANAGER_MODULE):    manager.join()
        if (ML_MODULE):         ml.join()
        if (SE_MODULE):         se.join()
        if (MIDI_MODULE):       midi_generator.join()
        if (AUDIO_MODULE):      audio_recorder.join()
    except KeyboardInterrupt:
        logging.info('Execution interrupted by user, stopping...')
        if (WEB_SERVER):
            server.stop()  # Stop Server
            server.join()
        if (MANAGER_MODULE):
            manager.stop()  # Stop Manager
            manager.join()
        if (ML_MODULE):
            ml.stop()  # Stop ML
            ml.join()
        if (SE_MODULE):
            se.stop()  # Stop SE
            se.join()
        if (MIDI_MODULE):
            midi_generator.stop()  # Stop Midi
            midi_generator.join()
        if (AUDIO_MODULE):
            audio_recorder.stop()  # Stop Audio
            audio_recorder.join()
        logging.info("##### All is stopped, bye #####")
        sys.exit(0)  # Finaly, exit


# If main program, start main
if __name__ == "__main__":
    main()
