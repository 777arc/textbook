.. _pulse-shaping-chapter:

#######################
Pulse Shaping
#######################

Dit hoofdstuk gaat over pulsvorming, inter-symbool-interferentie, matched filters, en raised-cosine filters.
We zullen uiteindelijk Python gebruiken om pulsvorming toe te passen op BPSK symbolen.
Je kunt dit hoofdstuk als deel 2 van het Filters hoofdstuk opvatten, waarin we een duik nemen in het vormgeven van pulsen.

**********************************
Inter-Symbool-Interferentie (ISI)
**********************************

In het :ref:`filters-chapter` hoofdstuk hebben we geleerd dat blokvormige symbolen/pulsen een overbodige hoeveelheid van het spectrum gebruiken, en dat we het gebruik van het spectrum drastisch kunnen verminderen door gebruik het *vormgeven* van onze pulsen.
Maar, je kunt niet zomaar elk laagdoorlaatfilter toepassen want dan krijg je last van inter-symbool-interferentie (ISI). Dit is wanneer symbolen elkaar storen en overspoelen.

Wanneer we digitale symbolen versturen, dan versturen we ze zij-aan-zij (i.t.t. een bepaalde tijd te wachten tussen pulsen). Wanneer je een pulsvormend filter toepast worden deze pulsen uitgerekt in het tijddomein (om het te samen te drukken in frequentie), waardoor aangrenzende symbolen elkaar gaan overlappen. Dit overlappen is niet erg zolang het pulsvormende filter aan een eis voldoet: alle pulsen behalve een, moeten optellen tot 0 op elke veelvoud van de symboolperiode :math:`T`. Dit is het beste te begrijpen door een figuur:

.. image:: ../_images/pulse_train.svg
   :align: center 
   :target: ../_images/pulse_train.svg

Zoals je ziet is op elke interval van :math:`T` er maar een pulse hoog, terwijl alle andere pulsen 0 zijn en de x-as kruisen. Wanneer de ontvanger het signaal sampled doet het dit op het perfecte moment (wanner de puls het hoogst is), dus alleen dat moment in tijd is belangrijk. Meestal vindt er nog een vorm van symboolsynchronisatie plaats bij de ontvanger om ervoor te zorgen dat de symbolen inderdaad bij de toppen wordt gesampled.

**********************************
Matched Filter
**********************************

Een truc dat in draadloze communicatie wordt toegepast heet matched filters (op elkaar afgestemde filters).
Om deze afstemming van filters te begrijpen zul je eerste deze twee punten moeten snappen:

1. De pulsen zoals hierboven besproken hoeven *alleen bij de ontvanger* perfect uitgelijnd te zijn voor het samplen. Tot dat punt maakt het niet uit of er ISI plaatsvindt, de signalen kunnen door het luchtruim vliegen met ISI zonder problemen.

2. We willen een laagdoorlaatfilter bij de zender om te voorkomen dat ons signaal teveel van het spectrum gebruikt. De ontvanger heeft echter ook een laagdoorlaatfilter nodig om zoveel mogelijk ruis/interferentie op on signaal weg te filteren. Dit resulteert in een laagdoorlaatfilter bij zender (Tx) alsmede de ontvanger (Rx). De ontvanger sampled het signaal dan na beide filters (en natuurlijk de effecten van het draadloze kanaal).

Wat we in moderne communicatie doen, is het opsplitsen van het vormgevende filter tussen Tx en Rx. Ze *moeten* niet identiek zijn, maar, theoretisch gezien, is het *optimaal* om identieke filters te gebruiken om de SNR te maximaliseren bij de aanwezigheid van AWGN. Deze vorm van filteren heet het "matched filter" concept.

Another way of thinking about matched filters is that the receiver correlates the received signal with the known template signal.  The template signal is essentially the pulses the transmitter sends, irrespective of the phase/amplitude shifts applied to them.  Recall that filtering is done by convolution, which is basically correlation (in fact they are mathematically the same when the template is symmetrical).  This process of correlating the received signal with the template gives us our best chance at recovering what was sent, and it is why it's theoretically optimal.  As an analogy, think of an image recognition system that looks for faces using a template of a face and a 2D correlation:

.. image:: ../_images/face_template.png
   :scale: 70 % 
   :align: center 

**********************************
Splitting a Filter in Half
**********************************

How do we actually split a filter in half?  Convolution is associative, which means:

.. math::
 (f * g) * h = f * (g * h)

Let's imagine :math:`f` as our input signal, and :math:`g` and :math:`h` are filters.  Filtering :math:`f` with :math:`g`, and then :math:`h` is the same as filtering with one filter equal to :math:`g * h`.

Also, recall that convolution in time domain is multiplication in frequency domain:

.. math::
 g(t) * h(t) \leftrightarrow G(f)H(f)
 
To split a filter in half you can take the square root of the frequency response.

.. math::
 X(f) = X_H(f) X_H(f) \quad \mathrm{where} \quad X_H(f) = \sqrt{X(f)}

