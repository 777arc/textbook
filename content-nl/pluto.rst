.. _pluto-chapter:

####################################
PlutoSDR in Python
####################################

.. image:: ../_images/pluto.png
   :scale: 50 % 
   :align: center 
   
Je zult in de hoofdstuk leren om de Python API voor de `PlutoSDR <https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html>`_ te gebruiken; een goedkope SDR van Analog Devices.  
We zullen de stappen behandelen om de drivers/software voor de PlutoSDR te kunnen draaien, en behandelen hoe je kunt zenden en ontvangen met de PlutoSDR in Python.

****************************
Software/Drivers Installatie
****************************

Een VM opzetten
###############
Terwijl de gegeven Python voorbeelden ook onder Windows, Mac en Linux zouden moeten werken, zijn de instructies in het specifiek geschreven voor Ubuntu 22. Als je moeite hebt om de software op jouw OS te installeren met behulp van `de instructies van Analog Devices <https://wiki.analog.com/university/tools/pluto/users/quick_start>`_, raad ik aan om een Ubuntu 22 VM te installeren volgens de instructies hieronder. Onder Windows 11 is een alternatieve route, Windows Subsystem for Linux (WSL) met Ubuntu 22. Dit draait vrij goed en ondersteund standaard al grafische linux applicaties. 

