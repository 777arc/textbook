import matplotlib.pyplot as plt
import numpy as np

Fs = 1000
Ts = 1 / Fs

f = 2
T = 1 / f
phi = 0.1 * T
t = np.arange(0, 600) * Ts
x = np.sin(f * 2 * np.pi * (t - phi))

fig, ax = plt.subplots(figsize=(10, 3))

# Plot stuff
ax.plot(t, x)
arrowstyle = '<->'
ax.text(T / 4 - 0.02, 0.4, 'Amplitude', color='r')
ax.annotate(text='', xy=(T / 4 + phi, 0), xytext=(T / 4 + phi, 1), arrowprops=dict(color='red', arrowstyle=arrowstyle))  # amplitude

ax.text(T / 2 + 0.02, -0.2, 'Period   (1/Frequency)', color='r')
ax.annotate(text='', xy=(phi, -0.05), xytext=(T + phi, -0.05), arrowprops=dict(color='red', arrowstyle=arrowstyle))

ax.text(0.01, 0.15, 'Phase', color='r')
ax.annotate(text='', xy=(0, 0.05), xytext=(phi, 0.05), arrowprops=dict(color='red', arrowstyle=arrowstyle))

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

fig.savefig('../_static/amplitude_phase_period.svg', bbox_inches='tight')
