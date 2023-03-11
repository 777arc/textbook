import numpy as np
import matplotlib.pyplot as plt

num_symbols = 10
sps = 8

#bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0's
bits = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1]

x = np.array([])
for bit in bits:
    pulse = np.zeros(sps)
    pulse[0] = bit*2-1 # set the first value to either a 1 or -1
    x = np.concatenate((x, pulse)) # add the 8 samples to the signal

# Create our raised-cosine filter
num_taps = 101
beta = 0.35
Ts = sps # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
t = np.arange(num_taps) - (num_taps-1)//2
print(t)
print(len(t))
h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)

# Filter our signal, in order to apply the pulse shaping
x_shaped = np.convolve(x, h)
fig, ax = plt.subplots(1,1,figsize=(10,4))
plt.plot(x_shaped, '.-')
for i in range(num_symbols):
    xpos = i*sps+num_taps//2+1
    ypos = x_shaped[xpos]
    plt.arrow(x=xpos, y=0, dx=0, dy=ypos, color="red", ls=(0, (5, 5)))
plt.grid(True)
ax.set_yticks([-1, 0, +1], minor=False)
plt.show()
#fig.savefig('../_images/pulse_shaping_python3.svg', bbox_inches='tight')
