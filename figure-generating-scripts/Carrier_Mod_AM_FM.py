import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']


def fig2img(fig):  # from https://stackoverflow.com/a/61754995/3459491
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = BytesIO()
    fig.savefig(buf, bbox_inches="tight")
    buf.seek(0)
    return Image.open(buf)

def frame(offset=0):
    plt.figure(figsize=(5,3))
    
    time = np.arange(44100.0) - offset
    time = time / 44100.0
    modulator_frequency = 2
    carrier_frequency = 20
    modulation_index = 1  # shared AM / FM

    modulator = np.cos(2.0 * np.pi * modulator_frequency * time) * modulation_index
    carrier = np.cos(2.0 * np.pi * carrier_frequency * time)

    plt.subplot(4, 1, 1)
    plt.axis('off')
    plt.plot(modulator, 'black')
    plt.text(45000, -.6, 'Signal to be\nModulated', {'fontsize': 13})

    plt.subplot(4, 1, 2)
    plt.axis('off')
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.plot(carrier, 'green')
    plt.text(45000, -.2, 'Carrier', {'fontsize': 13})
    
    plt.subplot(4, 1, 3)
    plt.axis('off')
    signal_am = (modulator * 0.8 * carrier) + carrier
    plt.plot(signal_am, 'red')
    plt.text(45000, -.2, 'AM', {'fontsize': 13})

    plt.subplot(4, 1, 4)
    plt.axis('off')
    signal_fm = np.zeros_like(modulator)
    for i, t in enumerate(time):
        signal_fm[i] = np.sin(2 * np.pi * (carrier_frequency * t + modulator[i]))
    plt.plot(signal_fm, 'blue')
    plt.text(45000, -.2, 'FM', {'fontsize': 13})
    return plt

frames = []
frames_tot = 91
for index, offset in enumerate(np.linspace(0, 44100, frames_tot, endpoint=False)):
    print(f'Frame index {index}/{frames_tot-1}')
    fig = frame(offset)
    # f.savefig(f'frame{index:05d}.png', bbox_inches="tight")
    im = fig2img(fig)
    fig.close()
    frames.append(im)
# frames[0].save('waves.gif', save_all=True, append_images=frames[:-1], duration=100, loop=0)

# skip frame 0 from append_images, make the loop slightly cleaner
frames[0].save('../_images/generated/Carrier_Mod_AM_FM.webp', save_all=True, append_images=frames[:-1], duration=100)
