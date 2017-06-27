#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import sys
import django_config        # Init Django context, do not remove !

from audio.audio_module import AudioModule
from machine_learning.ml_module import MlModule
from manager.manager_module import ManagerModule
from midi.midi_module import MidiModule
from sys_expert.se_module import SeModule
from tools import log
from user_interface.external_run import DjangoThread

"""
This is the main script of the autolight project.
It start all threads and wait for the end.
"""

# Constants
WEB_SERVER = True
ML_MODULE = True
SE_MODULE = True
MIDI_MODULE = False
AUDIO_MODULE = True
MANAGER_MODULE = True


# Main function of the project
def main():
    # Start logging system
    log.config_logger()
    logging.info("##### Autolights is starting, hi ! #####")

    # Create modules
    if WEB_SERVER:
        logging.info("Starting Webserver")
        server = DjangoThread()
        server.start()

    logging.info("Building modules")
    audio_recorder = AudioModule()
    midi_generator = MidiModule()
    if MIDI_MODULE: midi_generator.init()
    manager = ManagerModule(midi_generator)
    se = SeModule(manager)
    ml = MlModule(manager)

    # Setup listeners
    logging.info("Setting up listeners")
    if SE_MODULE:  audio_recorder.listeners += se.new_audio
    if ML_MODULE:  audio_recorder.listeners += ml.new_audio

    # Start threads
    logging.info("Starting threads")
    if AUDIO_MODULE: audio_recorder.start()
    if MIDI_MODULE: midi_generator.start()
    if SE_MODULE: se.start()
    if ML_MODULE: ml.start()
    if MANAGER_MODULE: manager.start()

    try:
        # Join all threads
        if WEB_SERVER:        server.join()
        if MANAGER_MODULE:    manager.join()
        if ML_MODULE:         ml.join()
        if SE_MODULE:         se.join()
        if MIDI_MODULE:       midi_generator.join()
        if AUDIO_MODULE:      audio_recorder.join()
    except KeyboardInterrupt:
        logging.info('Execution interrupted by user, stopping...')
        if WEB_SERVER:
            logging.info("Stopping web server...")
            server.stop_server()  # Stop Server
            server.join()
        if MANAGER_MODULE:
            logging.info("Stopping manager...")
            manager.stop()  # Stop Manager
            manager.join()
        if ML_MODULE:
            logging.info("Stopping machine learning...")
            ml.stop()  # Stop ML
            ml.join()
        if SE_MODULE:
            logging.info("Stopping system expert...")
            se.stop()  # Stop SE
            se.join()
        if MIDI_MODULE:
            logging.info("Stopping MIDI...")
            midi_generator.stop()  # Stop Midi
            midi_generator.join()
        if AUDIO_MODULE:
            logging.info("Stopping audio...")
            audio_recorder.stop()  # Stop Audio
            audio_recorder.join()
        logging.info("##### All is stopped, bye #####")
        sys.exit(0)  # Finally, exit


# If main program, start main
if __name__ == "__main__":
    main()
