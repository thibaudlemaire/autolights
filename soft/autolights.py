#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import logging
import sys
import user_interface.django_config
import django

from user_interface.external_run import DjangoThread
from manager import manager_interface
from audio.audio_module import AudioModule
from machine_learning.ml_module import MlModule
from manager.manager_module import ManagerModule
from midi.midi_module import MidiModule
from sys_expert.se_module import SeModule
from tools import log
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

    # Init Django
    django.setup()

    # Create modules
    logging.info("Building modules")
    if MANAGER_MODULE: manager = ManagerModule()
    if AUDIO_MODULE: audio_recorder = AudioModule()
    if MIDI_MODULE: midi_generator = MidiModule()
    if SE_MODULE: se = SeModule()
    if ML_MODULE: ml = MlModule()
    if WEB_SERVER: server = DjangoThread()

    # Setup listeners
    logging.info("Setting up listeners")
    if SE_MODULE:  audio_recorder.listeners += se.new_audio
    if ML_MODULE:     audio_recorder.listeners += ml.new_audio
    # Register Manager

    if MANAGER_MODULE:
        logging.info("Registering manager")
        manager_interface.init(manager)

    # Start threads
    logging.info("Starting threads")
    if WEB_SERVER: server.start()
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
