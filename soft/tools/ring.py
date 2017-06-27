import numpy as np


class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype=np.int16)
        self.index = 0
        self.length = length

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self, n):
        if n > self.length: n = self.length
        "Returns the n last data added to the buffer"
        idx = (self.index + np.arange(n) - n) %self.data.size
        return self.data[idx]
