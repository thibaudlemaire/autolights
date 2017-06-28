import drop as dr
import numpy as np
from scipy.signal import *



def high_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[5000.0/fe*2],btype="highpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    signal=signal[88:]
    time=time[88:]
    return 20*np.log10(signal),time

def low_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[150.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    signal=signal[88:]
    time=time[88:]
    return 20*np.log10(signal),time

def detect_bass(signal,fe):
    signal,time=low_freq_energie(signal,fe)
    ma=max(signal)
    if ma>180:    
        return True
    else: 
        return False

def detect_high_sweep(signal,fe):
    signal,time=high_freq_energie(signal,fe)
    ma=max(signal)
    if ma>172:
        return True
    else:
        return False