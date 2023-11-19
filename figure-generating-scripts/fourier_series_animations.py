import imageio
import matplotlib.pyplot as plt
import numpy as np

# Make arbitrary step function
Fs = 1
ydata = np.repeat(np.random.randint(-1, 2, 10), 100)
ydata = ydata.astype(float)
xdata = np.arange(len(ydata))
multiplier = 3
num_n = 20

# Make sawtooth
# xdata = np.linspace(-3*np.pi, 3*np.pi, 1024)
# ydata = (xdata % (2*np.pi) - np.pi)/np.pi
# multiplier = 3 # how many cycles our dominant freq is
# num_n = 11

filenames = []
for n in range(1, num_n):
    # Use FFT instead of actually computing fourier series
    Y = np.fft.rfft(ydata)  # don't do FFT shift so DC is [0] and first freq is [1] and so on
    Y[(n + 1) * multiplier:] = 0  # remember that the lowest freq is a sinusoid that spans the whole range
    ydata_fourier = np.fft.irfft(Y)

    # Plot the result
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(xdata, ydata, 'b')
    ax.plot(xdata, ydata_fourier, 'r')

    # Add text showing n
    if num_n == 11:  # only for triangle
        ax.text(2.5 * np.pi, 1, 'n = ' + str(n), fontsize=16)

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
    ax.set_yticklabels([])

    ax.axis([min(xdata), max(xdata), -1.5, 1.5])
    # plt.show()
    # exit()

    filename = '/tmp/fourier_series_' + str(n) + '.png'
    fig.savefig(filename, bbox_inches='tight')
    filenames.append(filename)

# Create animated gif
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/tmp/fourier_series.gif', images, fps=2)