Below shows a simplified diagram of a transmit and receive chain, with a Raised Cosine (RC) filter being split into two Root Raised Cosine (RRC) filters; the one on the transmit side is the pulse shaping filter, and the one on the received side is the matched filter.  Together, they cause the pulses at the demodulator to appear as if they had been pulse shaped with a single RRC filter.

.. image:: ../_images/splitting_rc_filter.svg
   :align: center 
   :target: ../_images/splitting_rc_filter.svg


**********************************
Specific Pulse Shaping Filters
**********************************

We know that we want to:

1. Design a filter that reduces the bandwidth of our signal (to use less spectrum) and all pulses except one should sum to zero every symbol interval.

2. Split the filter in half, putting one half in the Tx and the other in the Rx.

Let's look at some specific filters that are common to use for pulse-shaping.

Raised-Cosine Filter
#########################

The most popular pulse-shaping filter seems to be the "raised-cosine" filter.  It's a good low-pass filter for limiting the bandwidth our signal will occupy, and it also has the property of summing to zero at intervals of :math:`T`:

.. image:: ../_images/raised_cosine.svg
   :align: center 
   :target: ../_images/raised_cosine.svg

Note that the above plot is in the time domain. It depicts the impulse response of the filter.  The :math:`\beta` parameter is the only parameter for the raised-cosine filter, and it determines how quickly the filter tapers off in the time domain, which will be inversely proportional with how quickly it tapers off in frequency:

.. image:: ../_images/raised_cosine_freq.svg
   :align: center 
   :target: ../_images/raised_cosine_freq.svg

The reason it's called the raised-cosine filter is because the frequency domain when :math:`\beta = 1` is a half-cycle of a cosine wave, raised up to sit on the x-axis.

The equation that defines the impulse response of the raised-cosine filter is:

.. math::
 h(t) = \frac{1}{T} \mathrm{sinc}\left( \frac{t}{T} \right) \frac{\cos\left(\frac{\pi\beta t}{T}\right)}{1 - \left( \frac{2 \beta t}{T}   \right)^2}

More information about the :math:`\mathrm{sinc}()` function can be found `here <https://en.wikipedia.org/wiki/Sinc_function>`_.

Remember: we split this filter between the Tx and Rx equally.  Enter the Root Raised Cosine (RRC) Filter!

Root Raised-Cosine Filter
#########################

The root raised-cosine (RRC) filter is what we actually implement in our Tx and Rx. Combined they form a normal raised-cosine filter, as we discussed.  Because splitting a filter in half involves a frequency-domain square root, the impulse response gets a bit messy:

.. image:: ../_images/rrc_filter.png
   :scale: 70 % 
   :align: center 

Luckily it's a heavily used filter and there are plenty of implementations, including `in Python <https://commpy.readthedocs.io/en/latest/generated/commpy.filters.rrcosfilter.html>`_.

Other Pulse-Shaping Filters
###########################

Other filters include the Gaussian filter, which has an impulse response resembling a Gaussian function.  There is also a sinc filter, which is equivalent to the raised-cosine filter when :math:`\beta = 0`.  The sinc filter is more of an ideal filter, meaning it eliminates the frequencies necessary without much of a transition region.

**********************************
Roll-Off Factor
**********************************

Let's scrutinize the parameter :math:`\beta`.  It is a number between 0 and 1, and is called the "roll-off" factor or sometimes "excess bandwidth".  It determines how fast, in the time domain, the filter rolls off to zero.  Recall that, to be used as a filter, the impulse response should decay to zero on both sides:

.. image:: ../_images/rrc_rolloff.svg
   :align: center 
   :target: ../_images/rrc_rolloff.svg

More filter taps are required the lower :math:`\beta` gets.  When :math:`\beta = 0` the impulse response never fully hits zero, so we try to get :math:`\beta` as low as possible without causing other issues.  The lower the roll-off, the more compact in frequency we can create our signal for a given symbol rate, which is always important.

A common equation used to approximate bandwidth, in Hz, for a given symbol rate and roll-off factor is:

.. math::
    \mathrm{BW} = R_S(\beta + 1)

:math:`R_S` is the symbol rate in Hz.  For wireless communications we usually like a roll-off between 0.2 and 0.5.  As a rule of thumb, a digital signal that uses symbol rate :math:`R_S` is going to occupy a little more than :math:`R_S` worth of spectrum, including both positive and negative portions of spectrum.  Once we upconvert and transmit our signal, both sides certainly matter.  If we transmit QPSK at 1 million symbols per second (MSps), it will occupy around 1.3 MHz.  The data rate will be 2 Mbps (recall that QPSK uses 2 bits per symbol), including any overhead like channel coding and frame headers.

**********************************
Python Exercise
**********************************

As a Python exercise let's filter and shape some pulses.  We will use BPSK symbols so that it's easier to visualize--prior to the pulse-shaping step, BPSK involves transmitting 1's or -1's with the "Q" portion equal to zero.  With Q equal to zero we can plot the I portion only, and it's easier to look at.

