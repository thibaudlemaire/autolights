#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: thibaud
"""
import alsaaudio
import numpy as np

_SAMPLES_PER_FRAME = 256

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL, device="hw:1")

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(_SAMPLES_PER_FRAME)

while True:
    # Read data from device
    l,data = inp.read()
    if l == _SAMPLES_PER_FRAME:
        # Create a np.ndarray (= a frame) to put samples
        array = np.empty(_SAMPLES_PER_FRAME, dtype=float)
        # Conversion of each sample in float
        for i in range(l):
            integer = int.from_bytes(data[2*i:2*i+2], byteorder='little', signed=True)
            fl = float(integer)/2**15
            array.put(i, fl)
        print(array)
