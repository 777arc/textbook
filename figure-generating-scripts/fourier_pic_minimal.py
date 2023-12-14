import matplotlib.pyplot as plt
import numpy as np

# Coords for M shape
xs = [-2, 133, 238, 550, 472, 472, 470, 560, 230, 228, 228, 62, -63, -233, -239, -563, -479, -479, -479, -559, -244, -140]
ys = [34, 341, 575, 575, 366, 48, -326, -515, -517, -308, -55, -419, -424, -57, -515, -517, -324, 67, 362, 581, 577, 349]

# Animate rotating circles over time
c = np.asarray(xs) + 1j*np.asarray(ys) # create complex samples
N = len(c) # FFT size
C = np.fft.fftshift(np.fft.fft(c)) # take FFT
f = np.arange(-N//2, N//2) # frequencies of each bin
points_x = []
points_y = []
colors = ['g', 'b', 'r']
for t in list(range(N)) + [0]: # at the end go back to t=0
    x = 0
    y = 0
    color_i = 0
    vectors = [C[i] * np.exp(2j*np.pi/N*f[i]*t) for i in range(N)]
    for i in np.flip(np.argsort(np.abs(vectors))): # sort in order of vector length, biggest vectors will be plotted first
        dx = np.real(vectors[i])
        dy = np.imag(vectors[i])
        plt.gcf().gca().add_artist(plt.Circle((x,y), np.abs(vectors[i]), color=colors[color_i], alpha=0.05)) # circle, radius is magnitude
        plt.arrow(x, y, dx, dy, color=colors[color_i]) # vector
        color_i += 1
        color_i = color_i % len(colors) # loop through colors
        x += dx # add vector to total
        y += dy
    points_x.append(x) # keep points on plot
    points_y.append(y)
    plt.plot(points_x,points_y,'k.-')
    plt.axis([-30000, 30000, -20000, 20000])
    plt.draw()
    plt.pause(0.5)
    plt.cla()