1. Installeer en open `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_.
2. Maak een nieuwe VM aan. Voor de geheugengrootte raad ik 50% van je RAM aan.
3. Creeer een dynamisch groeiende virtuele hardeschijf, kies hiervoor VDI. 15 GB zou voldoende moeten zijn. Als je zeker wilt zijn kun je nog meer toekennen.
4. Download de Ubuntu 22 Desktop .iso- https://ubuntu.com/download/desktop
5. Start de VM. Kies het gedownloade .iso bestand als installatiemedium. Kies “install ubuntu”, met de standaard opties en klik op "continue" bij het venster wat je waarschuwt over de veranderingen. Kies een naam/wachtwoord en wacht op de VM om te installeren. Wanneer de installatie klaar is zal de VM herstarten. Schakel na de herstart de VM uit.
6. Ga naar de VM instellingen (het tandwieltje).
7. Onder system > processor > kies tenminste 3 processors. Als je een discrete video kaart hebt dan kun je meer videogeheugen toekennen onder display > video memory .
8. Start jouw VM.
9. Ik raad ook aan om de "VM guest additions" te installeren. Ga binnen de VM naar Devices > Insert Guest Additions CD > druk op "run" in het nieuwe venster en volg de instructies. Herstart de VM. Je kunt het klembord delen met de Host via  Devices > Shared Clipboard > Bidirectional.

PlutoSDR verbinden
###################

1. Drivers installeren
 A. Voor MacOS, onder systeem voorkeuren, zet "kernel extensions" aan. Installeer vervolgens HoRNDIS (Misschien moet je herstarten).
 B. Voor Windows kun je deze driver installeren: https://github.com/analogdevicesinc/plutosdr-m2k-drivers-win/releases/download/v0.7/PlutoSDR-M2k-USB-Drivers.exe
 C. Voor Linux zou je niets speciaals te hoeven doen.
2. Plug je Pluto in de host machine via USB. Gebruik de middelste usb poort van de Pluto want de andere is alleen voor voeding. Na het inpluggen van de Pluto wordt een virtuele netwerkkaart aangemaakt, het verschijnt als een USB ethernet adapter.
3. Op de host machine (niet de VM), open jouw favoriete tool en ping 192.168.2.1. Zorg er eerst voor dat dit werkt voordat je verder gaat.
4. Open een nieuwe terminal binnen de VM
5. Ping 192.168.2.1. Als dat niet werk, los dat eerst op. Wanneer je, tijdens het pingen, de Pluto uit de computer haalt zou de ping geen antwoord meer moeten geven. Als het gewoon door blijft gaan dan zit er waarschijnlijk een ander apparaat op hetzelfde ip-adres. Je zult het het adres van de pluto moeten aanpassen.
6. Schrijf het juiste ip adres van de Pluto ergens op, want dit hebben we nodig om later verbinding te maken.

PlutoSDR Driver installeren
###########################

De onderstaande terminal commando's (op de VM) zou de volgende zaken moeten installeren:

1. **libiio**, Analog Device’s “cross-platform” bibliotheek
2. **libad9361-iio**, AD9361 is de specifieke RF chip binnen de PlutoSDR
3. **pyadi-iio**, de Pluto's Python API, *ons einddoel*, maar het is afhankelijk van de eerste twee


.. code-block:: bash

 sudo apt-get install build-essential git libxml2-dev bison flex libcdk5-dev cmake python3-pip libusb-1.0-0-dev libavahi-client-dev libavahi-common-dev libaio-dev
 cd ~
 git clone --branch v0.23 https://github.com/analogdevicesinc/libiio.git
 cd libiio
 mkdir build
 cd build
 cmake -DPYTHON_BINDINGS=ON ..
 make -j$(nproc)
 sudo make install
 sudo ldconfig
 
 cd ~
 git clone https://github.com/analogdevicesinc/libad9361-iio.git
 cd libad9361-iio
 mkdir build
 cd build
 cmake ..
 make -j$(nproc)
 sudo make install
 
 cd ~
 git clone --branch v0.0.14 https://github.com/analogdevicesinc/pyadi-iio.git
 cd pyadi-iio
 pip3 install --upgrade pip
 pip3 install -r requirements.txt
 sudo python3 setup.py install

PlutoSDR Drivers testen
##########################

Open een nieuwe terminal (in jouw VM) en type de volgende commando's:

.. code-block:: bash

 python3
 import adi
 sdr = adi.Pluto('ip:192.168.2.1') # of wat jouw Pluto's IP ook is
 sdr.sample_rate = int(2.5e6)
 sdr.rx()

Als je tot nu toe geen problemen ervaart dan kun je verder met de volgende stappen.

Pluto's IP Adres aanpassen
####################################

Mocht je om een of andere reden het standaard IP van 192.168.2.1 niet willen, dan kun je het IP met deze stappen aanpassen:

1. Bewerk het config.txt bestand op de PlutoSDR schijf (dus het USB-drive achtige ding wat tevoorschijn komt wanneer je de Pluto inplugt. Voer het nieuw IP adres in.
2. Werp de schijf uit maar laat de Pluto in de computer zitten! In Ubuntu 22 is er een naast de PlutoSDR device een uitwerp symbool, binnen de verkenner.
3. Wacht een paar seconden na het uitwerpen en plug daarna de Pluto uit en in de computer. Ga terug naar config.txt en verifieer dat de wijziging is opgeslagen.

Op dezelfde manier zou je de firmware van de Pluto kunnen updaten. Zie voor meer info https://wiki.analog.com/university/tools/pluto/users/firmware.

"Hack" de PlutoSDR voor een groter RF bereik
############################################

De PlutoSDR komt standaard met een beperkte frequentiebereik en bemonsteringsfrequentie, maar de onderliggende chip kan veel hogere frequenties aan. Volg deze stappen om het volle frequentiebereik aan te zeten. Dit proces wordt door Analog Devices zelf uitgelegd dus heeft minimale risico's. De restricties zijn door Analog Devices aangezet omdat de specifieke chips niet voldeden aan de strenge performance-eisen op deze hogere frequenties. Maar als SDR studenten maken we ons niet zo druk over die perfomance-eisen.

Tijd om te hacken! Open een terminal (host of VM):

.. code-block:: bash

 ssh root@192.168.2.1

Het wachtwoord is analog.

Je zou een welkkomst 'scherm' moeten zien. Je hebt nu geSSHt naar de linux-omgeving van de Pluto zelf!
Als je een Pluto firmwareversie van 0.31 of minder hebt, type dan de volgende commando's:

.. code-block:: bash

 fw_setenv attr_name compatible
 fw_setenv attr_val ad9364
 reboot

Voor firmwares van 0.32 en hoger:

.. code-block:: bash
 
 fw_setenv compatible ad9364
 reboot

Nu moet het mogelijk zijn om af te stemmen op frequenties tussen de 70 MHz en 6 GHz, en een sample rat van 56 MHz! Joepie!

************************
Ontvangen
************************

Via de PlutoSDR's Python API is het simpel om monsters te ontvangen. 
Voor elke SDR applicatie wil je weten wat de middenfrequentie, bemonsteringsfrequentie en versterking is, en of je eventueel automatic gain control (AGC) wilt gebruiken.
Er zijn andere details, maar deze drie parameters zijn essentieel voor de SDR om te starten met monsters ontvangen.
Sommige SDR's hebben een commando om te beginnen met het bemonsteren, en anderen zoals de Pluto beginnen zodra je hem initialiseert.
Op het moment dat de interne buffers van de Pluto volzitten, dan zal het de oudste samples gaan verwijderen.
Alle SDR API's hebben een "ontvang monsters" functie, en voor de Pluto is dit rx(), dat een stapel monsters teruggeeft.
De hoeveelheid monsters dat het teruggeeft is gedefinieerd door de buffergrootte wat van tenvoren is ingesteld.

De onderstaande code gaat ervan uit dat je Pluto's Python API hebt geinstalleerd.
Deze code initialiseert de Pluto, stelt de bemonsteringsfrequentie in op 1 MHz, stelt de middenfrequentie in op 100 MHz en stelt de versterking in op 70 dB met AGC uitgeschakeld.
Het maakt meestal niets uit in welke volgorde je deze dingen doet.
In de onderstaande code vragen we de Pluto om 10,000 monsters per rx() functieaanroep.
We drukken de eerste 10 monsters af.

.. code-block:: python

    import numpy as np
    import adi
    
    sample_rate = 1e6 # Hz
    center_freq = 100e6 # Hz
    num_samps = 10000 # number of samples returned per call to rx()
    
    sdr = adi.Pluto()
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.rx_hardwaregain_chan0 = 70.0 # dB
    sdr.rx_lo = int(center_freq)
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
    sdr.rx_buffer_size = num_samps
    
    samples = sdr.rx() # receive samples off Pluto
    print(samples[0:10])

Voor nu doen we niets interessants met deze monsters, maar de rest van dit boek staat vol met Python code dat werkt met IQ-monsters zoals we zojuist hebben ontvangen.

Ontvangstversterking
####################

De Pluto kan worden ingesteld op een vaste versterking of een automatische. Een automatische versterkingscontrole (AGC) zal automatisch de versterking van de ontvanger aanpassen om een sterk signaalniveau te behouden (-12dBFS om exact te zijn).
AGC moet je niet verwarren met een analoog-naar-digitaal converter (ADC) dat het signaal digitaliseerd.
Technisch gezien is de AGC een gesloten-lus feedbackschakeling dat de versterking beheert op basis van het ontvangen signaal met als doel om een constant vermogensniveau te behouden desondanks variërende ingangsvermogens.
Typisch zorgt de AGC ervoor dat het signaal de ADC niet overstuurt maar wel zo goed mogelijk het volledige bereik van de ADC gebruikt.


The radio-frequency integrated circuit, or RFIC, inside the PlutoSDR has an AGC module with a few different settings.  (An RFIC is a chip that functions as a transceiver: it transmits and receives radio waves.)  First, note that the receive gain on the Pluto has a range from 0 to 74.5 dB.  When in "manual" AGC mode, the AGC is turned off, and you must tell the Pluto what receive gain to use, e.g.:

.. code-block:: python

  
  sdr.gain_control_mode_chan0 = "manual" # turn off AGC
  gain = 50.0 # allowable range is 0 to 74.5 dB
  sdr.rx_hardwaregain_chan0 = gain # set receive gain

If you want to enable the AGC, you must choose from one of two modes:

1. :code:`sdr.gain_control_mode_chan0 = "slow_attack"`
2. :code:`sdr.gain_control_mode_chan0 = "fast_attack"`

And with AGC enabled you don't provide a value to :code:`rx_hardwaregain_chan0`. It will get ignored because the Pluto itself adjusts the gain for the signal. The Pluto has two modes for AGC: fast attack and slow attack, as shown in the code snipped above. The difference between the two is intuitive, if you think about it. Fast attack mode reacts quicker to signals.  In other words, the gain value will change faster when the received signal changes level.  Adjusting to signal power levels can be important, especially for time-division duplex (TDD) systems that use the same frequency to transmit and receive. Setting the gain control to fast attack mode for this scenario limits signal attenuation.  With either mode, if there is no signal present and only noise, the AGC will max out the gain setting; when a signal does show up it will saturate the receiver briefly, until the AGC is able to react and ramp down the gain.  You can always check the current gain level in realtime with:

.. code-block:: python
 
 sdr._get_iio_attr('voltage0','hardwaregain', False)

For more details about the Pluto's AGC, such as how to change the advanced AGC settings, refer to `the "RX Gain Control" section of this page <https://wiki.analog.com/resources/tools-software/linux-drivers/iio-transceiver/ad9361>`_.

