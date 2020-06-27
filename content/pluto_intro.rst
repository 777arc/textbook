####################################
PlutoSDR Basics
####################################

.. image:: ../_static/pluto.png
   :scale: 50 % 
   :align: center 
   
In this chapter we learn how to use the Python API for the PlutoSDR.  

************************
Software/Drivers Install
************************

Setting up VM
#############

While the Python code provided in this textbook should work under Windows, Mac, and Linux, the install instructions below are specific to Ubuntu 18, so if you are having trouble getting the software set up using Analog Device's instructions on your OS, I would recommend just installing an Ubuntu 18 VM and trying the instructions below.

1. Install VirtualBox - https://www.virtualbox.org/wiki/Downloads, then open it
2. Create new VM.  For memory size, I recommend 50% of your computer’s RAM
3. Create virtual hard disk, choose VDI, and dynamically allocate size.  15 GB should be enough, if you want to be really safe you can use more
4. Download Ubuntu 18 Desktop .iso- http://releases.ubuntu.com/18.04/
5. Start the VM, it will ask you for installation media, choose the Ubuntu 18 desktop .iso file.  Choose “install ubuntu”, use default options, it will pop up warning you about the changes you are about to make, hit continue.  Choose name/password and then wait for it to finish.  After finishing it will restart, but power off the VM after the restart.
6. Go into the VM settings (the gear icon)
7. Under system > processor > choose at least 3 CPUs.  If you have an actual video card then in display > video memory > choose something much higher
8. Start up your VM
9. I recommend installing VM guest additions- within the VM go to Devices > Insert Guest Additions CD > hit run when a box pops up.  Follow instructions. Restart VM.  The shared clipboard can be enabled through Devices > Shared Clipboard > Bidirectional

Connecting PlutoSDR
###################

1. If running OSX, within OSX, not the VM, in system preferences, enable "kernel extensions".  Then install HoRNDIS (you may need to reboot after).
2. If running Windows, install this driver: https://github.com/analogdevicesinc/plutosdr-m2k-drivers-win/releases/download/v0.7/PlutoSDR-M2k-USB-Drivers.exe
3. If running Linux you shouldn't have to do anything special
4. Plug Pluto into the host machine over USB, make sure to use middle port on Pluto.  It should create a virtual network adapter, i.e. the Pluto appears like a USB ethernet adapter
5. On the host machine (not VM), open a terminal or whatever ping tool you want and ping 192.168.2.1.  If that doesn't work stop here, and debug the network interface. 
6. Within the VM, open a new terminal
7. Ping 192.168.2.1.  If that doesn't work stop here and debug.  If the ping works then you should be good to go, assuming 192.168.2.1 was actually the Pluto and not some random computer on the network (unlikely but possible)
8. If you want to be 100% sure 192.168.2.1 is your pluto, try doing “ssh root@192.168.2.1” pass: analog, and it should log into it

Installing PlutoSDR Driver
##########################

The terminal commands below should build and install the latest version of:

1. **libiio**, Analog Device’s “cross-platform” library for interfacing hardware
2. **libad9361-iio**, AD9361 is the specific RF chip inside the PlutoSDR
3. **pyadi-iio**, the Pluto's Python API, *this is our end goal*, but it depends on the previous two libraries


.. code-block:: bash

 sudo apt-get install git libxml2 libxml2-dev bison flex libcdk5-dev cmake python3-pip 
 cd ~
 git clone https://github.com/analogdevicesinc/libiio.git
 cd libiio
 cmake ./
 make all -j3
 sudo make install
 
 cd bindings/python/
 sudo python3 setup.py install
 cd ~
 git clone https://github.com/analogdevicesinc/libad9361-iio.git
 cd libad9361-iio
 cmake ./
 make -j3
 sudo make install
 
 cd ~
 git clone https://github.com/analogdevicesinc/pyadi-iio.git
 cd pyadi-iio
 sudo python3 setup.py install

Testing PlutoSDR Drivers
##########################

Open a new terminal (in your VM) and type the following commands:

.. code-block:: bash

 python3
 import adi
 sdr = adi.Pluto('ip:192.168.2.1')
 sdr.sample_rate = int(2.5e6)
 sdr.rx()

