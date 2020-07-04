import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))

t = np.arange(1024)
x = np.exp(0.05*2*np.pi*1j*t) + np.exp(-0.05*2*np.pi*1j*t) + np.exp(0.15*2*np.pi*1j*t) + np.exp(-0.15*2*np.pi*1j*t)
n = np.random.randn(len(x)) + 1j*np.random.randn(len(x))
r = x + 0.5*n
r = np.fft.ifft(np.fft.fft(r, 128))

X = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(r, 2048)))**2)
n = np.random.randn(len(X)) + 1j*np.random.randn(len(X))
X = X + 2*n # try to make it look a little more realistic

ax.plot(np.linspace(-1, 1, len(X)), X)
ax.axis([-1, 1, 10, 50])
ax.set_xlabel("Frequency [MHz]")
ax.set_ylabel("Power Spectral Density")
plt.show()
fig.savefig('../_static/fsk.svg', bbox_inches='tight')