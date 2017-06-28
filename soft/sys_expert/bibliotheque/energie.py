from . import drop as dr
import numpy as np
import librosa
from scipy.signal import *

BASS_THRESHOLD = 30
HIGH_THRESHOLD = 30

def high_freq_energie(signal,fe):
    b,a = iirfilter(N=2,Wn=[5000.0/fe*2],btype="highpass",ftype="butter")
    signal = lfilter(b,a,signal)
    energy_raw = librosa.feature.rmse(y=signal)
    return energy_raw

def low_freq_energie(signal,fe):
    b,a = iirfilter(N=2,Wn=[150.0/fe*2],btype="lowpass",ftype="butter")
    signal = lfilter(b,a,signal)
    energy_raw = librosa.feature.rmse(y=signal)
    return energy_raw

