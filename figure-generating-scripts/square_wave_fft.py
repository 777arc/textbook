import matplotlib.pyplot as plt
import numpy as np

y = np.repeat(np.arange(10) % 2, 20) * 2 - 1
y = y.astype(float)
Y = np.abs(np.fft.rfft(y, 10000))
print(Y)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
plt.subplots_adjust(wspace=0.4)

# Plot stuff
ax1.plot(y)
ax1.text(len(y) + 10, -0.05, 'Time')
ax1.set_ylabel("Amplitude")

ax2.plot(Y)
ax2.set_xlabel("Frequency")
ax2.set_ylabel("Magnitude")

# set the x-spine (see below for more info on `set_position`)
ax1.spines['left'].set_position('zero')
ax2.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax1.spines['right'].set_color('none')
ax1.yaxis.tick_left()
ax2.spines['right'].set_color('none')
ax2.yaxis.tick_left()

# set the y-spine
ax1.spines['bottom'].set_position('zero')
ax2.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax1.spines['top'].set_color('none')
ax1.xaxis.tick_bottom()
ax2.spines['top'].set_color('none')
ax2.xaxis.tick_bottom()

# Turn off tick numbering/labels
ax1.set_xticklabels([])
ax1.set_yticklabels([])
ax2.set_xticklabels([])
ax2.set_yticklabels([])

plt.show()

fig.savefig('../_static/square-wave.svg', bbox_inches='tight')
