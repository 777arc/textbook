import matplotlib.pyplot as plt
import numpy as np

snr_per_bit_dB = np.linspace(-20, 40, 10000)  # dB
c = np.log2(1 + 10 ** (snr_per_bit_dB / 10))  # remember to do the foruma in linear
'''
# Work backwards
c = np.linspace(0.1, 10, 1000)
snr_per_bit = (2**c - 1)
snr_per_bit_dB = 10.0*np.log10(snr_per_bit)
'''
fig, ax = plt.subplots(figsize=(7, 4))

# actual signal
ax.plot(snr_per_bit_dB, c, 'r--')

ax.axis([-20, 30, 0, 10])
# ax.grid(True)

ax.set_xlabel('SNR [dB]')
ax.set_ylabel('Shannon Limit [bits/s/Hz]')

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
# ax.set_xticklabels([])
# ax.set_yticklabels([])

plt.show()

fig.savefig('../_images/generated/shannon_limit.svg', bbox_inches='tight')
