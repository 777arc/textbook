import matplotlib.pyplot as plt
import numpy as np

Fs = 300  # sample rate
Ts = 1 / Fs  # sample period
N = 2048  # number of samples to simulate

t = Ts * np.arange(N)
x = np.exp(1j * 2 * np.pi * 50 * t)  # simulates sinusoid at +50 Hz

n = (np.random.randn(N) + 1j * np.random.randn(N)) / np.sqrt(2)  # AWGN with unity power
noise_power = 2
r = x + n * np.sqrt(noise_power)

PSD = (np.abs(np.fft.fft(r)) / N) ** 2
PSD_log = 10.0 * np.log10(PSD)
PSD_shifted = np.fft.fftshift(PSD_log)

f = np.linspace(Fs / -2.0, Fs / 2.0, N)  # lazy method

plt.plot(f, PSD_shifted)
plt.grid(True)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")

# plt.show()

plt.savefig('../_static/fft_example1.svg', bbox_inches='tight')
