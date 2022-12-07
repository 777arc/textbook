.. _modulation-chapter:

###################
Digitale Modulatie
###################

In dit hoofdstuk gaan we met behulp van digitale modulatie data *echt versturen* en draadloze symbolen behandelen! We gaan signalen ontwerpen die "informatie" bevatten, dus 1'en en 0'en, door gebruik van modulatietechnieken zoals ASK, PSK, QAM en FSK. We zullen ook IQ figuren en constellaties behandelen en het hoofdstuk afsluiten met wat Python voorbeelden.

Het grote doel van moduleren is om zoveel mogelijk data in een zo klein mogelijk spectrum te proppen. Technisch gezegd willen we de "spectrale efficientie" (bits/sec/Hz) maximaliseren. 1'en en 0'en sneller versturen zal de bandbreedte van ons signaal groter maken (denk aan de :ref:`Tijd-Frequentie Eigenschappen`), wat betekent dat meer van het spectrum wordt gebruikt. Naast snellere transmissie zullen we ook andere technieken bekijken. Er zijn veel afwegingen voor de modulatiekeuze, maar er is ook vrijheid voor creativiteit.

*******************
Symbolen
*******************
Nieuwe term waarschuwing! Het uitgaande signaal zal worden opgebouwd uit "symbolen". Elk symbool zal een aantal bits aan informatie bevatten en we willen symbolen achter elkaar versturen, duizenden of miljoenen in een rij.

Als een versimpeld voorbeeld, laten we zeggen dat we 1'en en 0'en sturen met hoge en lage spanningsniveaus. Een symbool is zo'n 1 of 0:

.. image:: ../_images/symbols.png
   :scale: 60 % 
   :align: center 

In het bovenstaande voorbeeld stelt een symbool slechts een bit voor. Hoe kunnen we meerdere bits per symbool overbrengen? Laten we bestuderen hoe signalen over ethernetkabels worden gestuurd, wat is vastgelegd in een IEEE standaard genaamd IEEE 802.3 1000BASE-T. In normale situaties gebruikt ethernet een 4-niveau amplitude modulatie (2 bits per symbool) met 8 ns symbolen.

.. image:: ../_images/ethernet.svg
   :align: center 
   :target: ../_images/ethernet.svg

Neem een moment om deze vragen te beantwoorden:

1. Hoeveel bits per seconde worden overgestuurd in bovenstaande voorbeeld?
2. Hoeveel data-draden zouden nodig zijn om 1 gigabit/sec te versturen?
3. Als een modulatieschema 16 verschillende niveaus heeft, hoeveel bits per symbool is dat?
4. Met 16 verschillende niveaus en 8ns symbolen, hoeveel bits per seconde is dat?

.. raw:: html

   <details>
   <summary>Antwoorden</summary>

1. 250 Mbps - (1/8e-9)*2
2. Vier (wat ethernet kabels ook hebben)
3. 4 bits per symbool - log_2(16)
4. 0.5 Gbps - (1/8e-9)*4

.. raw:: html

   </details>

*******************
Draadloze Symbolen
*******************
Vraag: Waarom kunnen we niet het ethernet signaal van hierboven direct versturen? Er zijn veel redenen, de grootste:

1. Lage frequenties hebben *enorme* antennes nodig
2. Blokgolven nemen voor het aantal bits-per-seconde een *overbodige* ruimte van het spectrum in -- herinner van het  :ref:`freq-domain-chapter` hoofdstuk dat scherpe veranderingen in het tijddomein een grote hoeveelheid bandbreedte/spectrum gebruiken:

.. image:: ../_images/square-wave.svg
   :align: center 
   :target: ../_images/square-wave.svg

Wat we voor draadloze signalen doen is beginnen met een draaggolf, wat gewoon een sinusoide is. Bijv., FM-radio gebruikt een draaggolf zoals 101.1 MHz or 100.3 MHz. We moduleren die draaggolf op een bepaalde manier (er zijn vele). In geval van FM-radio is dit een analoge modulatie, niet digitaal, maar het is hetzelfde concept als digitale modulatie. 

