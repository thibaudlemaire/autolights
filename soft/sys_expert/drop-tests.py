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
filename ='./wav/drop_6.wav'
fe, signal = wavfile.read(filename) 
signal1 = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
time1 =np.arange(len(signal))*1.0/fe
plt.close("all")
plt.figure()
plt.plot(time1, signal1)

#a =  is_creux(signal)
energie2, time2, fe = dr.detect_env(signal1, time1, fe)
plt.figure()
plt.plot(time2,energie2)


a = dr.detection_creux(energie2)


plt.plot(time2[a], energie2[a], 'o')

b = dr.is_creux(signal1, time1 ,fe, 2)





"""
signal2 = signal[0:int(len(signal)/3)]
time2 = time[0:int(len(signal)/3)]

signal3 , time3, fe = dr.detect_env(signal2, time2, fe)
plt.figure()
plt.plot(time3, signal3)
der, a_pics, ind_pics, time = dr.find_pic(signal3, time3)

only_pics =  np.zeros(len(der))
for i in range (len(ind_pics)):
    only_pics[ind_pics[i]]=a_pics[i]

only_pics = np.concatenate([only_pics, np.zeros(len(only_pics))])
autocorr = np.correlate(der, der, mode='full')
autocorr = autocorr[autocorr.size/2:]
plt.figure()
plt.plot(np.arange(len(autocorr)), autocorr)
plt.figure()
auto=np.correlate(only_pics, only_pics, "same")
auto=auto[auto.size/2:]
plt.plot(np.arange(len(auto)), auto)








##calcule enveloppe et affiche les creux
sig_env, time, fe =dr.detect_env(signal,time, fe, 0.01)

plt.figure()
plt.plot(time, sig_env)



sig_auto = librosa.core.autocorrelate(signal, axis=-1)

plt.figure()
plt.plot(time, sig_auto)





sig_env, time, fe =dr.detect_env1(signal,time, fe)
time=time[0::200]
sig_env=sig_env[0::200]
plt.figure()
plt.plot(time, sig_env)


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

"""