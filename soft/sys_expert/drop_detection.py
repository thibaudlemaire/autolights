#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:20:10 2017

@author: Jane
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import librosa
import scipy.fftpack as scfft
from scipy.signal import *

    #OPEN FILE
filename ='Khaer - Chapter 1-shorter.wav'

fe, signal = wavfile.read(filename) 



f=fe
signal = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
#time =np.arange(len(signal))*1.0/fe  # on recalibre l'échelle des temps


plt.plot(np.arange(len(signal))*1.0/fe, signal)
time =np.arange(len(signal))*1.0/fe

    ## ÉCHANTILLONNAGE

def ech_function(sound, temps, ech) : 
    sig_ech= []
    time_ech= []
    i=0
    echantillonnage =ech
    while (i<len(sound)) :
        sig_ech.append(sound[i])
        time_ech.append(temps[i])
        i= i + echantillonnage
    return time_ech, sig_ech



plt.figure()             
plt.plot(np.arange(len(signal))*1.0/fe, signal, 'r')
#décale de 4ms l'échantillonnage 200
               
    #CALCUL DE L'ÉNERGIE
def calcul_energie(signal,a) :
    ech=len(signal)
    energie = np.zeros(ech)
    energie[0]= signal[0]
    n=0
    for n in range (1, ech):
        energie[n]=a*energie[n-1]+ (1.0-a)*(signal[n]**2)
    return energie




energie= calcul_energie(signal, 0.99995)
echantillonnage =1800
time, energie = ech_function(energie, time, echantillonnage)
fe=fe*1.0/echantillonnage

energie=energie/max(energie)
energie =lfilter(np.hanning(100),1,energie)
plt.figure()
plt.plot(time, energie, 'g')

"""
    #dérivation
N=4

derivee = np.zeros(len(time))

#le premier n pour lequel on calcule la dérivée est celui N points après le début
for p in range (0,N): #va jusqu'à N-1
    derivee[2*N]=derivee[2*N]+ energie[2*N-p] - energie[2*N-p-N]
    
    #on a d[2N]

#on calcule ceux d'après par récurrence

for n in range (2*N, len(energie)-1) :#faire minus one
    derivee[n+1] = derivee[n] + energie[n-(2*N-1)] + energie[n+1] -2*energie[n-(N-1)]
    #derivee[n+1] = derivee[n] + energie[n-(2*N-1)] + energie[n+1] -2*energie[n-(N-1)]
    #derivee[n+1] = derivee[n] -energie[n-(N-1)]+ energie[n+1] + energie[n-N] - energie[n +1 -(2*N-1)] 

plt.figure()    
plt.plot(time, derivee, color = 'r')

energie=derivee
"""
a=1
derivee = np.diff(energie, a)
plt.figure()
plt.plot(time[a:], derivee[a:])


    #detection de creux
den = lfilter([+1,-1], 1, energie)
den = np.sign(den)
dden = lfilter([+1,-1], 1, den)
ind = np.nonzero(dden==2)
ind=np.array(ind)
time=np.array(time)
plt.figure()
plt.plot(time[ind], energie[ind], 'o')

creux = np.nonzero(energie[ind]<- -10)



drops =[]
creux = energie[ind][0]
creux_time = time[ind]
i=5
k=0
test= True
for i in range (len(creux)-4) :
    k=1
    for k in range (5) :
        if (creux[i]>creux[i-k] or creux[i]>creux[i+k]) :
            test = False
    k=1
    if (test) :
        drops.append(ind[0][i])
        print ("there is a drop at " +  str(ind[0][i]*1.0/fe))
    test= True
    

drops_final=[]
l=0
for l in range (len(drops)) :
    if (drops[l]-1.0*fe > 0 and drops[l]-1 <len(energie)) :
        energie_before = sum(energie[int(drops[l]-1.0*fe):drops[l]-1])*1.0/(fe+1)
        energie_after = sum(energie[drops[l]+1:int(drops[l]+1.0*fe)]*1.0/(fe+1))
        if energie_before < energie_after * 0.7 :
            drops_final.append(drops[l]*1.0/fe)  





"""
j=complex(0,1)


def idealFilter(n,fe):
    h=[0]*n
    h[0]=0
    for i in range(1,n):
        h[i]=(fe/i*np.cos(fe*np.pi*i)-1/(np.pi*i**2)*np.sin(fe*np.pi*i))
    return h



realFilter=lfilter(idealFilter(13071,fe),1,np.hanning(13071))

plt.plot(time, lfilter(realFilter, 1, energie))


    # on découpe en frames

def frame_cut(sound, frame_time) :
    frame_length = int(frame_time*fe)
    frames = []
    i =0
    while (i<len(signal)-10) :
        frames.append(sound[i:i+frame_length])
        i = i + int(frame_length/2)
    return frames    
        
frames = frame_cut(signal,0.010)

plt.figure()
plt.plot(np.linspace(0,0.01,len(frames[-1])), frames[-1])

    #CALCUL DE LA TFTD DE CE SIGNAL
sound=frames[0]
tftd = scfft.fft(sound)
freq = scfft.fftfreq(len(sound),1.0/fe)

tftdmel=[0]*int(1127*np.log(1+len(tftd)/700))
for i in range (len(tftd)):
    tftdmel[int(1127*np.log(1+i/700))]=tftd[i]


tftd_mel=[0]*int(700*(np.exp(len(tftd)*1.0/1127)-1))
for i in range (int(700*(np.exp(len(tftd)*1.0/1127)-1))) :
    tftd_mel[i] =tftd[int(700*(np.exp(i*1.0/1127)-1))]

plt.figure()
plt.plot(freq, tftd)

plt.figure()
plt.plot(freq[0:len(tftd_mel)], tftd_mel)

"""



"""
    #rééchantillonnage
#on a à ce point fe/180 = 441hz pour fe = 44100 hz
echantillonnage = 100
time, derivee= ech_function(derivee, time, echantillonnage)
fe=fe/echantillonnage
plt.figure()
plt.plot(time, derivee, color = 'b')
"""


"""
    #dérivation
N=10

derivee = np.zeros(len(time))

#le premier n pour lequel on calcule la dérivée est celui N points après le début
for p in range (0,N): #va jusqu'à N-1
    derivee[2*N]=derivee[2*N]+ energie[2*N-p] - energie[2*N-p-N]
    
    #on a d[2N]

#on calcule ceux d'après par récurrence

for n in range (2*N, len(energie)-1) :#faire minus one brooo
    derivee[n+1] = derivee[n] + energie[n-(2*N-1)] + energie[n+1] -2*energie[n-(N-1)]
    #derivee[n+1] = derivee[n] + energie[n-(2*N-1)] + energie[n+1] -2*energie[n-(N-1)]
    #derivee[n+1] = derivee[n] -energie[n-(N-1)]+ energie[n+1] + energie[n-N] - energie[n +1 -(2*N-1)] 

plt.figure()    
plt.plot(time, derivee, color = 'r')

energie=derivee
"""








