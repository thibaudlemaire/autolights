#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:24:54 2017

@author: Jane
"""

import bibliotheque.drop as dr


import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *
from scipy.io import wavfile
import librosa

    #OPEN FILE
filename ='./wav/techno.wav'

fe, signal = wavfile.read(filename) 
sig = np.array(signal[:,1]) # nsd.shape[1]==2, on prend que un des canaux
sig=sig.astype(np.float)
time =np.arange(len(signal))*1.0/fe
plt.close("all")
#energie, temps, f = dr.detect_env(sig, time, fe)

            

print(dr.sync_test(sig,44100, [0], 0)

#print(dr.sync_test(sig,44100, [0],[0]*198))
#energie, time, fe = dr.detect_env(sig, time, fe)
#der, time = dr.derivateur(energie, time,10,0.2)
#plt.plot(time, der)

































"""
#plt.plot(time1[40000+int(0.02*44100/2):40000+int(0.02*44100/2)],sig[40000+int(0.02*44100/2):40000+int(0.02*44100/2)])

time1 = time1[int(6417-fe*0.01):int(6417+0.01*fe)]
signal1 = signal1[int(6417-fe*0.01):int(6417+0.01*fe)]
plt.figure()
plt.plot(time1, signal1)


energie2, time2, fe = dr.detect_env(signal1, time1, fe)
plt.figure()
plt.plot(time2, energie2)



#a =  is_creux(signal)
energie2, time2, fe = dr.detect_env(signal1, time1, fe)
plt.figure()
plt.plot(time2,energie2)


a = dr.detection_creux(energie2)


plt.plot(time2[a], energie2[a], 'o')

b = dr.is_creux(signal1, time1 ,fe, 2)


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

filename ='./wav/Avicii drop.wav'
fe, signal = wavfile.read(filename) 
signal = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
time =np.arange(len(signal))*1.0/fe

plt.figure()
plt.plot(time, signal)
##calcule enveloppe et affiche les creux
sig_env, time, fe =dr.detect_env(signal,time, fe, 0.01)

plt.figure()
plt.plot(time, sig_env)


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
