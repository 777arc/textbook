import matplotlib.pyplot as plt
import numpy as np
import time
import imageio

# Used https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php

filename = "logo_coords.csv"
scale = 60000
offset = 250
#filename = "M_coords.csv"
#scale = 20000
#offset = 600

# Load in data
xs = []
ys = []
for line in open(filename):
    x,y = line.replace('\n','').split(',')
    xs.append(int(x) - offset)
    ys.append(-1*(int(y) - offset))
#plt.plot(xs,ys,'.-')
#plt.show()

# Take FFT and use coefficients to reconstruct data
'''
c = np.asarray(xs) + 1j*np.asarray(ys)
N = len(c)
C = np.fft.fftshift(np.fft.fft(c))
reconstruct = np.zeros(N, dtype=complex)
t = np.arange(N)
f = np.arange(-N//2, N//2)
for i, Ci in enumerate(C):
    reconstruct += Ci * np.exp(2j*np.pi/N*f[i]*t)
plt.plot(np.real(reconstruct), np.imag(reconstruct), '.-')
plt.show()
'''

# Animate rotating circles over time
c = np.asarray(xs) + 1j*np.asarray(ys)
N = len(c) # FFT size
C = np.fft.fftshift(np.fft.fft(c, N))
f = np.arange(-N//2, N//2)
points_x = []
points_y = []
plt.figure(figsize=(15,10))
colors = ['g', 'b', 'r']
filenames = []
n = 0
for t in list(range(len(c))) + [0]: # time.  at the end go back to 0
    x = 0
    y = 0
    color_i = 0
    cis = []
    for i in range(N): # freq
        cis.append(C[i] * np.exp(2j*np.pi/N*f[i]*t)) # remember t is a single value now
    order = np.flip(np.argsort(np.abs(cis))) # sort in order of vector length, biggest vectors will be plotted first
    for i in order:
        ci = cis[i]
        mag = np.abs(ci)
        dx = np.real(ci)
        dy = np.imag(ci)
        color = colors[color_i]
        circle1 = plt.Circle((x,y), mag, color=color, alpha=0.05)
        plt.gcf().gca().add_artist(circle1)
        plt.arrow(x, y, dx, dy, color=color)#, head_width=500)
        color_i += 1
        color_i = color_i % len(colors)
        x += dx
        y += dy
    points_x.append(x)
    points_y.append(y)
    plt.plot(points_x,points_y,'k.-')
    plt.axis([-1.5*scale, scale*1.5, -1*scale, scale])
    if False:
        plt.draw()
        plt.pause(0.02) # 0.5
        plt.cla()
    else:
        print(n)
        filename = '/tmp/fourier_series_' + str(n) + '.png'
        n += 1
        plt.savefig(filename, bbox_inches='tight')
        plt.cla()
        filenames.append(filename)

# Plot final list of points and then pause 5 seconds
plt.plot(points_x,points_y,'k.-')
plt.axis([-1.5*scale, scale*1.5, -1*scale, scale])
if False:
    plt.draw()
    plt.pause(0.1)
    time.sleep(5)
else:
    filename = '/tmp/fourier_series_' + str(n) + '.png'
    n += 1
    plt.savefig(filename, bbox_inches='tight')
    filenames.append(filename)

    # Create animated gif
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('/tmp/fourier_series.gif', images, fps=10)

    print("Created animated gif")












