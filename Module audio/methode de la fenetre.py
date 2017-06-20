import numpy as np
import scipy.signal


j=complex(0,1)


def idealFilter(n,fe):
    h=[0]*n
    h[0]=0
    for i in range(1,n):
        h[i]=(fe/i*np.cos(fe*np.pi*i)-1/(np.pi*i**2)*np.sin(fe*np.pi*i))
    return h



    realFilter=scipy.signal.lfilter(idealFilter(100,1),1,np.hanning(100))
