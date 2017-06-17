#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""

import logging
import sys

from audio.audio_module import AudioModule
from logger import log
from machine_learning.ml_module import MlModule
from manager.manager_module import ManagerModule
from midi.midi_module import MidiModule
from sys_expert.se_module import SeModule

"""
This is the main script of the autolight project.
It start all threads and wait for the end.
"""


def main():
    # Start logging system
    log.config_logger()

    # Start audio acquisition thread
    logging.info("Building the audio acquisition thread")
    audio_recorder = AudioModule()
    audio_recorder.start()

    # Start MIDI out thread
    logging.info("Building the MIDI controler")
    midi_generator = MidiModule()
    midi_generator.start()

    # Start System Expert module
    logging.info("Building System Expert module")
    se = SeModule()
    se.start()

    # Start Machine Learning module
    logging.info("Building the Machine Learning module")
    ml = MlModule()
    ml.start()

    # Start Manager module
    logging.info("Building the Manager module")
    manager = ManagerModule()
    manager.start()

    # Setup listeners
    audio_recorder.listeners += se.new_audio
    audio_recorder.listeners += ml.new_audio

    try:
        # Join all threads
        manager.join()
        ml.join()
        se.join()
        midi_generator.join()
        audio_recorder.join()
    except KeyboardInterrupt:
        print('Execution interrupted by user, stopping...')
        manager.stop()  # Stop Manager
        manager.join()
        ml.stop()  # Stop ML
        ml.join()
        se.stop()  # Stop SE
        se.join()
        midi_generator.stop()  # Stop Midi
        midi_generator.join()
        audio_recorder.stop()  # Stop Audio
        audio_recorder.join()
        sys.exit(0)  # Finaly, exit


# If main program, start main
if __name__ == "__main__":
    main()
