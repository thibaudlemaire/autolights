import drop as dr
import numpy as np
from scipy.signal import *



def high_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[5000.0/fe*2],btype="highpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    signal=signal[(int)(fe*0.2):]
    time=time[(int)(fe*0.2):]
    ind = np.nonzero(signal>(10**(-5))) 
    ind = np.array(ind) #on repasse en np.array
    signal=signal[ind][0]
    return 20*np.log10(signal)

def low_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[150.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    signal=signal[(int)(fe*0.2):]
    time=time[(int)(fe*0.2):]
    ind = np.nonzero(signal>(10**(-5)))
    ind = np.array(ind) #on repasse en np.array
    signal=signal[ind][0]
    return 20*np.log10(signal)
   

def detect_bass(signal,fe):
    signal=low_freq_energie(signal,fe)
    ma=max(signal)
    if ma>180:    
        return True
    else: 
        return False

def detect_high_sweep(signal,fe):
    signal=high_freq_energie(signal,fe)
    ma=max(signal)
    if ma>172:
        return True
    else:
        return False