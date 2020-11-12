import matplotlib.pyplot as plt
import numpy as np

fig, (ax1) = plt.subplots(1, 1, figsize=(10, 3))
plt.subplots_adjust(wspace=0.4)

sps = 100
t = np.linspace(-4 * sps, 4 * sps, 1000)
leg = []
for beta in [0, 0.25, 0.5, 1]:
    h = np.sinc(t / sps) * np.cos(np.pi * beta * t / sps) / (1 - (2 * beta * t / sps) ** 2)
    ax1.plot(t, h)
    leg.append('β = ' + str(beta))

plt.legend(leg, fontsize=14)
ax1.text(max(t) * 1.12, -0.05, 'Time', fontsize=14)
ax1.text(-4 * sps - 15, -0.1, '-4T', fontsize=14)
ax1.text(-3 * sps - 15, -0.1, '-3T', fontsize=14)
ax1.text(-2 * sps - 15, -0.1, '-2T', fontsize=14)
ax1.text(-1 * sps - 15, -0.1, '-T', fontsize=14)
ax1.text(0 * sps - 15, -0.1, '0', fontsize=14)
ax1.text(1 * sps - 15, -0.1, '1T', fontsize=14)
ax1.text(2 * sps - 15, -0.1, '2T', fontsize=14)
ax1.text(3 * sps - 15, -0.1, '3T', fontsize=14)
ax1.text(4 * sps - 15, -0.1, '4T', fontsize=14)
ax1.text(-15, 1.1, 'h(t)', fontsize=14)

# set the x-spine (see below for more info on `set_position`)
ax1.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax1.spines['right'].set_color('none')
ax1.yaxis.tick_left()

# set the y-spine
ax1.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax1.spines['top'].set_color('none')
ax1.xaxis.tick_bottom()

# Turn off tick numbering/labels
ax1.set_xticklabels([])
ax1.set_yticklabels([])

plt.show()

fig.savefig('../_static/raised_cosine.svg', bbox_inches='tight')

fig, (ax1) = plt.subplots(1, 1, figsize=(10, 3))
plt.subplots_adjust(wspace=0.4)

sps = 100
leg = []
for beta in [0.01, 0.25, 0.5, 1]:
    f = np.linspace(-1.5 / sps, 1.5 / sps, 1000)
    H = []
    for fi in f:
        if np.abs(fi) <= (1 - beta) / 2 / sps:
            H.append(1)
        elif (np.abs(fi) <= (1 + beta) / 2 / sps) and (np.abs(fi) > (1 - beta) / 2 / sps):
            H.append(0.5 * (1 + np.cos(np.pi * sps / beta * (np.abs(fi) - (1 - beta) / (2 * sps)))))
        else:
            H.append(0)
    ax1.plot(f, H)
    if beta == 0.01:
        beta = 0
    leg.append('β = ' + str(beta))

plt.legend(leg, fontsize=14)
ax1.text(max(f) * 1.12, -0.05, 'Freq', fontsize=14)
ax1.text(-1.5 / sps - 0.0015, -0.1, '-3/2T', fontsize=14)
ax1.text(-1 / sps - 0.0015, -0.1, '-1/T', fontsize=14)
ax1.text(-0.5 / sps - 0.0015, -0.1, '-1/2T', fontsize=14)
ax1.text(0, -0.1, '0', fontsize=14)
ax1.text(1.5 / sps - 0.0015, -0.1, '3/2T', fontsize=14)
ax1.text(1 / sps - 0.0005, -0.1, '1/T', fontsize=14)
ax1.text(0.5 / sps - 0.0015, -0.1, '1/2T', fontsize=14)
ax1.text(0, 1.1, 'H(f)', fontsize=14)

# set the x-spine (see below for more info on `set_position`)
ax1.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax1.spines['right'].set_color('none')
ax1.yaxis.tick_left()

# set the y-spine
ax1.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax1.spines['top'].set_color('none')
ax1.xaxis.tick_bottom()

# Turn off tick numbering/labels
ax1.set_xticklabels([])
ax1.set_yticklabels([])

plt.show()

fig.savefig('../_static/raised_cosine_freq.svg', bbox_inches='tight')

fig, (ax1) = plt.subplots(1, 1, figsize=(10, 3))
plt.subplots_adjust(wspace=0.4)

sps = 100
t = np.linspace(-10 * sps, 10 * sps, 1000)
leg = []
for beta in [0, 0.25, 0.5, 1]:
    h = np.sinc(t / sps) * np.cos(np.pi * beta * t / sps) / (1 - (2 * beta * t / sps) ** 2)
    ax1.plot(t, h)
    leg.append('β = ' + str(beta))

plt.legend(leg, fontsize=14)
# for T in range(-10, 11):
#    ax1.text(T*sps - 15, -0.1, str(T) + 'T', fontsize=10)

ax1.text(-15, 1.1, 'h(t)', fontsize=14)
ax1.text(max(t) * 1.12, -0.05, 'Time', fontsize=14)

# set the x-spine (see below for more info on `set_position`)
ax1.spines['left'].set_position('zero')

# turn off the right spine/ticks
ax1.spines['right'].set_color('none')
ax1.yaxis.tick_left()

# set the y-spine
ax1.spines['bottom'].set_position('zero')

# turn off the top spine/ticks
ax1.spines['top'].set_color('none')
ax1.xaxis.tick_bottom()

# Turn off tick numbering/labels
ax1.set_xticklabels([])
ax1.set_yticklabels([])

plt.show()

fig.savefig('../_static/rrc_rolloff.svg', bbox_inches='tight')
