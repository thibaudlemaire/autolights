from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import *


filename='drop_3.wav'

fe,signal=wavfile.read(filename)
f=fe
signal=signal[:,1]



plt.specgram(signal, NFFT=2048, Fs=fe, noverlap=3*2048/4)
plt.show()




def calcul_energie(signal,a) :
    ech=len(signal)
    energie = np.zeros(ech)
    energie[0]= signal[0]
    n=0
    for n in range (1, ech):
        energie[n]=a*energie[n-1]+ (1.0-a)*(signal[n]**2)
    return energie 

energie= calcul_energie(signal, 0.99995)


fe=fe*1.0/echantillonnage

energie=energie/max(energie)
energie =lfilter(np.hanning(100),1,energie)
   
##low pass filter
    
b3,a3 = iirfilter(N=3,Wn=[100/f*2],btype="highpass",ftype="butter")
w,h=freqz(b3,a3,4096)
plt.figure()
plt.plot(w,abs(h))

#freq de coupure fc/fe=0.1 si Wn= [0.1¨*2]

plt.figure()
plt.plot(np.arange(len(signal))*1.0/fe, calcul_energie(lfilter(b3,a3, signal), 0.99995))
plt.show()