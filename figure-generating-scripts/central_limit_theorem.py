import matplotlib.pyplot as plt
import numpy as np

N = 100000

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 3))
fig.subplots_adjust(hspace=0.4)

x1 = np.random.weibull(2, N)
ax1.hist(x1, 100, density=True, facecolor='g')
ax1.axes.xaxis.set_ticks([])
ax1.axes.yaxis.set_ticks([])

x2 = np.random.uniform(-4, 4, N)
ax2.hist(x2, 100, density=True, facecolor='g')
ax2.axes.xaxis.set_ticks([])
ax2.axes.yaxis.set_ticks([])

x3 = np.random.exponential(1, N)
ax3.hist(x3, 300, density=True, facecolor='g')
ax3.axes.xaxis.set_ticks([])
ax3.axes.yaxis.set_ticks([])
ax3.set_xlim(left=-0.3, right=5)

x4 = np.random.weibull(100, N)
ax4.hist(x4, 200, density=True, facecolor='g')
ax4.axes.xaxis.set_ticks([])
ax4.axes.yaxis.set_ticks([])
ax4.set_xlim(left=0.92, right=1.02)

plt.show()

fig.savefig('../_images/central_limit_theorem.svg', bbox_inches='tight')


# Now the combination in a sep plot saved to tmp

fig, (ax) = plt.subplots(1, 1, figsize=(4, 3))
#x = x1 + x2 + x3 + x4 # not enough =P
x = np.random.randn(N)
ax.hist(x, 100, density=True, facecolor='g')
ax.axes.xaxis.set_ticks([])
ax.axes.yaxis.set_ticks([])

plt.show()

fig.savefig('/tmp/central_limit_theorem_main.svg', bbox_inches='tight')

# I then edited it in inkscape to make the nice graphic with arrows and such
