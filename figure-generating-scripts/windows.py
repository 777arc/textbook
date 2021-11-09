import matplotlib.pyplot as plt
import numpy as np

fig, [ax, ax2] = plt.subplots(1,2,figsize=(10, 4))
n = 1000
rect = np.ones(n)
rect[0] = 0
rect[-1] = 0
ax.plot(rect,'--')
ax.plot(np.hamming(n))
ax.plot(np.hanning(n))
ax.plot(np.bartlett(n))
ax.plot(np.blackman(n))
ax.plot(np.kaiser(n, 4))
ax.set_title("Time Domain")
#ax.axis([-100,n+100,0,1.2])
ax.legend(['Rectangular', 'Hamming', 'Hanning', 'Bartlett', 'Blackman', 'Kaiser'], fontsize='large', bbox_to_anchor=(0.5, 0.35), framealpha=1)

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
#ax.set_xlabel("Sample")
ax.set_ylabel("Amplitude / Value")
ax.text(n-10,-0.07,"N")
ax.text(-10,-0.07,"0")
ax.set_xticklabels([])
#ax.set_yticklabels([])



N = 10000
f = np.linspace(0, 100/N, 100)
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(rect, N)[0:100]))-30,'--')
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(np.hamming(n), N)[0:100]))-27-0.3)
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(np.hanning(n), N)[0:100]))-27)
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(np.bartlett(n), N)[0:100]))-27)
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(np.blackman(n), N)[0:100]))-27+0.75)
ax2.plot(f, 10*np.log10(np.abs(np.fft.fft(np.kaiser(n, 4), N)[0:100]))-27-0.8)
ax2.axis([0,np.max(f),-50,3])
ax2.set_xlabel("Normalized Frequency")
ax2.set_ylabel("dB")
ax2.set_title("Frequency Domain")
plt.show()

fig.savefig('../_images/generated/windows.svg', bbox_inches='tight')
