import matplotlib.pyplot as plt
import numpy as np


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
fig.subplots_adjust(hspace=0.4)

t = np.arange(0,1,0.001)
t_sub = np.arange(0,1,0.01)
symbols = (np.random.randint(0,2,10)+1)
train = np.repeat(symbols, 100)
train_sub = np.repeat(symbols, 10)
ax1.plot(t,train)
ax1.plot(t_sub,train_sub, '.r')
ax1.set_title("Our Data")
ax1.set_ylabel("Amplitude")
ax1.set_ylim(bottom=0.5, top=2.5)
ax1.set_xlim(left=0, right=1)


f = 30
x = np.sin(2*np.pi*f*t)*train
ax2.plot(t,x)
ax2.set_title("Wireless Signal")
ax2.set_xlabel("Time")
ax2.set_ylabel("Amplitude")
ax2.set_xlim(left=0, right=1)

plt.show()

fig.savefig('../_static/ask3.svg', bbox_inches='tight')
