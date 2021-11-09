import matplotlib.pyplot as plt
import numpy as np


fig, (ax1) = plt.subplots(1, 1, figsize=(10, 3))
fig.subplots_adjust(hspace=0.4)

t = np.arange(0,2,0.001)
symbols = np.random.randint(0,4,20)
train = np.repeat(symbols, 100)
f = 25
x = np.sin(2*np.pi*f*t)*train
#ax1.plot([2,2.1],[1,1],':r')
#ax1.plot([2,2.1],[2,2],':r')
#ax1.plot([2,2.1],[3,3],':r')
#ax1.plot([2,2.1],[0,0],':r')
ax1.plot(t,x)
ax1.set_ylabel("Amplitude")
ax1.set_xlabel("Time")
#ax1.set_ylim(bottom=0.5, top=2.5)
#ax1.set_xlim(left=0, right=2)
ax1.grid()

plt.show()

fig.savefig('../_images/generated/ask2.svg', bbox_inches='tight')
