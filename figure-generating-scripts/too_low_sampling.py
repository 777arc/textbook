import matplotlib.pyplot as plt
import numpy as np

f = 0.3  # freq of sinusoid (arbitrary)
Fs = [1 * f, 1.2 * f, 1.5 * f, 2 * f]
f_wrong = [0, -0.06, -0.15]
t_offset = 0.2

for i in range(4):
    fig, ax = plt.subplots(figsize=(10, 3))

    # actual signal
    t = np.arange(0, 17, 0.001)
    x = np.sin(2 * np.pi * f * t + t_offset)
    ax.plot(t, x, 'g')

    # sampled signal
    Ts = 1 / Fs[i]
    nT = np.arange(20) * Ts  # more than we need, but we'll clip them
    samples = np.sin(2 * np.pi * f * nT + t_offset)  # simulates sampling
    ax.plot(nT, samples, 'b.', markersize=15)

    # "wrong" signal for demonstration sake
    if i < 3:
        x_wrong = np.sin(2 * np.pi * f_wrong[i] * t + t_offset)
        ax.plot(t, x_wrong, 'r--')

    ax.axis([0, max(t) + 0.1, -1.2, 1.2], )

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

    # plt.show()

    fig.savefig('../_images/generated/sampling_Fs_' + str(round(Fs[i], 2)) + '.svg', bbox_inches='tight')
