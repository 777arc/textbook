.. _pluto-adv-chapter:

####################################
PlutoSDR Advanced Topics
####################################

.. image:: ../_static/pluto.png
   :scale: 50 % 
   :align: center 
   
In this chapter we learn some more advanced topics related to the PlutoSDR.  

************************
Automatic Gain Control
************************

Automatic gain control (AGC) is a way to have the receive gain be automatically adjusted, to maintain a suitable signal level (-12dBFS for anyone who is curious).  AGC is not to be confused with the analog-to-digital converter (ADC) that digitizes the signal.  Technically speaking, AGC is a closed-loop feedback circuit that controls the amplifier's gain in response to the received signal.  Its goal is to maintain a constant output power level, when there is a varying input power level.  Typically, the AGC will adjust the gain to avoid saturating the receiver (i.e. hitting the upper limit of the ADC's range), while simultaneously allowing the signal to "fill in" as many ADC bits as possible.  

The RFIC inside the PlutoSDR has an AGC module with a few different settings.  First, note that the receive gain on the Pluto has a range from 0 to 74.5 dB.  When in "manual" AGC mode, AGC is turned off, and you must tell the Pluto what receive gain to use, e.g.:

.. code-block:: python

  gain = 50.0 # 0 to 74.5 dB
  sdr.gain_control_mode_chan0 = "manual"  
  sdr.rx_hardwaregain_chan0 = gain

If you want to enable the AGC, you must choose from one of two modes:

1. :code:`sdr.gain_control_mode_chan0 = "slow_attack"`
2. :code:`sdr.gain_control_mode_chan0 = "fast_attack"`

And with AGC enabled you don't provide a value to :code:`rx_hardwaregain_chan0`.  The fast attack will react quicker, i.e. the gain value will change faster when the received signal changes level.  With either mode, if there is no signal present, just noise, the AGC will max out the gain setting, which means when a signal does show up it will saturate the receiver briefly, until the AGC is able to react and ramp down the gain.  You can always check the current gain level in realtime with:

.. code-block:: python
 
 sdr._get_iio_attr('voltage0','hardwaregain', False)

For more details about the Pluto's AGC, such as how to change the advanced AGC settings, refer to `the "RX Gain Control" section of this page <https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361>`_.
