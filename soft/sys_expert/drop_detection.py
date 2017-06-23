#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:20:10 2017

@author: Jane
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *


  

    #OPEN FILE
filename ='avicii2.wav'

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



#plt.figure()             
#plt.plot(np.arange(len(signal))*1.0/fe, signal, 'r')
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
echantillonnage =100
time, energie = ech_function(energie, time, echantillonnage)
fe=fe*1.0/echantillonnage

energie=energie/max(energie)
energie =lfilter(np.hanning(100),1,energie)


plt.figure()
plt.plot(time, energie, 'g')



    #detection de creux
den = lfilter([+1,-1], 1, energie)
den = np.sign(den)
dden = lfilter([+1,-1], 1, den)
ind = np.nonzero(dden==2)
ind=np.array(ind) -1
time=np.array(time)

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
            list_peaks.append(ind[0][i]*1.0/fe)
        peak = False
    return list_peaks
peaks = find_peak(energie, 2.0,fe)
        
    ##low pass filter
    
b3,a3 = iirfilter(N=2,Wn=[100.0/(fe*echantillonnage)*2],btype="lowpass",ftype="butter")

#freq de coupure fc/fe=0.1 si Wn= [0.1¨*2]





    ### filtre de dérivation

j=complex(0,1)    
def derivateur(M,b):
     n=np.arange(-M+1,M)
     n[M-1]=1
     h=(-2*np.pi)*((np.sin(np.pi*n*b*2)/2)-np.pi*b*n*np.cos(np.pi*n*b*2))/((np.pi**2)*n**2)
     h[M-1]=0
      
     return h*hamming(2*M-1)

a=calcul_energie(lfilter(b3,a3,signal),0.99995)
filtred_signal=[0]*(len(a)/100+1)
for k in range(len(a)/100):
    filtred_signal[k]=a[100*k]
dtnf =lfilter(derivateur(10, 0.2), 1,energie)
dtnf_ind = np.nonzero(dtnf>0)
dtnf_ind=np.array(dtnf_ind)
dtnf=dtnf[dtnf_ind][0] 
dtnf=dtnf/max(dtnf)



plt.figure()
plt.plot(time[dtnf_ind][0],dtnf)


    ###liste des pics
den2 = lfilter([+1,-1], 1, dtnf)
den2 = np.sign(den2)
dden2 = lfilter([+1,-1], 1, den2)
ind2 = np.nonzero(dden2==-2)
ind2=np.array(ind2) -1
time=time[dtnf_ind][0]
peaks=dtnf[ind2][0]
time=time[ind2]

clean_peaks=[0]
time2=[0]

for k in range (1,len(peaks)):
    if peaks[k]>peaks[k-1]:
        clean_peaks=clean_peaks+[peaks[k]]
        time2=time2+[time[k]]
plt.plot(time2,clean_peaks,'o')


  





