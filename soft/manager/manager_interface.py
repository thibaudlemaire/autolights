#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 09:10:13 2016

@author: thibaud
"""
import logging

MANAGER = None


# Function called to link the interface with the manager Class
def init(manager):
    global MANAGER
    MANAGER = manager


# Funciton called to update BPM
def new_bpm(bpm):
    if MANAGER: MANAGER.new_bpm(bpm)
    else: logging.info("New BPM !")

def drop():
    if MANAGER:
        MANAGER.drop()
    else:
        logging.info("Drop !")
