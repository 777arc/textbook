import matplotlib.pyplot as plt
import numpy as np

f = 0.1  # freq of sinusoid (arbitrary)
Fs = 0.5
t_offset = 0.2

fig, ax = plt.subplots(figsize=(6, 3))

# actual signal
t = np.arange(0, 18.5, 0.001)
x = np.sin(2 * np.pi * f * t + t_offset) + 0.9 * np.cos(2.5 * np.pi * f * 1.5123 * t + 10) + np.cos(2 * np.pi * f * 0.2123 * t + 20)
ax.plot(t, x, 'g')

# sampled signal
Ts = 1 / Fs
nT = np.arange(10) * Ts  # more than we need, but we'll clip them
samples = x = np.sin(2 * np.pi * f * nT + t_offset) + 0.9 * np.cos(2.5 * np.pi * f * 1.5123 * nT + 10) + np.cos(2 * np.pi * f * 0.2123 * nT + 20)  # simulates sampling
ax.plot(nT, samples, 'b.', markersize=15)

# Vertical lines
for i in range(10):
    ax.plot([i * Ts, i * Ts], [0, samples[i]], 'b:')

# Labels
arrowstyle = '<->'
ax.text(Ts * 4.35, 0.3, 'T', color='r', fontsize=18)
ax.annotate(text='', xy=(Ts * 4 * 0.98, 0.15), xytext=(Ts * 5 * 1.02, 0.15), arrowprops=dict(color='red', arrowstyle=arrowstyle))  # amplitude
ax.text(Ts * 1.7, 1.2, 'S(t)', color='g', fontsize=18)
ax.text(max(t) * 1.07, -0.2, 't', color='black', fontsize=18)

# ax.axis([0, max(t) + 0.1, -1.2, 1.2], )
# Set tick spacing
plt.xticks(np.arange(0, 19, Ts))

# set the x-spine (see below for more info on `set_position`)
ax.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()

# set the y-spine
ax.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()

# Turn off tick numbering/labels
ax.set_xticklabels([])
ax.set_yticklabels([])

plt.show()

fig.savefig('../_static/sampling.svg', bbox_inches='tight')
