import bibliotheque.drop as dr
import numpy as np




def high_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[5000.0/fe*2],btype="highpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    return 20*np.log10(signal),time

def low_freq_energie(signal,fe):
    time =np.arange(len(signal))*1.0/fe
    b,a = iirfilter(N=2,Wn=[100.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    signal, time, fe =dr.detect_env(signal, time, fe)
    return 20*np.log10(signal),time



  