************************
Transmitting
************************

Before you transmit any signal with your Pluto, make sure to connect a SMA cable between the Pluto's TX port, and whatever device will be acting as the receiver.  It's important to always start by transmitting over a cable, especially while you are learning *how* to transmit, to make sure the SDR is behaving how you intend.  Always keep your transmit power extremely low, as to not overpower the receiver, since the cable does not attenuate the signal like the wireless channel does.  If you own an attenuator (e.g. 30 dB), now would be a good time to use it.  If you do not have another SDR or a spectrum analyzer to act as the receiver, in theory you can use the RX port on the same Pluto, but it can get complicated.  I would recommend picking up a $10 RTL-SDR to act as the receiving SDR.

Transmitting is very similar to receiving, except instead of telling the SDR to receive a certain number of samples, we will give it a certain number of samples to transmit.  Instead of :code:`rx_lo` we will be setting :code:`tx_lo`, to specify what carrier frequency to transmit on.  The sample rate is shared between the RX and TX, so we will be setting it like normal.  A full example of transmitting is shown below, where we generate a sinusoid at +100 kHz, then transmit the complex signal at a carrier frequency of 915 MHz, causing the receiver to see a carrier at 915.1 MHz.  There is really no practical reason to do this, we could have just set the center_freq to 915.1e6 and transmitted an array of 1's, but we wanted to generate complex samples for demonstration purposes. 

