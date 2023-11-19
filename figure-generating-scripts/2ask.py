import matplotlib.pyplot as plt
import numpy as np


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
fig.subplots_adjust(hspace=0.4)

t = np.arange(0,2,0.001)
symbols = (np.random.randint(0,2,20)+1)
train = np.repeat(symbols, 100)
ax1.plot(t,train)
ax1.set_title("Our Data")
ax1.set_ylabel("Amplitude")
ax1.set_ylim(bottom=0.5, top=2.5)
ax1.set_xlim(left=0, right=2)
for i, symbol in enumerate(symbols):
    ax1.text(i/10+0.035, 2.1, str(symbol-1), fontsize=14, color='red')

f = 25
x = np.sin(2*np.pi*f*t)*train
ax2.plot(t,x)
ax2.set_title("Wireless Signal")
ax2.set_xlabel("Time")
ax2.set_ylabel("Amplitude")
ax2.set_xlim(left=0, right=2)

plt.show()

fig.savefig('../_static/ASK.svg', bbox_inches='tight')