Op wat voor manier kunnen we de draaggolf moduleren? Een andere manier om dit te vragen is: Wat zijn de verschillende eigenschappen van een sinusoide?

1. Amplitude
2. Fase
3. Frequentie

We kunnen onze data moduleren op een draaggolf door een of meerdere van de drie aan te passen.

****************************
Amplitude Shift Keying (ASK)
****************************

Amplitude Shift Keying (ASK) is het eerste digitale modulatieschema dat we zullen bespreken want amplitude modulatie is van de drie sinusoide eigenschappen het simpelst te visualiseren. We moduleren letterlijk de **amplitude** van de draaggolf. Hier is een voorbeeld van een 2-niveau ASK, genaamd 2-ASK:

.. image:: ../_images/ASK.svg
   :align: center
   :target: ../_images/ASK.svg

Let op hoe de gemiddelde waarde nul is; dit heeft altijd onze voorkeur.

We kunnen meer dan twee niveau's gebruiken om meer bits per symbool te versturen. Hieronder een voorbeeld van 4-ASK. In dit geval bevat elk symbool 2 bits aan informatie.

.. image:: ../_images/ask2.svg
   :align: center
   :target: ../_images/ask2.svg

Vraag: Hoeveel symbolen kun je in het signaal hierboven onderscheiden? Hoeveel bits worden in totaal verzonden?

.. raw:: html

   <details>
   <summary>Antwoorden</summary>

20 symbolen, dus 40 bits aan informatie

.. raw:: html

   </details>

Hoe kunnen we eigen dit signaal met code vormen? 
Het enige wat we moeten doen is een vector van N monsters per symbool maken en dat vermenigvuldigen met een sinusoide. 
Dit moduleert ons signaal op de draaggolf (de sinusoide is die draaggolf). Het voorbeeld hieronder laat 2-ASK zien met 10 symbolen per seconde.

.. image:: ../_images/ask3.svg
   :align: center
   :target: ../_images/ask3.svg

Het bovenste figuur laat de discrete monsters zien als rode punten, dus ons digitale signaal. Het onderste figuur laat zien hoe het resulterende gemoduleerde signaal eruit ziet, dit zou verzonden kunnen worden door de lucht. In echte systemen is de frequentie van de draaggolf veel hoger dan de snelheid waarmee de symbolen afwisselen. In ons voorbeeld zijn er maar 3 perioden van de draaggolf per symbool, maar in de praktijk zouden er duizenden kunnen zijn, afhankelijk van hoe hoog in het spectrum het verzonden wordt.

************************
Phase Shift Keying (PSK)
************************

Laten we overwegen om de fase te moduleren op dezelfde manier als we met de amplitude hebben gedaan. De simpelste vorm is Binaire PSK (BPSK) waar er twee faseniveaus zijn:

1. Geen faseverandering
2. 180 graden faseverandering

Voorbeeld van BPSK (let op de faseveranderingen):

.. image:: ../_images/bpsk.svg
   :align: center 
   :target: ../_images/bpsk.svg

Het is niet zo leuk om naar figuren te kijken als deze:

.. image:: ../_images/bpsk2.svg
   :align: center 
   :target: ../_images/bpsk2.svg

In plaats daarvan laten we de fase meestal zien in het complexe vlak.

***************************
IQ Diagrammen/Constellaties
***************************
Je hebt al eerder complexe nummers in IQ-diagrammen gezien in het :ref:`Complexe Getallen` deel, maar nu gaan we ze op een nieuwe en grappig manier gebruiken.  
We kunnen de amplitude en fase in een IQ-diagram laten zien voor een gegeven symbool.
In geval van het BPSK voorbeeld haden we fasen van 0 en 180 graden. 
Laten we die punten eens plaatsen in het IQ-diagram.
We gaan uit van een modulus/amplitude van 1.
In de praktijk maakt het niet echt uit welke modulus je gebruikt; een hogere waarde betekent een hoger signaalvermogen, je zou ook gewoon de versterking hoger kunnen zetten.