.. code-block:: python
    
    import numpy as np
    import adi

    sample_rate = 1e6 # Hz
    center_freq = 915e6 # Hz

    sdr = adi.Pluto("ip:192.168.2.1")
    sdr.sample_rate = int(sample_rate)
    sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = -50 # Increase to increase tx power, valid range is -90 to 0 dB

    N = 10000 # number of samples to transmit at once
    t = np.arange(N)/sample_rate
    samples = 0.5*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
    samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

    # Transmit our batch of samples 100 times, so it should be 1 second worth of samples total, if USB can keep up
    for i in range(100):
        sdr.tx(samples) # transmit the batch of samples once

Here are some notes about this code.  First, you want to simulate your IQ samples so that they are between -1 and 1, but then before transmitting them we have to scale by 2^14 due to how Analog Devices implemented the :code:`tx()` function.  If you are not sure what your min/max values are, simply print them out with :code:`print(np.min(samples), np.max(samples))` or write an if statement to make sure they never go above 1 or below -1 (assuming that code comes before the 2^14 scaling).  As far as transmit gain, the range is -90 to 0 dB, so 0 dB is the highest transmit power.  We always want to start at a low transmit power, and then work our way up if needed, so we have the gain set to -50 dB by default which is towards the low end.  Don't simply set it to 0 dB just because your signal is not showing up; there might be something else wrong, and you don't want to fry your receiver. 

Transmitting Samples on Repeat
##############################

If you want to continuously transmit the same set of samples on repeat, instead of using a for/while loop within Python like we did above, you can tell the Pluto to do so using just one line:

.. code-block:: python

 sdr.tx_cyclic_buffer = True # Enable cyclic buffers

You would then transmit your samples like normal: :code:`sdr.tx(samples)` just one time, and the Pluto will keep transmitting the signal indefinitely, until the sdr object destructor is called.  To change the samples that are being continuously transmitted, you cannot simply call :code:`sdr.tx(samples)` again with a new set of samples, you have to first call :code:`sdr.tx_destroy_buffer()`, then call :code:`sdr.tx(samples)`.

Transmitting Over the Air Legally
#################################

Countless times I have been asked by students what frequencies they are allowed to transmit on with an antenna (in the United States).  The short answer is none, as far as I am aware.  Usually when people point to specific regulations that talk about transmit power limits, they are referring to `the FCC's "Title 47, Part 15" (47 CFR 15) regulations <https://www.ecfr.gov/cgi-bin/text-idx?SID=7ce538354be86061c7705af3a5e17f26&mc=true&node=pt47.1.15&rgn=div5>`_.  But those are regulations for manufacturers building and selling devices that operate in the ISM bands, and the regulations discuss how they should be tested.  A Part 15 device is one where an individual does not need a license to operate the device in whatever spectrum it's using, but the device itself must be authorized/certified to show they are operating following FCC regulations before they are marketed and sold.  The Part 15 regulations do specify maximum transmit and received power levels for the different pieces of spectrum, but none of it actually applies to a person transmitting a signal with an SDR or their home-built radio.  The only regulations I could find related to radios that aren't actually products being sold were specific to operating a low-power AM or FM radio station in the AM/FM bands.  There is also a section on "home-built devices", but it specifically says it doesn't apply to anything constructed from a kit, and it would be a stretch to say a transmit rig using an SDR is a home-built device.  In summary, the FCC regulations aren't as simple as "you can transmit at these frequencies only below these power levels", but rather they are a huge set of rules meant for testing and compliance.

