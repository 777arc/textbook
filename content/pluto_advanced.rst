.. _pluto-adv-chapter:

####################################
PlutoSDR Advanced Topics
####################################

.. image:: ../_static/pluto_adv.png
   :scale: 50 % 
   :align: center 
   
In this chapter we learn some more advanced topics related to the PlutoSDR.  

************************
Receive Gain
************************

The Pluto can be configured to either have a fixed receive gain, or an automatic one, known as Automatic gain control (AGC), which is a way to have the receive gain be automatically adjusted to maintain a strong signal level (-12dBFS for anyone who is curious).  AGC is not to be confused with the analog-to-digital converter (ADC) that digitizes the signal.  Technically speaking, AGC is a closed-loop feedback circuit that controls the amplifier's gain in response to the received signal.  Its goal is to maintain a constant output power level despite a varying input power level.  Typically, the AGC will adjust the gain to avoid saturating the receiver (i.e. hitting the upper limit of the ADC's range), while simultaneously allowing the signal to "fill in" as many ADC bits as possible.  

The RFIC inside the PlutoSDR has an AGC module with a few different settings.  First, note that the receive gain on the Pluto has a range from 0 to 74.5 dB.  When in "manual" AGC mode, AGC is turned off, and you must tell the Pluto what receive gain to use, e.g.:

.. code-block:: python

  
  sdr.gain_control_mode_chan0 = "manual" # turn off AGC
  gain = 50.0 # allowable range is 0 to 74.5 dB
  sdr.rx_hardwaregain_chan0 = gain # set receive gain

If you want to enable the AGC, you must choose from one of two modes:

1. :code:`sdr.gain_control_mode_chan0 = "slow_attack"`
2. :code:`sdr.gain_control_mode_chan0 = "fast_attack"`

And with AGC enabled you don't provide a value to :code:`rx_hardwaregain_chan0`, it will get ignored.  The fast attack will react quicker, i.e. the gain value will change faster when the received signal changes level.  With either mode, if there is no signal present, just noise, the AGC will max out the gain setting, which means when a signal does show up it will saturate the receiver briefly, until the AGC is able to react and ramp down the gain.  You can always check the current gain level in realtime with:

.. code-block:: python
 
 sdr._get_iio_attr('voltage0','hardwaregain', False)

For more details about the Pluto's AGC, such as how to change the advanced AGC settings, refer to `the "RX Gain Control" section of this page <https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361>`_.

**********************************
Transmitting Over the Air Legally
**********************************

Countless times I have been asked by students what frequencies they are allowed to transmit on with an antenna (in the United States).  The short answer is none, as far as I am aware.  Usually when people point to specific regulations that talk about transmit power limits, they are refering to the FCC's "Part 15" regulations.  But those are regulations for manufaturers building and selling devices that operate in the ISM bands, and the regulations discuss how they should be tested.  A Part 15 device is one where an individual does not need a license to operate the device in whatever spectrum its using, but the device itself must be authorized/certified to show they are operating following FCC regulations, before they are marketed and sold.  The Part 15 regulations do call out maximum transmit and received power levels for the different pieces of spectrum, but none of it actually applies to a person transmitting a signal with an SDR or their home-built radio.  The only regulations I could find related to radios that aren't actually products being sold, was specific to operating a low power AM or FM radio station, in the AM/FM bands.  There is also a section on "home-built devices" but it specifically says it doesn't apply to anything constructed from a kit, and it would be a stretch to say a transmit rig using an SDR is a home-built device.  In summary, the FCC regulations aren't as simple as "you can transmit at these frequencies only below these power levels", but rather they are a huge set of rules meant for testing and compliance.  

Another way to look at it would be to say "well these aren't Part 15 devices, but let's follow the Part 15 rules as if they were".  For the 915 MHz ISM band, the rules are that "The field strength of any emissions radiated within the specified frequency band shall not exceed 500 microvolts/meter at 30 meters. The emission limit in this paragraph is based on measurement instrumentation employing an average detector."  So as you can see, it's not as simple as a maximum transmit power in watts. 

If anyone has more details about what is allowed and not allowed, please email me.


