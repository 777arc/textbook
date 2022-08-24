import matplotlib.pyplot as plt
import numpy as np


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
fig.subplots_adjust(hspace=0.4)

t = np.arange(0,2,0.001)
t2 = np.arange(-0.2,2,0.001)
np.random.seed(1)
symbols = np.random.randint(0,2,10)

# Graph starting with 1
starting_encode_symbol = 1
encode = np.full(fill_value=starting_encode_symbol,shape=[1,1], dtype=int)
previous = starting_encode_symbol
for i in symbols:
    encoded_symbol = i ^ previous
    encode = np.append(encode, encoded_symbol)
    previous = encoded_symbol
print(symbols)
print(encode)

train = np.repeat(symbols, 200)
train2 = np.repeat(encode, 200)
#ax1.plot(t,train+5)
#ax1.plot(t2, train2 + 3, c='#1f77b4')
#ax1.plot(t, train + 1, c='#1f77b4')
ax1.set_title("Starting With 1")
ax1.set_ylim(bottom=1.5, top=7)
ax1.set_xlim(left=-0.5, right=2)
ax1.tick_params(left = False, bottom = False)
ax1.axes.xaxis.set_ticklabels([])
ax1.axes.yaxis.set_ticklabels([])
ax1.axvline(x=0, c="black", label="x=0")

ax1.text(-.35, 6.1, 'Symbols')
ax1.text(-.35, 4.1, 'Encoded')
ax1.text(-.35, 2.1, 'Decoded')

for i, symbol in enumerate(symbols):
    ax1.text(i/5+0.07, 6.1, str(symbol), fontsize=14, color='black')
    ax1.text(i/5+0.07, 2.1, str(symbol), fontsize=14, color='black')
    ax1.annotate('+', xy=(.05 + i/5, 6.1),  xycoords='data', color='red',
            xytext=(-0.07 + i/5, 5.0), textcoords='data',
            arrowprops=dict(color='red', width=.7, headwidth=4, headlength=4),
            horizontalalignment='center', verticalalignment='center',
            )
    ax1.annotate('+', xy=(.05 + i/5, 3.7),  xycoords='data', color='red',
            xytext=(-0.07 + i/5, 3.7), textcoords='data',
            arrowprops=dict(color='red', width=.7, headwidth=4, headlength=4),
            horizontalalignment='center', verticalalignment='center',
            )

for i, symbol in enumerate(encode):
    ax1.text((i - 1)/5+0.07, 4.1, str(symbol), fontsize=14, color='black')

# Graph starting with 0
starting_encode_symbol = 0
encode = np.full(fill_value=starting_encode_symbol,shape=[1,1], dtype=int)
previous = starting_encode_symbol
for i in symbols:
    encoded_symbol = i ^ previous
    encode = np.append(encode, encoded_symbol)
    previous = encoded_symbol
print(symbols)
print(encode)

train = np.repeat(symbols, 200)
train2 = np.repeat(encode, 200)
#ax2.plot(t,train+5)
#ax2.plot(t2, train2 + 3, c='#1f77b4')
#ax2.plot(t, train + 1, c='#1f77b4')
ax2.set_title("Starting With 0")
ax2.set_ylim(bottom=1.5, top=7)
ax2.set_xlim(left=-0.5, right=2)
ax2.tick_params(left = False, bottom = False)
ax2.axes.xaxis.set_ticklabels([])
ax2.axes.yaxis.set_ticklabels([])
ax2.axvline(x=0, c="black", label="x=0")

ax2.text(-.35, 6.1, 'Symbols')
ax2.text(-.35, 4.1, 'Encoded')
ax2.text(-.35, 2.1, 'Decoded')

for i, symbol in enumerate(symbols):
    ax2.text(i/5+0.07, 6.1, str(symbol), fontsize=14, color='black')
    ax2.text(i/5+0.07, 2.1, str(symbol), fontsize=14, color='black')
    ax2.annotate('+', xy=(.05 + i/5, 6.1),  xycoords='data', color='red',
            xytext=(-0.07 + i/5, 5.0), textcoords='data',
            arrowprops=dict(color='red', width=.7, headwidth=4, headlength=4),
            horizontalalignment='center', verticalalignment='center',
            )
    ax2.annotate('+', xy=(.05 + i/5, 3.7),  xycoords='data', color='red',
            xytext=(-0.07 + i/5, 3.7), textcoords='data',
            arrowprops=dict(color='red', width=.7, headwidth=4, headlength=4),
            horizontalalignment='center', verticalalignment='center',
            )

for i, symbol in enumerate(encode):
    ax2.text((i - 1)/5+0.07, 4.1, str(symbol), fontsize=14, color='black')

plt.show()

fig.savefig('../_images/differential_coding.svg', bbox_inches='tight')
