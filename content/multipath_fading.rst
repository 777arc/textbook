.. _multipath-chapter:

#######################
Multipath Fading
#######################

So far we have only discussed the "AWGN Channel", i.e., a model for a wireless channel where the signal is simply added to noise.  In this chapter we introduce multipath, which is a propagation phenomenon that results in signals reaching the receiver by two or more paths, which we experience in real-world wireless systems.

*************************
Multipath
*************************

All realistic wireless channels include many "reflectors", given that RF signals bounce.  Any object between or near the transmitter (Tx) or receiver (Rx) can cause additional paths the signal travels along.  Each path experiences a different phase shift (delay) and attenuation (amplitude scaling).  At the receiver, all of the paths add up.  They can add up constructively, destructively, or a mix of both.  We call this concept of multiple signal paths "multipath".  There is the Line-of-Sight (LOS) path, and then all other paths.  In the example below, we show the LOS path and a single non-LOS path:

.. image:: ../_static/multipath.png
   :scale: 80 % 
   :align: center 

Destructive interference can happen if you get unlucky with how the paths sum together.  Consider the example above with just two paths.  Depending on the frequency and the exact distance of the paths, the two paths can be received 180 degrees out of phase at roughly the same amplitude, causing them to null out each other (depicted below).  You may have learned about constructive and destructive interference in physics class.  In wireless systems when the paths destructively combine, we call this interference "deep fade" because our signal briefly disappears.

.. image:: ../_static/destructive_interference.png
   :scale: 70 % 
   :align: center 

Paths can also add up constructively, causing a strong signal to be received.  Each path has a different phase shift and amplitude, which we can visualize on a plot in the time domain called a "power delay profile":

.. image:: ../_static/multipath2.png
   :scale: 70 % 
   :align: center 

The first path, the one closest to the y-axis, will always be the LOS path (assuming there is one) because there's no way for any other path to reach the receiver faster than the LOS path.  Typically the magnitude will decrease as the delay increases, since a path that took longer to show up at the receiver will have traveled further.

*************************
Fading
*************************

What usually happens is we get a mix of constructive and destructive interference, and it changes over time as the Rx, Tx, or environment is moving/changing.  We use the term "fading" when referring to the effects of a multipath channel **changing** over time.  That's why we often refer to it as "multipath fading"; it's really the combination of constructive/destructive interference and a changing environment. What we end up with is a SNR that varies over time; changes are usually on the order of milliseconds to microseconds, depending on how fast the Tx/Rx is moving. Beneath is a plot of SNR over time in milliseconds that demonstrates multipath fading.

.. image:: ../_static/multipath_fading.png
   :scale: 100 % 
   :align: center 

There are two types of fading from a **time** domain perspective:

- **Slow Fading:** The channel doesn't change within one packet's worth of data.  That is, a deep null during slow fading will wipe out the whole packet.
- **Fast Fading:** The channel changes very quickly compared to the length of one packet.  Forward error correction, combined with interleaving, can combat fast fading.

There are also two types of fading from a **frequency** domain perspective:

**Frequency Selective Fading**: The constructive/destructive interference changes within the frequency range of the signal.  When we have a wideband signal, we span a large range of frequencies.  Recall that wavelength determines whether it's constructive or destructive.  Well if our signal spans a wide frequency range, it also spans a wide wavelength range (since wavelength is the inverse of frequency).  Consequently we can get different channel qualities in different portions of our signal (in the frequency domain).  Hence the name frequency selective fading.

**Flat Fading**: Occurs when the signal's bandwidth is narrow enough that all frequencies experience roughly the same channel.  If there is a deep fade then the whole signal will disappear (for the duration of the deep fade).  

In the figure below, the :red:`red` shape shows our signal in the frequency domain, and the black curvy line shows the current channel condition over frequency.  Because the narrower signal is experiencing the same channel conditions throughout the whole signal, it's experiencing flat fading.  The wider signal is very much experiencing frequency selective fading.

.. image:: ../_static/flat_vs_freq_selective.png
   :scale: 70 % 
   :align: center 

Here is an example of a 16 MHz wide signal that is continuously transmitting.  There are several moments in the middle where there's a period of time a piece of signal is missing.  This example depicts frequency selective fading, which causes holes in the signal that wipe out some frequencies but not others.

.. image:: ../_static/fading_example.png
   :scale: 60 % 
   :align: center 
   
   
****************************
Mitigating Multipath Fading
****************************

In modern communications, we have developed ways to combat multipath fading.  

CDMA
#####

3G cellular uses a technology called code division multiple access (CDMA).  With CDMA you take a narrowband signal and spread it over a wide bandwidth before transmitting it (using a spread spectrum technique called DSSS).  Under frequency selective fading, it's unlikely that all frequencies will be in a deep null at the same time.  At the receiver the spreading is reversed, and this de-spreading process greatly mitigates a deep null.

.. image:: ../_static/cdma.png
   :scale: 100 % 
   :align: center 

OFDM 
#####

4G cellular, WiFi, and many other technologies use a scheme called orthogonal frequency-division multiplexing (OFDM).  OFDM uses something called subcarriers, where we split up the signal in the frequency domain into a bunch of narrow signals squashed together.  To combat multipath fading we can avoid assigning data to subcarriers that are in a deep fade, although it requires the receiving end to send channel information back to the transmitter quick enough.  We can also assign high order modulation schemes to subcarriers with great channel quality to maximize our data rate.






