import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


sps = 32

# Create our raised-cosine filter
num_taps = 1001
beta = 0.35
Ts = sps # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
t = np.arange(num_taps//-2, num_taps//2) # remember it's not inclusive of final number
h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)

N = 2000
fig, (ax) = plt.subplots(1, 1, figsize=(10, 4))
for delay in np.arange(-2,3):
    x = np.zeros(N)
    x[N//2 + delay*sps] = 1
    x_shaped = np.convolve(x, h, 'same')
    t = (np.arange(N) - N/2)/sps
    ax.plot(t, x_shaped, '-')

ax.axis([-7, 7, -0.3, 1.2])
ax.set_xlabel("Time")
ax.set_ylabel("Pulses (before being combined)")

#ax.xaxis.set_major_locator(MaxNLocator(integer=True))
major_ticks = np.arange(-6, 7)
ax.set_xticks(major_ticks)

plt.grid(True)
#plt.show()
fig.savefig('../_images/pulse_train.svg', bbox_inches='tight')
