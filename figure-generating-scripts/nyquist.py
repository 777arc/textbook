import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin

sample_rate = 1e6

# Generate noise
x = np.random.randn(10000)
h = firwin(21, 0.4)
x = np.convolve(x,h,'same')

# Trying to reduce the bumpyness look of it, so as to not throw people off
y = np.random.randn(10000)
h = firwin(31, 0.35)
y = np.convolve(y,h,'same')

x = x + y

fft = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x)))**2)
fft = fft[len(fft)//2:]

f = np.linspace(0, sample_rate/2, len(fft))

plt.plot(f, fft)
plt.plot([288e3, 288e3], [-100, 100], 'r:')
plt.xlabel("Frequency")
plt.axis([0, np.max(f), -12, 60])
ax = plt.gca()
ax.xaxis.set_ticklabels([])
#plt.ylabel("Magnitude")
ax.yaxis.set_ticklabels([])
plt.show()
#plt.savefig('../_images/max_freq.svg', bbox_inches='tight')