.. image:: ../_images/bpsk_iq.png
   :scale: 80 % 
   :align: center 

Het bovenstaande IQ-diagram laat zien wat we versturen, of eigenlijk het set van symbolen waaruit we versturen.
Het laat de draaggolf niet zien, dus je kunt dit zien als een basisband voorstelling van de symbolen.
Wanneer we voor een modulatieschema de mogelijke set van symbolen laten zien, noemen we dat de "constellatie". 
Vele modulatieschemas kunnen door hun constellaties worden gedefinieerd.

Om BPSK te ontvangen en decoderen kunnen we IQ-bemonstering toepassen, zoals we hebben geleerd in het vorige hoofdstuk, en bekijken waar de punten terechtkomen in het IQ-diagram.
Door het draadloze kanaal zal er echter wel een willekeurige fasedraaing aanwezig zijn, want het signaal loopt een willekeurige vertraging op wanneer het door de lucht voortplant tussen de antennes.
Verschillende methodes waar we later over leren kunnen deze willekeurige faserotatie teniet doen. 
Hier zijn een paar voorbeelden van hoe het BPSK-signaal eruit zou kunnen zien bij de ontvanger (zonder ruis).

.. image:: ../_images/bpsk3.png
   :scale: 60 % 
   :align: center 

Terug naar PSK. Wat als we vier verschillende fasen zouden willen? Bijv., 0, 90, 180 en 270 graden. 
In dit geval zou het op deze manier gevisualiseerd worden in het IQ-diagram, dit vormt het Quadrature Phase Shift Keying (QPSK) schema:

.. image:: ../_images/qpsk.png
   :scale: 60 % 
   :align: center 

We hebben voor PSK altijd N verschillende hoeken, voor het beste resultaate evenredig verdeeld over de 360 graden.
Meestal laten we ook de eenheidscirkel zien om aan te geven dat alle punten dezelfde modulus hebben:

.. image:: ../_images/psk_set.png
   :scale: 60 % 
   :align: center 

Vraag: Wat is er mis met het onderstaande PSK schema te gebruiken? Is dit een PSK-modulatieschema?

.. image:: ../_images/weird_psk.png
   :scale: 60 % 
   :align: center 

.. raw:: html

   <details>
   <summary>Antwoord</summary>

Er is niets onmogelijks aan dit PSK-schema. Je kunt het zeker gebruiken, maar, het schema is niet zo effectief als mogelijk omdat de symbolen niet univorm verdeeld zijn.
Wanneer we ruis op onze symbolen gaan behandelen wordt schema-efficientie duidelijk.
Het korte antwoord is dat we zoveel mogelijk 'ruimte' tussen de symbolen willen houden voor het geval er ruis is, zodanig dat bij de ontvanger een symbool niet wordt opgevat als een van de andere (incorrecte) symbolen. 
We willen niet een 0 ontvangen als een 1.

.. raw:: html

   </details>

Let's detour back to ASK for a moment.  Note that we can show ASK on the IQ plot just like PSK.  Here is the IQ plot of 2-ASK, 4-ASK, and 8-ASK, in the bipolar configuration, as well as 2-ASK and 4-ASK in the unipolar configuration.

.. image:: ../_images/ask_set.png
   :scale: 50 % 
   :align: center 

As you may have noticed, bipolar 2-ASK and BPSK are the same. A 180 degree phase shift is the same as multiplying the sinusoid by -1.  We call it BPSK, probably because PSK is used way more than ASK.

**************************************
Quadrature Amplitude Modulation (QAM)
**************************************
What if we combine ASK and PSK?  We call this modulation scheme Quadrature Amplitude Modulation (QAM). QAM usually looks something like this:

.. image:: ../_images/64qam.png
   :scale: 90 % 
   :align: center 
   
Here are some other examples of QAM:

