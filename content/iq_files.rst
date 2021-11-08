.. _iq-files-chapter:

#############
IQ Files
#############

In our Python examples we have stored signals as 1d numpy arrays of type "complex float".  In this chapter we learn how signals can be stored to a file and then read back into Python.  Storing signal data in a file is useful.  You may want to record a signal to a file in order to manually analyze it offline or share it with a colleague.

*************************
Binary Files
*************************

Recall that a digital signal at baseband is a sequence of complex numbers.

Example: [0.123 + j0.512,    0.0312 + j0.4123,    0.1423 + j0.06512, ...]

These numbers correspond to [I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, ...]

When we want to save complex numbers to a file, we save them in the format IQIQIQIQIQIQIQIQ.  I.e., we store a bunch of floats in a row, and when we read them back we must separate them back into [I+jQ, I+jQ, ...].

While it's possible to store the complex numbers in a text file or csv file, we prefer to save them in what's called a "binary file" to save space.  At high sample rates your signal recordings could easily be multiple GB, and we want to be as memory efficient as possible.  If you have ever opened a file in a text editor and it looked incomprehensible like the screenshot below, it was probably binary.  Binary files contain a series of bytes, and you have to keep track of the format yourself.  Binary files are the most efficient way to store data, assuming all possible compression has been performed.  Because our signals usually appear like a random sequence of floats, we typically do not attempt to compress the data.  Binary files are used for plenty of other things, e.g., compiled programs (called "binaries").  When used to save signals, we call them binary "IQ files", utilizing the file extension .iq.

.. image:: ../_images/binary_file.png
   :scale: 70 % 
   :align: center 

In Python, the default complex type is np.complex128, which uses two 64-bit floats per sample.  But in DSP/SDR, we tend to use 32-bit floats instead because the ADCs on our SDRs don't have **that** much precision to warrant 64-bit floats.  In Python we will use **np.complex64**, which uses two 32-bit floats.  When you are simply processing a signal in Python it doesn't really matter, but when you go to save the 1d array to a file, you want to make sure it's an array of np.complex64 first.

*************************
Python Examples
*************************

In Python, and numpy specifically, we use the :code:`tofile()` function to store a numpy array to a file.  Here is a short example of creating a simple BPSK signal plus noise and saving it to a file in the same directory we ran our script from:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    num_symbols = 10000

    x_symbols = np.random.randint(0, 2, num_symbols)*2-1 # -1 and 1's
    n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
    r = x_symbols + n * np.sqrt(0.01) # noise power of 0.01
    print(r)
    plt.plot(np.real(r), np.imag(r), '.')
    plt.grid(True)
    plt.show()

    # Now save to an IQ file
    print(type(r[0])) # Check data type.  Oops it's 128 not 64!
    r = r.astype(np.complex64) # Convert to 64
    print(type(r[0])) # Verify it's 64
    r.tofile('bpsk_in_noise.iq') # Save to file


Now examine the details of the file produced and check how many bytes it is.  It should be num_symbols * 8 because we used np.complex64, which is 8 bytes per sample, 4 bytes per float (2 floats per sample).

Using a new Python script, we can read in this file using :code:`np.fromfile()`, like so:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    samples = np.fromfile('bpsk_in_noise.iq', np.complex64) # Read in file.  We have to tell it what format it is
    print(samples)

    # Plot constellation to make sure it looks right
    plt.plot(np.real(samples), np.imag(samples), '.')
    plt.grid(True)
    plt.show()

A big mistake is to forget to tell np.fromfile() the file format. Binary files don't include any information about their format.  By default, np.fromfile() assumes it is reading in an array of float64s.

Most other languages have methods to read in binary files, e.g., in MATLAB you can use fread().  For visually analyzing an RF file see the section below.

*****************************
Visually Analyzing an RF File
*****************************

Although we learned how to create our own spectrogram plot in the :ref:`freq-domain-chapter` Chapter, nothing beats using an already created piece of software, and when it comes to analyzing a long RF recording, I recommend using `inspectrum <https://github.com/miek/inspectrum>`_.  Inspectrum is a fairly simple but powerful graphical tool for scanning through an RF file visually, with fine control over the colormap range and FFT size (zoom amount).  You can hold alt and use the scrollwheel to shift through time.  It has optional cursors to measure the delta-time between two bursts of energy, and the ability to export a slice of the RF file into a new file.  For installation on Debian-based platforms such as Ubuntu, use the following commands:

.. code-block:: bash

 sudo apt-get install qt5-default libfftw3-dev cmake pkg-config libliquid-dev
 git clone https://github.com/miek/inspectrum.git
 cd inspectrum
 mkdir build
 cd build
 cmake ..
 make
 sudo make install
 inspectrum

.. image:: ../_images/inspectrum.jpg
   :scale: 30 % 
   :align: center 
   
*************************
Max Values and Saturation
*************************

When receiving samples off a SDR it's important to know the maximum sample value.  Many SDRs will output the samples as floats using a maximum value of 1.0 and minimum value of -1.0.  Other SDRs will give you samples as integers, usually 16-bit, in which case the max and min values will be +32767 and -32768 (unless otherwise specified), and you can choose to divide by 32,768 to convert them to floats from -1.0 to 1.0.  The reason to be aware of the maximum value for your SDR is due to saturation: when receiving an extremely loud signal (or if the gain is set too high), the receiver will "saturate" and it will truncate the high values to whatever the maximum sample value is.  The ADCs on our SDRs have a limited number of bits.  When making an SDR app it's wise to always be checking for saturation, and when it happens you should indicate it somehow.

A signal that is saturated will look choppy in the time domain, like this:

.. image:: ../_images/saturated_time.png
   :scale: 30 % 
   :align: center 

Because of the sudden changes in time domain, due to the truncation, the frequency domain might look smeared.  In other words, the frequency domain will include false features; features that resulted from the saturation and are not actually part of the signal, which can throw people off when analyzing a signal. 

*************************
Annotating IQ Files
*************************

Since the IQ file itself doesn't have any metadata associated with it, it's common to have a 2nd file, containing information about the signal, with the same filename but a .txt or other file extension.  This should at a minimum include the sample rate used to collect the signal, and the frequency to which the SDR was tuned.  After analyzing the signal, the metadata file could include information about sample ranges of interesting features, such as bursts of energy.  The sample index is simply an integer that starts at 0 and increments every complex sample.  If you knew that there was energy from sample 492342 to 528492, then you could read in the file and pull out that portion of the array: :code:`samples[492342:528493]`.
