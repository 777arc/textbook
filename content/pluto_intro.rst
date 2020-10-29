.. _pluto-chapter:

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

While the Python code provided in this textbook should work under Windows, Mac, and Linux, the install instructions below are specific to Ubuntu 18. If you have trouble installing the software on your OS following `the instructions provided by Analog Devices <https://wiki.analog.com/university/tools/pluto/users/quick_start>`_, I recommend installing an Ubuntu 18 VM and trying the instructions below.

1. Install and open `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_.
2. Create a new VM.  For memory size, I recommend using 50% of your computer’s RAM.
3. Create the virtual hard disk, choose VDI, and dynamically allocate size.  15 GB should be enough. If you want to be really safe you can use more.
4. Download Ubuntu 18 Desktop .iso- http://releases.ubuntu.com/18.04/
5. Start the VM. It will ask you for installation media. Choose the Ubuntu 18 desktop .iso file.  Choose “install ubuntu”, use default options, and a pop up will warn you about the changes you are about to make. Hit continue.  Choose name/password and then wait for the VM to finish initializing.  After finishing the VM will restart, but you should power off the VM after the restart.
6. Go into the VM settings (the gear icon).
7. Under system > processor > choose at least 3 CPUs.  If you have an actual video card then in display > video memory > choose something much higher.
8. Start up your VM.
9. I recommend installing VM guest additions. Within the VM go to Devices > Insert Guest Additions CD > hit run when a box pops up.  Follow the instructions. Restart the VM.  The shared clipboard can be enabled through Devices > Shared Clipboard > Bidirectional.

Connecting PlutoSDR
###################

1. If running OSX, within OSX, not the VM, in system preferences, enable "kernel extensions".  Then install HoRNDIS (you may need to reboot after).
2. If running Windows, install this driver: https://github.com/analogdevicesinc/plutosdr-m2k-drivers-win/releases/download/v0.7/PlutoSDR-M2k-USB-Drivers.exe
3. If running Linux you shouldn't have to do anything special.
4. Plug Pluto into the host machine over USB. Make sure to use the middle USB port on Pluto because the other is for power only.  Plugging in Pluto should create a virtual network adapter, i.e., the Pluto appears like a USB ethernet adapter.
5. On the host machine (not VM), open a terminal or your preferred ping tool and ping 192.168.2.1.  If that doesn't work, stop and debug the network interface.
6. Within the VM, open a new terminal
7. Ping 192.168.2.1.  If that doesn't work stop here and debug.  If the ping works then you should be good to go, assuming 192.168.2.1 is actually the Pluto and not some random computer on the network (unlikely but possible).  If you want to be 100% sure 192.168.2.1 is your Pluto, try doing “ssh root@192.168.2.1” pass: analog, and it should log into it.
8. Write down the IP address because you'll need it when we start using the Pluto in Python.

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
 make all -j4
 sudo make install
 sudo ldconfig
 cd bindings/python/
 sudo python3 setup.py.cmakein install
 
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
 sdr = adi.Pluto('ip:192.168.2.1') # or whatever your Pluto's IP is
 sdr.sample_rate = int(2.5e6)
 sdr.rx()

If you get this far without an error, then continue with the next steps.

Changing Pluto's IP Address
####################################

If for some reason the default IP of 192.168.2.1 does not work because you already have a 192.168.2.0 subnet, or because you want multiple Pluto's connected at the same time, you can change the IP using these steps:

1. Edit the config.txt file on the PlutoSDR mass storage device (i.e., the USB-drive looking thing that shows up after you plug in the Pluto).  Enter the new IP you want.
2. Eject the mass storage device (don't unplug the Pluto!). In Ubuntu 18 there's an eject symbol next to the PlutoSDR device, when looking at the file explorer.
3. Wait a few seconds, and then cycle power by unplugging the Pluto and plugging it back in.  Go back into the config.txt to determine if your change(s) saved.

Note that this procedure is also used to flash a different firmware image onto the Pluto. For more details see https://wiki.analog.com/university/tools/pluto/users/firmware.

"Hack" PlutoSDR to Increase RF Range
####################################

The PlutoSDR's ship with a limited center frequency range and sampling rate, but the underlying chip is capable of much higher frequencies.  Follow these steps to unlock the full frequency range of the chip.  Plesae bear in mind that this process is provided by Analog Devices, thus it is as low risk as you can get.  The PlutoSDR's frequency limitation has to do with Analog Devices "binning" the AD9364 based on strict performance requirements at the higher frequencies. .... As SDR enthusiasts and experimenters, we're not too concerned about said performance requirements.

Time to hack! Open a terminal (either host or VM, doesn't matter):

.. code-block:: bash

 ssh root@192.168.2.1

The default password is analog.

You should see the PlutoSDR welcome screen. You have now SSHed into the ARM CPU on the Pluto itself!
Type the following commands in:

.. code-block:: bash

 fw_setenv attr_name compatible
 fw_setenv attr_val ad9364
 reboot

You should now be able to tune up to 6 GHz and down to 70 MHz, not to mention use a sample rate up to 56 MHz!  Yay!

************************
Python Exercises
************************

Instead of providing you code to run, I have created multiple exercises where 95% of the code is provided and the remaining code is fairly straightforward Python for you to create.  The exercises aren't meant to be difficult. They are missing just enough code to get you to think.

Exercise 1: Determine Your USB Throughput
#########################################

Let's try receiving samples from the PlutoSDR, and in the process, see how many samples per second we can push through the USB 2.0 connection.  

**Your task is to create a Python script that determines the rate samples are received in Python, i.e., count the samples received and keep track of time to figure out the rate.  Then, try using different sample_rate's and buffer_size's to see how it impacts the highest achievable rate.**

Keep in mind, if you receive fewer samples per second than the specified sample_rate, it means you are losing/dropping some fraction of samples, which will likely happen at high sample_rate's. The Pluto only uses USB 2.0.

The following code will act as a starting point yet contains the instructions you need to accomplish this task.

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

Additionally, in order to time how long something takes, you can use the following code:

.. code-block:: python

 start_time = time.time()
 # do stuff
 end_time = time.time()
 print('seconds elapsed:', end_time - start_time)

Here are several hints to get you started.

Hint 1: You'll need to put the line "samples = sdr.rx()" into a loop that runs many times (e.g., 100 times). You must count how many samples you get each call to sdr.rx() while tracking how much time has elapsed.

Hint 2: Just because you are calculating samples per second, that doesn't mean you have to perform exactly 1 second's worth of receiving samples. You can divide the number of samples you received by the amount of time that passed.

Hint 3: Start at sample_rate = 10e6 like the code shows because this rate is way more than USB 2.0 can support. You will be able to see how much data gets through.  Then you can tweak rx_buffer_size. Make it a lot larger and see what happens.  Once you have a working script and have fiddled with rx_buffer_size, try adjusting sample_rate. Determine how low you have to go until you are able to receive 100% of samples in Python (i.e., sample at a 100% duty cycle).

Hint 4: In your loop where you call sdr.rx(), try to do as little as possible so that it doesn't add extra delay in execution time. Don't do anything intensive like print from inside the loop.

As part of this exercise you will get an idea for the max throughput of USB 2.0. You can look up online to verify your findings.

As a bonus, try changing the center_freq and rx_rf_bandwidth to see if it impacts the rate you can receive samples off the Pluto.


Exercise 2: Create a Spectrogram/Waterfall
##########################################

For this exercise you will create a spectrogram, a.k.a. waterfall, like we learned about at the end of the :ref:`freq-domain-chapter` chapter.  A spectrogram is simply a bunch of FFT's displayed stacked on top of each other. In other words, it's an image with one axis representing frequency and the other axis representing time.

In the :ref:`freq-domain-chapter` chapter we learned the Python code to perform an FFT.  For this exercise you can use code snippets from the previous exercise, as well as a little bit of basic Python code.

Hints:

1. Try setting sdr.rx_buffer_size to the FFT size so that you always perform 1 FFT for each call to `sdr.rx()`.
2. Build a 2d array to hold all the FFT results where each row is 1 FFT.  A 2d array filled with zeros can be created with: `np.zeros((num_rows, fft_size))`.  Access row i of the array with: `waterfall_2darray[i,:]`.
3. `plt.imshow()` is a convenient way to display a 2d array. It scales the color automatically.

As a stretch goal, make the spectrogram update live.




