import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4))
n = 1000
rect = np.ones(n)
rect[0] = 0
rect[-1] = 0
ax.plot(rect)
ax.plot(np.hamming(n))
ax.plot(np.hanning(n))
ax.plot(np.bartlett(n))
ax.plot(np.blackman(n))
ax.plot(np.kaiser(n, 4))
ax.legend(['Rectangular','Hamming','Hanning','Bartlett','Blackman','Kaiser'],fontsize='large',loc='lower center')


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
#ax.set_yticklabels([])

plt.show()

fig.savefig('../_static/windows.svg', bbox_inches='tight')

