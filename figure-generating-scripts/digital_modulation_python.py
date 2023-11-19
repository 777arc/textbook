import matplotlib.pyplot as plt
import numpy as np

### No noise
num_symbols = 1000

x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols

fig, (ax1) = plt.subplots(1, 1, figsize=(4, 4))
fig.subplots_adjust(hspace=0.4)
ax1.plot(np.real(x_symbols), np.imag(x_symbols), '.')
ax1.set_ylabel("Q")
ax1.set_xlabel("I")
ax1.set_ylim(bottom=-1, top=1)
ax1.set_xlim(left=-1, right=1)
ax1.grid()
plt.show()
fig.savefig('../_static/qpsk_python.svg', bbox_inches='tight')



### Add AWGN
n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
noise_power = 0.01
r = x_symbols + n * np.sqrt(noise_power)

fig, (ax1) = plt.subplots(1, 1, figsize=(4, 4))
fig.subplots_adjust(hspace=0.4)
ax1.plot(np.real(r), np.imag(r), '.')
ax1.set_ylabel("Q")
ax1.set_xlabel("I")
ax1.set_ylim(bottom=-1, top=1)
ax1.set_xlim(left=-1, right=1)
ax1.grid()
plt.show()
fig.savefig('../_static/qpsk_python2.svg', bbox_inches='tight')


### Phase noise
phase_noise = np.random.randn(len(x_symbols)) * 0.15 # adjust multiplier for "strength" of phase noise
r = x_symbols * np.exp(1j*phase_noise)

fig, (ax1) = plt.subplots(1, 1, figsize=(4, 4))
fig.subplots_adjust(hspace=0.4)
ax1.plot(np.real(r), np.imag(r), '.')
ax1.set_ylabel("Q")
ax1.set_xlabel("I")
ax1.set_ylim(bottom=-1, top=1)
ax1.set_xlim(left=-1, right=1)
ax1.grid()
plt.show()
fig.savefig('../_static/phase_jitter.svg', bbox_inches='tight')



### Phase noise plus AWGN
phase_noise = np.random.randn(len(x_symbols)) * 0.2 # adjust multiplier for "strength" of phase noise
r = x_symbols * np.exp(1j*phase_noise) + n * np.sqrt(noise_power)

fig, (ax1) = plt.subplots(1, 1, figsize=(4, 4))
fig.subplots_adjust(hspace=0.4)
ax1.plot(np.real(r), np.imag(r), '.')
ax1.set_ylabel("Q")
ax1.set_xlabel("I")
ax1.set_ylim(bottom=-1.2, top=1.2)
ax1.set_xlim(left=-1.2, right=1.2)
ax1.grid()
plt.show()
fig.savefig('../_static/phase_jitter_awgn.svg', bbox_inches='tight')



