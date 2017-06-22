
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:55:20 2017

@author: Jane
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import librosa

filename ='drop_6.wav'
#mambo number five commence après 8*fe échantillons
## ouverture d'une fichier wav et création de l'array de temps correspondant

fe, snd = wavfile.read(filename) 
ech = snd.shape[0] #nombre d'échantillons que l'on possède
signal = snd[:,1] # nsd.shape[1]==2, on prend que un des canaux
time =np.arange(len(signal))/fe  # on recalibre l'échelle des temps

#wavfile.write('Catpeur16.wav', int(fe) , signal[250000:])


    ##BPM
a = librosa.beat.beat_track(y=signal[8*fe: 8*fe + int(0.2*fe*5)], sr=fe)#, onset_envelope=None, hop_length=512, start_bpm=120.0, tightness=100, trim=True, bpm=None, units='frames')
#il faut prendre au moins 4 fois le temps par beat pour avoir le même BPM sur l'ensemble du signal

print("the BPM is " + str(a[0]))

    ##MFCC
mfcc = librosa.feature.mfcc(y=signal[8*fe:], hop_length=int(0.010*sr))#, n_mfcc =  20)