If you get this far without an error then continue with the next steps


"Hack" PlutoSDR to Increase RF Range
####################################

The PlutoSDR's ship with a limited center frequency range and sampling rate, but the underlying chip is capable of much higher, and these steps will unlock the ful range.  Note that this process is provided by Analog Devices, it is as low risk as you can get, the reason for the limitation has to do with Analog Devices "binning" the AD9364 based on strict performance requirements at the higher frequencies, stuff we don't really care about as SDR enthusiasts.

Open terminal (either host or VM, doesn't matter)

.. code-block:: bash

 ssh root@192.168.2.1

Default pass is: analog

You should see the PlutoSDR welcome screen, you have now SSHed into the ARM CPU on the Pluto itself!
Type the following commands in:

.. code-block:: bash

 fw_setenv attr_name compatible
 fw_setenv attr_val ad9364
 reboot

You should now be able to tune up to 6 GHz and use a sample rate up to 56 MHz!

************************
Python Exercises
************************

Instead of just giving you code to run, I have create multiple exercises where 95% of the code is provided, and the remaining code is fairly straightforward Python.  They aren't meant to be difficult exercises, they are missing just enough code to get you to think.

Exercise 1: Determine Your USB Throughput
#########################################

Let's try receiving samples from the PlutoSDR, and in the process, see how many samples per second we can push through the USB 2.0 connection.  

**Your task is to create a Python script that determines the rate samples are actually being received in Python, i.e. count the samples received and keep track of time to figure out the rate.  Then, try using different sample_rate's and buffer sizes to see how it impacts the highest achievable rate.**  

Note that if you find you are receiving less samples per second than the specified sample_rate, it means you are losing/dropping some fraction of samples, which will likely happen at high sample_rate's. 

The following code will act as a starting point, and provides almost all the code you need to accomplish this task.  

.. code-block:: python

 import numpy as np
 import adi
 import matplotlib.pyplot as plt
 import time
 
 sample_rate = 10e6 # Hz
 center_freq = 100e6 # Hz
 
 sdr = adi.Pluto("ip:192.168.2.1")
 sdr.sample_rate = int(sample_rate)
 sdr.rx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
 sdr.rx_lo = int(center_freq)
 sdr.rx_buffer_size = 1024 # this is the buffer the Pluto uses to buffer samples
 samples = sdr.rx() # receive samples off Pluto

In addition, in order to time how long something takes, you can use the following code:

.. code-block:: python

 start_time = time.time()
 # do stuff
 end_time = time.time()
 print('seconds elapsed:', end_time - start_time)

My hint is that you'll need to put the line "samples = sdr.rx()" into a loop, and count how many samples you get each call to sdr.rx(), while keeping track of how much time has elapsed.  Second hint- just because you are calculating samples per second, doesn't mean you have to perform exactly 1 second worth of receiving samples, you can always divide the number of samples you received by the amount of time that passed.

As part of this exercise you will get an idea for the max throughput of USB 2.0, something you can look up online to verify your findings. 

As a bonus, try changing the center_freq to see if/how it impacts the rate you can receive samples off the Pluto.


Exercise 2: Create a Spectrogram/Waterfall
##########################################

For this exercise you will create a spectrogram, a.k.a. waterfall, like we learned about at the end of the Frequency Domain chapter.  A spectrogram is simply a bunch of FFT's displayed stacked on top of each other, i.e. it's an image with one axis representing frequency and the other axis representing time. 

In the Frequency Domain chapter we saw the Python code to perform an FFT.  For this exercise you can use code snippets from the previous exercise, as well as a little bit of basic python code.

Hints:

1. Try setting sdr.rx_buffer_size to the FFT size so that you always perform 1 FFT for each call to `sdr.rx()`.
2. Build a 2d array to hold all the FFT results, each row is 1 FFT.  A 2d array filled with zeros can be created with: `np.zeros((num_rows, fft_size))`.  Access row i of the array with: `waterfall_2darray[i,:]`. 
3. `plt.imshow()` is a convenient way to display a 2d array, and have it scale the color automatically.

As a stretch goal, make the spectrogram update live.



