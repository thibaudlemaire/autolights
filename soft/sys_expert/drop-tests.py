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

##calcule enveloppe et affiche les creux
sig_env, time1, f =dr.detect_env(signal, time, fe)
plt.figure()
plt.plot(time1, sig_env)

en_creux = dr.detection_creux(sig_env)
sel_creux = dr.is_creux(sig_env) #indices des creux du signal
plt.plot(time[en_creux], sig_env[en_creux], 'o')




derivee, pic_der, ind_der, time2 = dr.find_pic(sig_env, time1)


plt.figure()
plt.plot(time2,derivee)
plt.plot(time2[ind_der], derivee[ind_der], 'o')
liste_densites = dr.densite_pic_haut(signal, time, 0.1 ,fe )


m = dr.bass_medium(signal, time, fe)

test= dr.no_bass(signal[0:10*fe],m, time, fe)