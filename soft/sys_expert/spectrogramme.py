#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:44:26 2017

@author: Jane
"""




from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import librosa
import scipy.fftpack as scfft
from scipy.signal import *
import matplotlib
from scipy.io import wavfile
  

filename ='Avicii drop.wav'

fe, signal = wavfile.read(filename) 



f=fe
signal = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
#time =np.arange(len(signal))*1.0/fe  # on recalibre l'échelle des temps

def calcul_energie(signal,a) :
    ech=len(signal)
    energie = np.zeros(ech)
    energie[0]= signal[0]
    n=0
    for n in range (1, ech):
        energie[n]=a*energie[n-1]+ (1.0-a)*(signal[n]**2)
    return energie




energie= calcul_energie(signal, 0.99995)

plt.plot(np.arange(len(signal))*1.0/fe, energie)
time =np.arange(len(signal))*1.0/fe

plt.figure()              
#Pxx, freqs, bins, im = 
plt.specgram(signal, NFFT=2048,   Fs=fe, noverlap=3.0*2048/4)
plt.show()