import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.io import wavfile


j=complex(0,1)


def idealFilter(M,b):
    n=np.arange(-M+1,M)
    n[M-1]=10**(-12)
    h=(-2*np.pi)*((np.sin(np.pi*n*b*2)/2)-np.pi*b*n*np.cos(np.pi*n*b*2))/((np.pi**2)*n**2)
    h[M-1]=0
    return h




w,h=scipy.signal.freqz(idealFilter(1000,0.2)*scipy.signal.hamming(1999),1,4096)

plt.plot(w,abs(h))

plt.show()


              