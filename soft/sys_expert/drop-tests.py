#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:24:54 2017

@author: Jane
"""

import bibliotheque.drop as dr

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import librosa
import scipy.fftpack as scfft
from scipy.signal import *
from scipy.io import wavfile
  

    #OPEN FILE
filename ='./wav/Avicii drop.wav'
fe, signal = wavfile.read(filename) 
signal = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
time =np.arange(len(signal))*1.0/fe

ampl_pics, ind_pics = dr.find_pic(signal)
sig_env, time, fe =dr.detect_env(signal, time, fe)
plt.figure()
plt.plot(time, sig_env)


plt.plot(time, sig_env, 'g')
#plt.plot(time[ind_pics], sig_env[ind_pics],'o')
liste_densites = dr.densite_pic(signal, time, 0.1 ,fe )

