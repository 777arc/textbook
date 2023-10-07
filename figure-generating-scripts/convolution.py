# A big thanks to Wylie (TheWylieStCoyote) for the script, check out his python based intro to signal processing here https://github.com/TheWylieStCoyote/Introduction_to_Signal_Processing_GRCon21/blob/main/notebooks/Section_1.ipynb

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

total_frames = 100

rect = lambda x, center=0, width=1, hight=1.: hight*(np.abs(x-center)<width/2) 
exp = lambda x, center=0, lam=1, amp=1.: amp*np.exp(-lam*(x-center) )*(x-center>=0)
gaussian = lambda x, center=0, sigma=1, amp=1: amp*stats.norm.pdf( (x-center)/sigma )
frame_to_delay = lambda n, total=200, start=-5, stop=5: n/total * (stop-start) + start

conv_func = {
    'rect_exp': {
        'sig1': rect, 'sig1_kwargs': {'center': 0},
        'sig2':  exp, 'sig2_kwargs': {},
        'x_params': (-5, 5, 1001), 'expansion': 0,
    },
    'rect_rect': {
        'sig1': rect, 'sig1_kwargs': {'center': 0},
        'sig2': rect, 'sig2_kwargs': {},
        'x_params': (-3, 3, 1001), 'expansion': 0.5,
    },
    'rect_fat_rect': {
        'sig1': rect, 'sig1_kwargs': {'center': 0, 'width':2},
        'sig2': rect, 'sig2_kwargs': {},
        'x_params': (-3, 3, 1001), 'expansion': 0.5,
    },
    'gaussian_gaussian': {
        'sig1': gaussian, 'sig1_kwargs': {'center': 0},
        'sig2': gaussian, 'sig2_kwargs': {},
        'x_params': (-5, 5, 1001), 'expansion': 3,
    }
}

def build_signal(x, sig, center=0, *args, **kwargs):
    if 'center' not in kwargs.keys():
        kwargs['center'] = center
    elif 'center' in kwargs.keys():
        kwargs['center'] += center
    return sig(x, **kwargs)

def plot_sig1_sig2_conv(x, sig1_y, sig2_y, delay, conv12, fig, gs, ax):
    ax1, ax2 = ax
    sig_product = sig1_y * sig2_y

    ax1.cla()
    ax1.set_xlim((min(x), max(x)))
    ax1.set_ylim((-0.1, 1.1))
    ax1.plot(x, sig_product, 'k', label='f(t)g(t-tau)')
    ax1.plot(x, sig1_y, 'b', label='f(t)')
    ax1.plot(x, sig2_y, 'r', label='g(t-tau)')
    ax1.fill_between(x, sig_product, color='b', alpha=0.2)
    #ax1.legend(loc='upper right')
    ax1.grid(True)

    ax2.cla()
    ax2.set_xlim((min(x), max(x)))
    ax2.set_ylim((-0.1, 1.1))
    ax2.set_xlabel('f*g')
    ax2.plot(delay, conv12, 'k', label='')
    ax2.grid(True)

for name, params in conv_func.items():
    file_name = '../_images/' + name + '_conv.gif'
    sig1, sig1_kwargs = params['sig1'], params['sig1_kwargs']
    sig2, sig2_kwargs = params['sig2'], params['sig2_kwargs']
    x_params, expansion = params['x_params'], params['expansion']
    
    x = np.linspace(*x_params)
    sig1_y = build_signal(x, sig1, **sig1_kwargs)
    sig2_y = build_signal(x, sig2, **sig2_kwargs)[::-1]
    
    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(8, 4)
    gs = fig.add_gridspec(4, 8)
    ax1 = fig.add_subplot(gs[0:2, :])
    ax2 = fig.add_subplot(gs[2:4, :])
    ax = (ax1, ax2)
    
    delay_array, conv_array = [], []
    
    def plot_conv_animate(frame):
        t = frame_to_delay(
            frame, total=total_frames, start=x_params[0]-expansion, 
            stop=x_params[1]+expansion)
        
        tau = (x_params[1])*0 - t
        
        sig2_kwargs_2nd = sig2_kwargs
        
        if 'center' in sig2_kwargs.keys():
            tau -= sig2_kwargs['center']
            del sig2_kwargs_2nd['center']
        
        sig2_y = build_signal(x, sig2, center=tau, **sig2_kwargs_2nd)[::-1]
        conv = np.dot(sig1_y, sig2_y)*(x[1]-x[0])
        
        delay_array.append(t)
        conv_array.append(conv)
        
        plot_sig1_sig2_conv(x, sig1_y, sig2_y, delay_array, conv_array, fig, gs, ax)
    
    anim = FuncAnimation(fig, plot_conv_animate, frames=range(total_frames), interval=40, blit=False)
    
    print("Starting", file_name)
    anim.save(file_name)
    print('Done')
