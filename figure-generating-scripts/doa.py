

# Mention in chapter
'''
sdr requirements (phase coherent rx channels)
transmit side beamforming is pretty easy its just pointing in a specific direction
uses in cellular and satellite ground stations and satellites
grating lobes when spacing is greater than half wavelenght, its like spatial aliasing because you arent sampling in space fine enough
including beamforming in the title

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

sample_rate = 1e6
N = 10000 # number of samples to simulate

# Create a tone to act as the transmitted signal
t = np.arange(N)/sample_rate
f_tone = 0.02e6
tx = np.exp(2j*np.pi*f_tone*t)

# Simulate three omnidirectional antennas in a line with 1/2 wavelength between adjancent ones, receiving a signal that arrives at an angle

d = 0.5
Nr = 3
theta_degrees = 20 # direction of arrival
theta = theta_degrees / 180 * np.pi # convert to radians
a = np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta))
print(a)

# we have to do a matrix multiplication of a and tx, so first lets convert both to matrix' instead of numpy arrays which dont let us do 1d matrix math
a = np.asmatrix(a)
tx = np.asmatrix(tx)

# so how do we use this? simple:

r = a.T @ tx  # matrix multiply. dont get too caught up by the transpose a, the important thing is we're multiplying the array factor by the tx signal
print(r.shape) # r is now going to be a 2D array, 1d is time and 1d is spatial

# Plot the real part of the first 200 samples of all three elements
if False:
    fig, (ax1) = plt.subplots(1, 1, figsize=(7, 3))
    ax1.plot(np.asarray(r[0,:]).squeeze().real[0:200]) # the asarray and squeeze are just annoyances we have to do because we came from a matrix
    ax1.plot(np.asarray(r[1,:]).squeeze().real[0:200])
    ax1.plot(np.asarray(r[2,:]).squeeze().real[0:200])
    ax1.set_ylabel("Samples")
    ax1.set_xlabel("Time")
    ax1.grid()
    ax1.legend(['0','1','2'], loc=1)
    plt.show()
    fig.savefig('../_images/doa_time_domain.svg', bbox_inches='tight')
    exit()
# note the phase shifts, they are also there on the imaginary portions of the samples

# So far this has been simulating the recieving of a signal from a certain angle of arrival
# in your typical DOA problem you are given samples and have to estimate the angle of arrival(s)
# there are also problems where you have multiple receives signals from different directions and one is the SOI while another might be a jammer or interferer you have to null out

# One thing we didnt both doing- lets add noise to this recieved signal.
# AWGN with a phase shift applied is still AWGN so we can add it after or before the array factor is applied, doesnt really matter, we'll do it after
# we need to make sure each element gets an independent noise signal added

n = np.random.randn(Nr, N) + 1j*np.random.randn(Nr, N)
r = r + 0.1*n

if False:
    fig, (ax1) = plt.subplots(1, 1, figsize=(7, 3))
    ax1.plot(np.asarray(r[0,:]).squeeze().real[0:200]) # the asarray and squeeze are just annoyances we have to do because we came from a matrix
    ax1.plot(np.asarray(r[1,:]).squeeze().real[0:200])
    ax1.plot(np.asarray(r[2,:]).squeeze().real[0:200])
    ax1.set_ylabel("Samples")
    ax1.set_xlabel("Time")
    ax1.grid()
    ax1.legend(['0','1','2'], loc=1)
    plt.show()
    fig.savefig('../_images/doa_time_domain_with_noise.svg', bbox_inches='tight')
    exit()

# OK lets use this signal r but pretend we don't know which direction the signal is coming in from, lets try to figure it out
# The "conventional" beamforming approach involves scanning through (sampling) all directions from -pi to +pi (-180 to +180) 
# and at each direction we point the array towards that angle by applying the weights associated with pointing in that direction
# which will give us a single 1D array of samples, as if we recieved it with 1 antenna
# we then calc the mean of the magnitude squared as if we were doing an energy detector
# repeat for a ton of different angles and we can see which angle gave us the max


''' signal from hack-a-sat 4 where we wanted to find the direction of the least energy because there were jammers
N = 880 # num samples
r = np.zeros((Nr,N), dtype=np.complex64)
r[0, :] = np.fromfile('/home/marc/hackasat4/darkside/dishy/Receiver_0.bin', dtype=np.complex64)
r[1, :] = np.fromfile('/home/marc/hackasat4/darkside/dishy/Receiver_1.bin', dtype=np.complex64)
r[2, :] = np.fromfile('/home/marc/hackasat4/darkside/dishy/Receiver_2.bin', dtype=np.complex64)
'''

if False:
    theta_scan = np.linspace(-1*np.pi, np.pi, 1000) # 100 different thetas between -180 and +180 degrees
    results = []
    for theta_i in theta_scan:
        #print(theta_i)
        w = np.asmatrix(np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta_i))) # look familiar?
        r_weighted = np.conj(w) @ r # apply our weights corresponding to the direction theta_i
        r_weighted = np.asarray(r_weighted).squeeze() # get it back to a normal 1d numpy array
        results.append(np.mean(np.abs(r_weighted)**2)) # energy detector

    print(theta_scan[np.argmax(results)] * 180 / np.pi) # 19.99999999999998

    fig, (ax1) = plt.subplots(1, 1, figsize=(7, 3))
    ax1.plot(theta_scan*180/np.pi, results) # lets plot angle in degrees
    ax1.plot([20],[np.max(results)],'r.')
    ax1.text(-5, np.max(results) + 0.7, '20 degrees')
    ax1.set_xlabel("Theta [Degrees]")
    ax1.set_ylabel("DOA Metric")
    ax1.grid()
    plt.show()
    fig.savefig('../_images/doa_conventional_beamformer.svg', bbox_inches='tight')

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta_scan, results) # MAKE SURE TO USE RADIAN FOR POLAR
    ax.set_theta_zero_location('N') # make 0 degrees point up
    ax.set_theta_direction(-1) # increase clockwise
    ax.set_rgrids([0,2,4,6,8]) 
    ax.set_rlabel_position(22.5)  # Move grid labels away from other labels
    plt.show()

    fig.savefig('../_images/doa_conventional_beamformer_polar.svg', bbox_inches='tight')