.. image:: ../_images/qam.png
   :scale: 50 % 
   :align: center 

For a QAM modulation scheme, we can technically put points wherever we want to on the IQ plot since the phase *and* amplitude are modulated.  The "parameters" of a given QAM scheme are best defined by showing the QAM constellation. Alternatively, you may list the I and Q values for each point, like below for QPSK:

.. image:: ../_images/qpsk_list.png
   :scale: 80 % 
   :align: center 

Note that most modulation schemes, except the various ASKs and BPSK, are pretty hard to "see" in the time domain.  To prove my point, here is an example of QAM in time domain. Can you distinguish between the phase of each symbol in the below image? It's tough.

.. image:: ../_images/qam_time_domain.png
   :scale: 50 % 
   :align: center 

Given the difficulty discerning modulation schemes in the time domain, we prefer to use IQ plots over displaying the time domain signal.  We might, nonetheless, show the time domain signal if there's a certain packet structure or the sequence of symbols matters.

****************************
Frequency Shift Keying (FSK)
****************************

Last on the list is Frequency Shift Keying (FSK).  FSK is fairly simple to understand--we just shift between N frequencies where each frequency is one possible symbol.  However, because we are modulating a carrier, it’s really our carrier frequency +/- these N frequencies. E.g.. we might be at a carrier of 1.2 GHz and shift between these four frequencies:

1. 1.2005 GHz
2. 1.2010 GHz
3. 1.1995 GHz
4. 1.1990 GHz

The example above would be 4-FSK, and there would be two bits per symbol.  A 4-FSK signal in the frequency domain might look something like this:

.. image:: ../_images/fsk.svg
   :align: center 
   :target: ../_images/fsk.svg

If you use FSK, you must ask a critical question: What should the spacing between frequencies be?  We often denote this spacing as :math:`\Delta f` in Hz. We want to avoid overlap in the frequency domain, so :math:`\Delta f` must be large enough.  The width of each carrier in frequency is a function of our symbol rate.  More symbols per second means shorter symbols, which means wider bandwidth (recall the inverse relationship between time and frequency scaling).  The faster we transmit symbols, the wider each carrier will get, and consequently the larger we have to make :math:`\Delta f` to avoid overlapping carriers.  We won't go into any more details about the design of FSK in this textbook.

IQ plots can't be used to show different frequencies. They show magnitude and phase.  While it is possible to show FSK in the time domain, any more than 2 frequencies makes it difficult to distinguish between symbols:

.. image:: ../_images/fsk2.svg
   :align: center
   :target: ../_images/fsk2.svg

As an aside, note that FM radio uses Frequency Modulation (FM) which is like an analog version of FSK.  Instead of having discrete frequencies we jump between, FM radio uses a continuous audio signal to modulate the frequency of the carrier.  Below is an example of FM and AM modulation where the "signal" at the top is the audio signal being modulated onto to the carrier.

.. image:: ../_images/Carrier_Mod_AM_FM.webp
   :align: center
   :target: ../_images/Carrier_Mod_AM_FM.webp

In this textbook we are mainly concerned about digital forms of modulation.

*******************
Differential Coding
*******************

In many wireless (and wired) communications protocols you are likely to run into something called differential coding.  To demonstrate its utility consider receiving a BPSK signal.  As the signal flies through the air it experiences some random delay between the transmitter and receiver, causing a random rotation in the constellation, as we mentioned earlier.  When the receiver synchronizes to it, and aligns the BPSK to the "I" axis, it has no way of knowing if it is 180 degrees out of phase or not, because the constellation looks the same.  So instead of having to send pilot symbols to let it know which cluster represents 1 and which is 0, it can choose to use differential coding and not even worry about it.  Using differential coding also allows us to use a non-coherent receiver which are simpler than coherent receivers.

