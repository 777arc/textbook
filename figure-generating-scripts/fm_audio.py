import numpy as np
from scipy.signal import resample_poly, firwin, bilinear, lfilter
import matplotlib.pyplot as plt
 
# Thanks to Joel Cordeiro for the base code

#x = np.fromfile('/home/marc/Downloads/fm_clip_for_rds.iq', dtype=np.complex64) # med SNR
#x = np.fromfile('/home/marc/Downloads/fm_rds_250k.iq', dtype=np.complex64) # high SNR
x = np.fromfile('fm_rds_250k_1Msamples.iq', dtype=np.complex64) # high SNR, shorter
sample_rate = 250e3    # sample frequency

# Add the following code right after the "Acquiring a Signal" section

from scipy.io import wavfile

# Demodulation
x = np.diff(np.unwrap(np.angle(x)))

# De-emphasis filter, low pass RC analog filter H(s) = 1/(RC*s + 1), implemented via bilinear transform
bz, az = bilinear(1, [75e-6, 1], fs=sample_rate)
x = lfilter(bz, az, x)

# decimate by 6 to get mono audio
x = x[::6]
sample_rate_audio = sample_rate/6

# normalize volume so its between -1 and +1
x /= np.max(np.abs(x))

# some machines want int16s
x *= 32767
x = x.astype(np.int16)

# Save to wav file, you can open this in Audacity for example
wavfile.write('fm.wav', int(sample_rate_audio), x)


'''
# Analyze filter
n = np.random.randn(1000000)
n = lfilter(bz, az, n)
fft = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(n)))**2)
fft = fft[len(fft)//2:]
f = np.linspace(0, sample_rate/2, len(fft))/1e3
plt.plot(f, fft)
plt.xlabel('Frequency [kHz]')
plt.ylabel('PSD [dB]')
plt.show()
'''