In this simulation we will use 8 samples per symbol, and instead of using a square-wave looking signal of 1's and -1's, we use a pulse train of impulses.  When you put an impulse through a filter, the output is the impulse response (hence the name).  Therefore if you want a series of pulses, you want to use impulses with zeros in between to avoid square pulses.

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal

    num_symbols = 10
    sps = 8

    bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0's

    x = np.array([])
    for bit in bits:
        pulse = np.zeros(sps)
        pulse[0] = bit*2-1 # set the first value to either a 1 or -1
        x = np.concatenate((x, pulse)) # add the 8 samples to the signal
    plt.figure(0)
    plt.plot(x, '.-')
    plt.grid(True)
    plt.show()

.. image:: ../_images/pulse_shaping_python1.png
   :scale: 80 % 
   :align: center 

At this point our symbols are still 1's and -1's.  Don't be caught up in the fact we used impulses.  In fact, it might be easier to *not* visualize the impulses response but rather think of it as an array:

.. code-block:: python

 bits: [0, 1, 1, 1, 1, 0, 0, 0, 1, 1]
 BPSK symbols: [-1, 1, 1, 1, 1, -1, -1, -1, 1, 1]
 Applying 8 samples per symbol: [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, ...]

We will create a raised-cosine filter using a :math:`\beta` of 0.35, and we will make it 101 taps long to give the signal enough time to decay to zero.  While the raised cosine equation asks for our symbol period and a time vector :math:`t`, we can assume a **sample** period of 1 second to "normalize" our simulation.  It means our symbol period :math:`Ts` is 8 because we have 8 samples per symbol.  Our time vector then will be a list of integers.  With the way the raised-cosine equation works, we want :math:`t=0` to be in the center.  We will generate the 101-length time vector starting at -51 and ending at +51.

.. code-block:: python

    # Create our raised-cosine filter
    num_taps = 101
    beta = 0.35
    Ts = sps # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
    t = np.arange(-50, 51) # remember it's not inclusive of final number
    h = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
    plt.figure(1)
    plt.plot(t, h, '.')
    plt.grid(True)
    plt.show()


.. image:: ../_images/pulse_shaping_python2.png
   :scale: 80 % 
   :align: center 

Note how the output definitely decays to zero.  The fact we are using 8 samples per symbol determines how narrow this filter appears and how fast it decays to zero.  The above impulse response looks like a typical low-pass filter, and there's really no way for us to know that it's a pulse-shaping specific filter versus any other low-pass filter.

Lastly, we can filter our signal :math:`x` and examine the result.  Don't focus heavily on the introduction of a for loop in the provided code.  We'll discuss why it's there after the code block.

.. code-block:: python 
 
    # Filter our signal, in order to apply the pulse shaping
    x_shaped = np.convolve(x, h)
    plt.figure(2)
    plt.plot(x_shaped, '.-')
    for i in range(num_symbols):
        plt.plot([i*sps+num_taps//2,i*sps+num_taps//2], [0, x_shaped[i*sps+num_taps//2]])
    plt.grid(True)
    plt.show()

.. image:: ../_images/pulse_shaping_python3.svg
   :align: center 
   :target: ../_images/pulse_shaping_python3.svg

This resulting signal is summed together from many of our impulse responses, with approximately half of them first multiplied by -1.  It might look complicated, but we will step through it together.

Firstly, there are transient samples before and after the data because of the filter and the way convolution works.  These extra samples get included in our transmission but they don't actually contain "peaks" of pulses.

Secondly, the vertical lines were created in the for loop for visualization's sake.  They are meant to demonstrate where intervals of :math:`Ts` occur.  These intervals represent where this signal will be sampled by the receiver.  Observe that for intervals of :math:`Ts` the curve has the value of exactly 1.0 or -1.0, making them the ideal points in time to sample.

If we were to upconvert and transmit this signal, the receiver would have to determine when the boundaries of :math:`Ts` are e.g., using a symbol synchronization algorithm.  That way the receiver knows *exactly* when to sample to get the right data.  If the receiver samples a little too early or late, it will see values that are slightly skewed due to ISI, and if it's way off then it will get a bunch of weird numbers.

Here is an example, created using GNU Radio, that illustrates what the IQ plot (a.k.a. constellation) looks like when we sample at the right and wrong times.  The original pulses have their bit values annotated.

.. image:: ../_images/symbol_sync1.png
   :scale: 50 % 
   :align: center 

The below graph represents the ideal position in time to sample, along with the IQ plot:

.. image:: ../_images/symbol_sync2.png
   :scale: 40 % 
   :align: center 

Compare that to the worst time to sample.  Notice the three clusters in the constellation.  We are sampling directly in between each symbol; our samples are going to be way off.

.. image:: ../_images/symbol_sync3.png
   :scale: 40 % 
   :align: center 

Here is another example of a poor sample time, somewhere in between our ideal and worst cases. Heed the four clusters.  With a high SNR we might be able to get away with this sampling time interval, though it isn't advisable.

.. image:: ../_images/symbol_sync4.png
   :scale: 40 % 
   :align: center 
   
Remember that our Q values are not shown on the time domain plot because they are roughly zero, allowing the IQ plots to spread horizontally only.