In its most basic form, which is what is used for BPSK, differential coding involves transmitting a 0 when the input bit is the same as the previous output bit, and transmitting a 1 when they differ.  So we still transmit the same number of bits (except one extra bit is needed at the beginning to start the output sequence), but now we don't have to worry about the 180 degree phase ambiguity.  To demonstrate how this works, consider transmitting the bit sequence [1, 1, 0, 0, 0, 1, 0] using BPSK.  Assume we start the output sequence with 1; it actually doesn't matter whether you use 1 or 0.  After applying differential coding, we would ultimately transmit [1, 0, 1, 1, 1, 1, 0, 0].  The 1's and 0's are still mapped to the positive and negative symbols we discussed earlier.  It might be easier to visualize the input and output sequences stacked like this:

.. image:: ../_images/differential_coding.svg
   :align: center
   :target: ../_images/differential_coding.svg


The big downside to using differential coding is that if you have a bit error, it will lead to two bit errors.  The alternative to using differential coding for BPSK is to add pilot symbols periodically, which are symbols already known by the receiver, and it can use the known values to not only figure out which cluster is 1 and which is 0, but also reverse multipath caused by the channel.  One problem with pilot symbols is that the wireless channel can change very quickly, on the order of tens or hundreds of symbols if it's a moving receiver and/or transmitter, so you would need pilot symbols often enough to reflect the changing channel.  So if a wireless protocol is putting high emphasis on reducing the complexity of the receiver, such as RDS which we study in the :ref:`rds-chapter` chapter, it may choose to use differential coding.

*******************
Python Example
*******************

As a short Python example, let's generate QPSK at baseband and plot the constellation.

Even though we could generate the complex symbols directly, let's start from the knowledge that QPSK has four symbols at 90-degree intervals around the unit circle.  We will use 45, 135, 225, and 315 degrees for our points.  First we will generate random numbers between 0 and 3 and perform math to get the degrees we want before converting to radians.

.. code-block:: python

 import numpy as np
 import matplotlib.pyplot as plt
 
 num_symbols = 1000
 
 x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
 x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
 x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
 x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols
 plt.plot(np.real(x_symbols), np.imag(x_symbols), '.')
 plt.grid(True)
 plt.show()

.. image:: ../_images/qpsk_python.svg
   :align: center 
   :target: ../_images/qpsk_python.svg

Observe how all the symbols we generated overlap. There's no noise so the symbols all have the same value.  Let's add some noise:

.. code-block:: python

 n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
 noise_power = 0.01
 r = x_symbols + n * np.sqrt(noise_power)
 plt.plot(np.real(r), np.imag(r), '.')
 plt.grid(True)
 plt.show()

.. image:: ../_images/qpsk_python2.svg
   :align: center
   :target: ../_images/qpsk_python2.svg

Consider how additive white Gaussian noise (AGWN) produces a uniform spread around each point in the constellation.  If there's too much noise then symbols start passing the boundary (the four quadrants) and will be interpreted by the receiver as an incorrect symbol.  Try increasing :code:`noise_power` until that happens.

For those interested in simulating phase noise, which could result from phase jitter within the local oscillator (LO), replace the :code:`r` with:

.. code-block:: python

 phase_noise = np.random.randn(len(x_symbols)) * 0.1 # adjust multiplier for "strength" of phase noise
 r = x_symbols * np.exp(1j*phase_noise)

.. image:: ../_images/phase_jitter.svg
   :align: center
   :target: ../_images/phase_jitter.svg

You could even combine phase noise with AWGN to get the full experience:

.. image:: ../_images/phase_jitter_awgn.svg
   :align: center
   :target: ../_images/phase_jitter_awgn.svg

We're going to stop at this point.  If we wanted to see what the QPSK signal looked like in the time domain, we would need to generate multiple samples per symbol (in this exercise we just did 1 sample per symbol). You will learn why you need to generate multiple samples per symbol once we discuss pulse shaping.  The Python exercise in the :ref:`pulse-shaping-chapter` chapter will continue where we left off here.

*******************
Further Reading
*******************

#. https://en.wikipedia.org/wiki/Differential_coding

