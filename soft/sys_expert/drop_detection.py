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

from scipy.io import wavfile
  

    #OPEN FILE
filename ='Avicii drop.wav'

fe, signal = wavfile.read(filename) 



f=fe
signal = signal[:,1] # nsd.shape[1]==2, on prend que un des canaux
#time =np.arange(len(signal))*1.0/fe  # on recalibre l'échelle des temps


#plt.plot(np.arange(len(signal))*1.0/fe, signal)
time =np.arange(len(signal))*1.0/fe

               
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
echantillonnage =100
time, energie = time[::echantillonnage], energie[::echantillonnage]
fe=fe*1.0/echantillonnage

energie=energie/max(energie)
energie =lfilter(np.hanning(100),1,energie)
plt.figure()
plt.plot(time, energie, 'g')


    #detection de creux
def detection_creux(signal) :
    den = lfilter([+1,-1], 1, signal)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==2)
    return np.array(ind) -1
            

time=np.array(time)
ind=detection_creux(energie)
plt.plot(time[ind], energie[ind], 'o')


#creux = np.nonzero(energie[ind]<- -10)

def find_peak(energie, temps,f) :
    den = lfilter([+1,-1], 1, energie)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==2)
    ind=np.array(ind) -1
    list_peaks = []
    ech = temps*f
    i = 0
    for i in range (len(ind[0])) :
        peak = True
        k=0
        if (i==0) :
            peak=False
        while (k<len(ind[0]) and ind[0][k]-ind[0][i]<=ech) :
            if (abs(ind[0][i]-ind[0][k])<=ech) :
                if (energie[ind[0][i]] > energie[ind[0][k]]) :
                    peak = False
            k=k+1
        if (peak == True) :
            list_peaks.append(ind[0][i]*1.0)#/fe)
        peak = False
    return list_peaks

peaks = find_peak(energie, 2.0,fe)
        


    ### filtre de dérivation

j=complex(0,1)    
def derivateur(M,b):
     n=np.arange(-M+1,M)
     n[M-1]=1
     h=(-2*np.pi)*((np.sin(np.pi*n*b*2)/2)-np.pi*b*n*np.cos(np.pi*n*b*2))/((np.pi**2)*n**2)
     h[M-1]=0
     return h*hamming(2*M-1)
 
"""
ind = np.nonzero(dden==2)
ind=np.array(ind) -1
time=np.array(time)

plt.plot(time[ind], energie[ind], 'o')
"""

dtnf =lfilter(derivateur(10, 0.2), 1, energie)

dtnf_ind = np.nonzero(dtnf>0)
dtnf_ind = np.array(dtnf_ind)
dtnf=dtnf[dtnf_ind][0]
time=time[dtnf_ind][0]
plt.figure()
plt.plot(time,dtnf)



    ### détecteurs de pics
def detection_pics(signal) :
    den = lfilter([+1,-1], 1, signal)
    den = np.sign(den)
    dden = lfilter([+1,-1], 1, den)
    ind = np.nonzero(dden==-2)
    return np.array(ind) -1

ind_pics = detection_pics(dtnf)

plt.plot(time[ind_pics][0], dtnf[ind_pics][0], 'o')





a = librosa.beat.beat_track(y=signal, sr=f*echantillonnage)
def piccount_drop(indpics,ipic,n,T,f) :
    #ipic = indpics[ipic]
    ech=int(f*T*1.0/n)
    compte=[0]*n
    k=0
    while ( k<n ) :
        i=0
        while (indpics[i] <= ipic-k*ech) :
            if (ipic-(k+1)*ech<indpics[i]) :
                compte[k]=compte[k]+1
            i=i+1
        k=k+1
    return compte

        
"""        
        compte[k]=np.nonzero(ipic-(k+1)*ech <indpics)
        print(compte[k][0])
        compte[k]=np.nonzero(indpics[compte[k][0]]<ipic-k*ech)
        print(compte[k][0])
        #compte[k]=len(compte[k])
        k=k+1
        ipic=ipic-ech
"""
def densite_pic(signal, time, T,fe ) :
    ech=T*fe
    #pics_amplitude,pics_position = find_pics(signal, time)[0:1] #retourne les positions des pics
    pics_position = ind_pics[0]
    densite = []
    liste=[0]*len(signal)
    for i in range (len(pics_position)) :
        liste[pics_position[i]]=1
    print(liste)
    densite = np.array([sum(liste[k*ech:(k+1)*ech]) for k in range (int(len(time)/(fe*T))) ])
    return densite

pipi = densite_pic(signal, time, 1,fe )
pics_count = piccount_drop(ind_pics[0], 6190, 2, 6, fe)



    ##low pass filter
    
b,a = iirfilter(N=2,Wn=[100.0/(fe*echantillonnage)*2],btype="lowpass",ftype="butter")
#freq de coupure fc/fe=0.1 si Wn= [0.1¨*2]
#plt.figure()
#plt.plot(np.arange(len(signal))*1.0/(fe*echantillonnage))

w,h=freqz(b,a,4096)
#plt.figure()
#plt.plot(w, abs(h))


energie_low = calcul_energie(lfilter(b,a, signal),0.99995)
time_low = np.arange(len(signal))*1.0/(fe*echantillonnage)
plt.figure()
plt.plot(time_low,energie_low)




    ##passe haut
    
b1,a1 = iirfilter(N=2,Wn=[5000.0/(fe*echantillonnage)*2],btype="highpass",ftype="butter")

signal_high