Another way to look at it would be to say "well, these aren't Part 15 devices, but let's follow the Part 15 rules as if they were".  For the 915 MHz ISM band, the rules are that "The field strength of any emissions radiated within the specified frequency band shall not exceed 500 microvolts/meter at 30 meters. The emission limit in this paragraph is based on measurement instrumentation employing an average detector."  So as you can see, it's not as simple as a maximum transmit power in watts.

Now, if you have your amateur radio (ham) license, the FCC allows you to use certain bands set aside for amateur radio.  There are still guidelines to follow and maximum transmit powers, but at least these numbers are specified in watts of 
effective radiated power.  `This info-graphic <http://www.arrl.org/files/file/Regulatory/Band%20Chart/Band%20Chart%20-%2011X17%20Color.pdf>`_ shows which bands are available to use depending on your license class (Technician, General and Extra).  I would recommend anyone interested in transmitting with SDRs to get their ham radio license, see `ARRL's Getting Licensed page <http://www.arrl.org/getting-licensed>`_ for more info. 

If anyone has more details about what is allowed and not allowed, please email me.

************************************************
Transmitting and Receiving Simultaneously
************************************************

Using the tx_cyclic_buffer trick you can easily receive and transmit at the same time, by kicking off the transmitter, then receiving. 
The following code shows a working example of transmitting a QPSK signal in the 915 MHz band, receiving it, and plotting the PSD.

.. code-block:: python

    import numpy as np
    import adi
    import matplotlib.pyplot as plt

    sample_rate = 1e6 # Hz
    center_freq = 915e6 # Hz
    num_samps = 100000 # number of samples per call to rx()

    sdr = adi.Pluto("ip:192.168.2.1")
    sdr.sample_rate = int(sample_rate)

    # Config Tx
    sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = -50 # Increase to increase tx power, valid range is -90 to 0 dB

    # Config Rx
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samps
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.rx_hardwaregain_chan0 = 0.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

    # Create transmit waveform (QPSK, 16 samples per symbol)
    num_symbols = 1000
    x_int = np.random.randint(0, 4, num_symbols) # 0 to 3
    x_degrees = x_int*360/4.0 + 45 # 45, 135, 225, 315 degrees
    x_radians = x_degrees*np.pi/180.0 # sin() and cos() takes in radians
    x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) # this produces our QPSK complex symbols
    samples = np.repeat(x_symbols, 16) # 16 samples per symbol (rectangular pulses)
    samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

    # Start the transmitter
    sdr.tx_cyclic_buffer = True # Enable cyclic buffers
    sdr.tx(samples) # start transmitting

    # Clear buffer just to be safe
    for i in range (0, 10):
        raw_data = sdr.rx()
        
    # Receive samples
    rx_samples = sdr.rx()
    print(rx_samples)

    # Stop transmitting
    sdr.tx_destroy_buffer()

    # Calculate power spectral density (frequency domain version of signal)
    psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
    psd_dB = 10*np.log10(psd)
    f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

    # Plot time domain
    plt.figure(0)
    plt.plot(np.real(rx_samples[::100]))
    plt.plot(np.imag(rx_samples[::100]))
    plt.xlabel("Time")

    # Plot freq domain
    plt.figure(1)
    plt.plot(f/1e6, psd_dB)
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("PSD")
    plt.show()


You should see something that looks like this, assuming you have proper antennas or a cable connected:

.. image:: ../_images/pluto_tx_rx.svg
   :align: center 

It is a good exercise to slowly adjust :code:`sdr.tx_hardwaregain_chan0` and :code:`sdr.rx_hardwaregain_chan0` to make sure the received signal is getting weaker/stronger as expected.

************************
Reference API
************************

For the entire list of sdr properties and functions you can call, refer to the `pyadi-iio Pluto Python code (AD936X) <https://github.com/analogdevicesinc/pyadi-iio/blob/master/adi/ad936x.py>`_.

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




