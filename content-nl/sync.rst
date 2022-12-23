.. _sync-chapter:

################
Synchronisatie
################

Dit hoofdstuk gaat over het synchroniseren van draadloze signalen in tijd en frequentie. Hiermee corrigeren we frequentieafwijking en stellen het moment van samplen af op symbool niveau. We zullen de klokhersteltechniek van Mueller en Muller en de Costas Loop gebruiken in Python.

***************************
Introduction
***************************

We hebben besproken hoe je digitale signalen draadloos kunt versturen met een digitaal modulatieschema zoals QPSK en het toepassen van vormgevende filters om de bandbreedte te beperken. We kunnen kanaalcodering toepassen bij slechte signaalruisverhoudingen. 
Het zal sowieso helpen om zoveel mogelijk te filteren voordat we het signaal verwerken.
In dit hoofdstuk zullen we onderzoeken hoe synchronisatie wordt uitgevoerd aan de ontvangende kant. 
Synchronisatie is een reeks bewerkingen die plaatsvindt *vóór* demodulatie en kanaaldecodering.
Hieronder zie je de totale zender-kanaal-ontvanger keten waarbij de blokken die we in dit hoofdstuk zullen behandelen, geel zijn gemaakt. (Dit diagram is niet allesomvattend - de meeste systemen bevatten ook egalisatie en multiplexing).

.. image:: ../_images/sync-diagram.svg
   :align: center 
   :target: ../_images/sync-diagram.svg

***************************
Draadloos kanaal simuleren
***************************

We zullen een realistischer kanaalmodel moeten gaan gebruiken voordat we het over synchronisatie gaan hebben. Zolang er geen willekeurige vertraging plaatsvindt is er namelijk geen synchronisatie nodig, of tenminste is het erg simpel om te synchroniseren (met de sampleklok). Je zou in dat geval alleen maar rekening hoeven houden met de vertraging die jouw filters introduceren. Naast een tijdsvertraging zullen we ook een frequentieafwijking simuleren; oscillators zijn immers niet perfect, er zal altijd een verschil zijn tussen de middenfrequentie van de zender en ontvanger.

We zullen eerst wat Python code gaan bekijken waarmee we een vertraging en frequentieafwijking kunnen simuleren. De code zal verder gaan waar het :ref:`pulse-shaping-chapter` is geeindigt; alle code uit dit hoofdstuk kun je erachter toevoegen. Voor het gemak is de code hier ook te vinden:

.. raw:: html

   <details>
   <summary>Python Code van het vorige hoofdstuk</summary>

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    import math

    # symbolen genereren
    num_symbols = 100
    sps = 8
    bits = np.random.randint(0, 2, num_symbols) # De te verzenden bits
    pulse_train = np.array([])
    for bit in bits:
        pulse = np.zeros(sps)
        pulse[0] = bit*2-1 # alleen eerste waarde gelijk aan bitwaarde
        pulse_train = np.concatenate((pulse_train, pulse)) # de 8 samples toevoegen aan x

    # het RC filter bouwen
    num_taps = 101
    beta = 0.35
    Ts = sps # sample rate is 1 Hz, periodetijd is 1, *symbool*periodetijd is 8
    t = np.arange(-51, 52) # neemt laatste nummer niet mee
    h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)

    # signaal x filteren.
    samples = np.convolve(pulse_train, h)

.. raw:: html

   </details>

De code die te maken heeft met het weergeven van de figuren hebben we weg gelaten, we gaan ervan uit dat je nu hebt geleerd hoe je dat moet doen.
Om de figuren extra mooi te maken zoals in dit boek heb je veel extra code nodig, wat niet het leerdoel is.


Vetraging toevoegen
###################

We zouden makkelijk het signaal kunnen vertragen door de samples te verschuiven, maar dit simuleert alleen een vertraging dat een veelvoud is van onze sampletijd. Realistisch gezien zal de vertraging nooit exact gelijk zijn aan de sampletijd. We kunnen een willekeurige vertraging geven met een speciaal filter dat alle frequenties doorlaat maar de samples wel vertraagt met een fractie van de sampletijd. Je kunt het zien als een alles-doorlaatfiler dat een faseverschuiving introduceert op alle frequenties. (Een tijdsvertraging en faseverschuiving zijn immers hetzelfde!) De Python code van dit filter staat hieronder:

.. code-block:: python

    # filter maken en toepassen
    delay = 0.4 # fractie van de sampletijd
    N = 21 # aantal coefficienten
    n = np.arange(-N//2, N//2) # ...-3,-2,-1,0,1,2,3...
    h = np.sinc(n - delay) # coefficienten berekenen
    h *= np.hamming(N) # venster toepassen om beide kanten naar 0 te latten gaan
    h /= np.sum(h) # normaliseren zodat de versterking 1 is en we het signaal niet dempen
    samples = np.convolve(samples, h) # filter toepassen.

Zoals je ziet berekenen we de filtercoefficienten met behulp van de sinc() functie. Een sinc in het tijddomein is een rechthoek in het frequentiedomein en de rechthoek voor dit filter reikt over het hele frequentiebereik van ons signaal. Er is geen vervoming, alleen een vertraging. In dit voorbeeld is dat :math:`0.4*T_s`. Hou in je achterhoofd dat *elk* filter een vertraging toevoegt gelijk aan het aantal coefficienten/2 -1 vanwege de convolutieoperatie.

De vertraging is te zien wanneer we de in en uitgang van het filter weergeven. Als je alleen een paar symbolen bekijkt is het goed zichtbaar.

.. image:: ../_images/fractional-delay-filter.svg
   :align: center
   :target: ../_images/fractional-delay-filter.svg



Frequentieafwijking introduceren
################################

Om het ontvangen signaal nog realistcher te maken kunnen we een frequentieafwijking toepassen. Stel we hebben een samplerate van 1 MHz gebruikt (dit is niet belangrijk maar maakt het vervolg wat makkelijker). Mochten we een frequentieverschuiving van 13 kHz (willekeurig gekozen) willen toepassen dan kan dat met deze code:

.. code-block:: python

   # freq afwijking
   fs = 1e6 # samplerate van 1 MHz
   fo = 13000 # offset 13 khz
   Ts = 1/fs # sampletijd
   t = np.arange(0, Ts*len(samples), Ts) # tijdvector
   samples = samples * np.exp(1j*2*np.pi*fo*t) # verschuiving
 
Dit figuur laat het signaal voor en na de frequentieverschuiving zien.
 
.. image:: ../_images/sync-freq-offset.svg
   :align: center
   :target: ../_images/sync-freq-offset.svg

Tot nu toe konden we alleen het reele I-deel weergeve omdat we BPSK gebruiken. Maar nu we een frequentieverschuiving hebben geintroduceerd om een draadloos kanaal te simuleren verspreidt de energie zich over het I en Q deel. Dus vanaf nu moeten we beide delen weergeven. Voel je vrij een andere frequentieverschuiving te kiezen. Bij een verschuiving van 1 kHz zul je ook een sinusoide kunnen herkennen in de omlijning van het signaal; het varieert dan langzaam genoeg om een paar symbolen te overspannen.

Als je de code bestudeert zul je zien dat de samplerate niet helemaal arbitrair is, het is afhankelijk van het ratio tussen :code:`fo` en :code:`fs`.

Voor nu kun je de code beschouwen als de simulatie van een draadloos kanaal. De code komt na de zender maar voor de ontvanger. De kan van de ontvanger gaan we verder bestuderen in dit hoofdstuk.

***************************
Tijdsynchronisatie
***************************

Wanneer een signaal draadloos wordt verzonden ervaart het een willekeurige faseverschuiving vanwege de reistijd. We kunnen niet zomaar beginnen te samplen op onze samplefrequentie want dan zitten we hoogstwaarschijnlijk naast het juiste samplemoment zoals aan het eind van :ref:`pulse-shaping-chapter` is besproken. Bekijk de laatste drie figuren van dat hoofdstuk eens als je dit niet kunt volgen. Het doel is dus om origenele samplefrequentie en fase terug te vinden. Het wordt ook "clock-recovery" (herstellen van de klok) genoemd.

De meeste synchronisatietechnieken zijn gebaseerd op de phase locked loop (PLL); we zullen PLLs hier niet bespreken maar het is goed om te weten en je kunt er zelf informatie over opzoeken als je geinteresseerd bent. PLL's zijn closed-loop systemen die feedback gebruiken om voortdurend wat bij te stellen; in dit geval een tijdsvertraging om op de pieken te kunnen samplen.

Je kunt de synchronisatie zien als een blok welk een stroom aan samples ontvangt en uitstuurt, net als een filter. Dit blok wordt ingesteld met informatie over ons signaal, met name het aantal samples per symbool (onze beste inschatting). Het blok werkt als een decimator, de samplefrequnetie aan de uitgang is lager dan aan de ingang. We willen maar 1 sample per symbool hebben dus de factor is gelijk aan het aantal samples per symbool.
Als we 1M symbolen per seconde zenden, en het signaal bij de ontvanger samplen met 16 MHz, dan krijgen we 16 samples per symbool.
De ingangsfrequentie van het blok is dan 16 MHz maar de uitgang 1 MHz, gezien we maar 1 sample per symbool willen.

De meeste algoritmes leunen op het feit dat digitale symbolen stijgen en dalen en de overgang is het moment waarop we willen samplen. Anders verwoord, als we de absolute versie van ons signaal nemen dan willen we op de pieken samplen:

.. image:: ../_images/symbol_sync2.png
   :scale: 40 % 
   :align: center 

De meeste algoritmen zijn op een PLL gebaseerd en het verschil tussen ze is de vergelijking die de afwijking in de tijd (:math:`\mu`) probeert te corrigeren. De waarde van :code:`mu` wordt in elke iteratie van de loop geüpdatet. Je kunt het bekijken als de waarde die verteld hoeveel samples we het signaal moeten verschuiven om het "perfecte" samplemoment te vinden. Dus met een waard van :code:`mu = 3.61` zouden we de ingang 3.61 samples moeten verschuiven om correct te kunen samplen. Omdat we 8 samples per symbool hebben zou een :code:`mu>8` gewoon weer terugvouwen naar 0.

Het volgende stuk code implementeert het Mueller en Muller klokherstel algoritme. Je kunt het testen zolang je de frequentieverschuiving 0 laat; dit corrigeert alleen een faseverschuiving:

.. code-block:: python

    mu = 0 # Eerste inschatting
    out = np.zeros(len(samples) + 10, dtype=complex)
    out_rail = np.zeros(len(samples) + 10, dtype=complex) # stores values, each iteration we need the previous 2 values plus current value
    i_in = 0 # input samples index
    i_out = 2 # output index (eerste twee zijn 0)
    while i_out < len(samples) and i_in+16 < len(samples):
        out[i_out] = samples[i_in + int(mu)] # probeer het "beste" sample.
        out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0) #90,45,-45 of -90
        x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
        y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
        mm_val = np.real(y - x)
        mu += sps + 0.3*mm_val
        i_in += int(np.floor(mu)) # het is een index dus afronden
        mu = mu - np.floor(mu) # getal achter de punt bepalen
        i_out += 1 # index uitgang ophogen
    out = out[2:i_out] # eerste 2 verwijderen, alles na i_out is niet gebruikt
    samples = out # samples zijn de uitgang

Het blok wordt de "ontvangen" samples gevoerd en geeft aan de uitgang 1 sample per keer (:code:`i_out` wordt telkens opgehoogd).
Het gebruikt niet alle ontvangen samples achter elkaar, maar slaat samples over in een poging sneller het juiste sample te vinden, op de piek van de puls.
Tijdens de herhaling probeert het langzaam met het symbool te synchroniseren door :code:`mu` aan te passen.
Als de synchronisatie volledig is zou de uitgang alleen samples moeten bevatten die op de juiste momenten zijn genomen.
De snelheid waarmee de lus reageert wordt bepaald door de 0.3 constante; een hogere waarde reageert heftiger of sneller, maar kan het systeem instabiel maken.

De volgende grafiek toont een voorbeelduitvoer waarbij we zowel de fractionele tijdvertraging als de frequentieverschuiving *uitgeschakeld* hebben. We tonen alleen I omdat Q nu uit nullen bestaat vanwege het gebrek aan frequentieverschuiving. De drie plots zijn op elkaar gestapeld om te laten zien hoe de bits verticaal zijn uitgelijnd.

**Top Plot**
    De originele BPSK symbolen, i.e., 1'en end -1'en.  Er zitten nullen tussen vanwege de 8 samples per symbool.
**Middle Plot**
    Na het vormgeven van de pulsen.
**Bottom plot**
    Na het uitvoeren van de Tijdsynchronisatie blijft er 1 sample per symbool over. Deze samples worden direct in de demodulator gestopt wat voor BPSK een vergelijking met 0 betekent.

.. image:: ../_images/time-sync-output.svg
   :align: center
   :target: ../_images/time-sync-output.svg

Als we kijken naar de uitgang van het synchronisatieblok in het onderste figuur, dan zien we dat het bijna 30 symbolen duurde voordat de juiste tijdvertraging was gevonden. Omdat een feedback-systeem altijd tijd nodig heeft om te reageren maken vele communicatieprotocolen gebruik van een "preamble" (Nederlands: reeks aan bits die het signaal voorgaan). Deze preamble bevat een synchronisatiesequentie: het verkondigt dat een nieuw pakketje is aangekomen, en geeft de ontvanger de tijd om te synchroniseren. Maar na ~30 symbolen werkt het perfect (in het figuur). Wat we over houden zijn perfecte 1'en en -1'en die overeenkomen met de verzonden data. Natuurlijk helpt het dat dit voorbeeld geen ruis had. Voel je vrij het ruisniveau en de tijdsvertraging aan te passen om te kijken hoe de synchronisatie werkt. In geval van QPSK zouden we met complexe getallen werken, maar de aanpak blijft hetzelfde.

****************************************
Tijdsynchronisatie met interpolatie
****************************************

Meestal interpoleren synchronisatieblokken de ingangssamples door een bepaald nummer, bijv. 16, zodanig dat het signaal ook een fractie van de sampletijd verschoven kan worden. De willekeurige vertraging dat een draadloos kanaal introduceert, is hoogstwaarschijnlijk niet perfect gelijk aan een veelvoud van de sampletijd. Dit zal helemaal niet het geval zijn wanneer we 2 of 4 samples per symbool ontvangen. Door de samples te interpoleren geeft het ons de mogelijkheid om "tussen" de samples te samplen om de uiterste piek van het symbool te vinden. De uitgang zal nog steeds 1 sample per symbool bevatten, het is de ingang dat geïnterpoleerd wordt.

De Python code voor tijdsynchronisatie dat we hierboven gebruikten bevat geen interpolatie. Om de code uit te breiden kun je de fractionele tijdvertraging aanzetten dat we aan het begin van dit hoofdstuk hebben geimplementeerd, dit geeft een realistischer beeld. Laat de frequentieverschuiving uit staan. Wanneer je de simulatie opnieuw uitrvoert zul je zien dat er nooit volledig gesynchroniseerd wordt met het signaal. Dit komt omdat we niet interpoleren en het dus niet mogelijk is om tussen de samples in te samplen. Laten we interpolatie toevoegen.

De snelste en makkelijkste manier om met Python een signaal te interpoleren is door gebruik te maken van scipy's :code:`signal.resample` of :code:`signal.resample_poly`. Beide functies bereiken hetzelfde, maar werken iets anders. We zullen de tweede functie toepassen omdat deze wat sneller is. We gaan een interpolatiefactor van 16 gebruiken, dus we voegen 15 extra samples tussen elke sample toe. Dit kan worden toegepast in 1 regel code en moet *voor* de tijdsynchronisatie worden toegevoegd. Het synchronisatie-algoritme moet ook iets aangepast worden. We kunnen het verschil bekijken:

.. code-block:: python

 samples_interpolated = signal.resample_poly(samples, 16, 1)
 
 # Plot the old vs new
 plt.figure('before interp')
 plt.plot(samples,'.-')
 plt.figure('after interp')
 plt.plot(samples_interpolated,'.-')
 plt.show()

Als we het *heel erg* vergroten dan zien we dat het hetzelfde signaal is, maar met 16x zoveel punten:

.. image:: ../_images/time-sync-interpolated-samples.svg
   :align: center
   :target: ../_images/time-sync-interpolated-samples.svg

Hopelijk is de reden achter het interpoleren duidelijk aan het worden. De extra samples staan ons toe om ook een fractie van de sampletijd te kunnen zien. Naar het interpoleren van de samples zullen we ook twee regels van het synchronisatieblok moeten aanpassen. De eerste twee regels van de while loop worden dan:

.. code-block:: python

 while i_out < len(samples) and i_in*16+16 < len(samples):
   out[i_out] = samples[i_in*16 + int(mu*16)] # probeer het "beste" sample.

We hebben een aantal dingen aangepast. Als eerste kunnen we :code:`i_in` niet meer gebruiken als de sampleindex. We hebben nu 16 keer zoveel samples dus we moeten de index met 16 vermenigvuldigen. De loop past :code:`mu` aan. Dit stelt de vertraging voor dat we nodig hebben om correct te samplen. 
Eerder kon we niet een fractie van de sampletijd wachten, maar nu wel, in stappen van een 16e van de sampletijd. 
We vermenigvuldigen :code:`\mu` dus met 16 om uit te vogelen met hoeveel samples we ons geinterpoleerde signaal moeten vertragen.
Als deze paragraaf niet duidelijk is, probeer dan de initiele code met het commentaar nogmaals door te lezen.
Het is niet heel belangrijk dat je het algoritme snapt, maar wel de limitaties ervan.

Voel je vrij om met eigen interpolatiefactoren te spelen. Je kunt ook proberen om de frequentieverschuiving nu toe te passen, of ruis toe te voegen, om te zien hoe het synchronisatiealgoritme dit aanpakt (hint: misschien moet je die 0.3 factor ook aanpassen).

Als de een frequentieverschuiving toepassen van 1 kHz dan zie je de volgende reactie. We zullen beide I en Q moeten weergeven omdat een frequentieverschuiving toe hebben gevoegd (door een complex exponent):

.. image:: ../_images/time-sync-output2.svg
   :align: center
   :target: ../_images/time-sync-output2.svg

Het is nu iets lastiger te zien maar de tijdsynchronisatie werkt nog steeds prima. Er is nu een sinusoide zichtbaar omdat we een frequentieverschuiving hebben geintroduceerd. In het volgende deel leren we hier mee om te gaan.

Het IQ-diagram (constellatie-diagram) is hieronder te zien van voor en na synchronisatie. Mocht je het zijn vergeten; je kunt een IQ-diagram maken d.m.v. een "scatter plot": :code:`plt.plot(np.real(samples), np.imag(samples), '.')`. In de animatie hebben we bewust de eerste en laatste 30 symbolen niet meegenomen omdat het algoritme toen nog niet klaar was met synchroniseren. De symbolen die overblijven zijn allemaal rond de eenheidscirkel verdeelt vanwege de frequentieverschuiving.

.. image:: ../_images/time-sync-constellation.svg
   :align: center
   :target: ../_images/time-sync-constellation.svg
    

We kunnen nog meer leren wanneer we de constellatie over de tijd uitzetten. Aan het begin zie zijn de symbolen eventjes niet 0 of op de eenheidscirkel. Dat is de tijd die het synchronisatiealgoritme nodig heeft om de juiste tijdsvertraging te vinden. Het gebeurt in een korte tijd dus kijk goed! Het ronddraaien komt door de frequentieverschuiving. Frequentie is een constante verandering in de fase, dus een frequentieverschuiving resulteert in het ronddraaien van het BPSK-diagram, wat leid tot een cirkel in het statische diagram van hierboven.

.. image:: ../_images/time-sync-constellation-animated.gif
   :align: center 

Hopelijk heb je dankzij de animatie een beter beeld van wat er echt gebeurt , en een gevoel voor hoe het werkt. In de praktijk werkt de while loop alleen op een beperkt aantal samples (bijv. 1000) en zul je het herhaaldelijk moeten aanroepen. Tussen de aanroepen in moet je de waarde van :code:`mu` , en de laatste paar waarden van :code:`out` en :code:`out_rail` , moeten onthouden.

Nu gaan we ons druk maken over frequentiesynchronisatie, opgedeelt in grove en fijne synchronisatie. Meestal doen we eerst de grove en daarna de fijne.

**********************************
Grove Frequentiesynchronisatie
**********************************

Ook al stellen we de zender en ontvanger in op dezelfde frequentie, er zal altijd een klein frequentieverschil zijn vanwege imperfecte hardware (de oscillator) of het Doppler-effect vanwege beweging. Het frequentieverschil zal minimaal zijn vergeleken met de draaggolf, maar zelfs een klein verschil kan een digitaal signaal verpesten. De oscillator binnen de Pluto heeft bijvoorbeeld een nauwkeurigheid van 25 PPM. Dus als je op 2.4 GHz afstelt, dan zou dat er maximaal +/- 60 kHz naast kunnen zitten. De samples die we van de SDR krijgen zitten in de basisband, we zien dan het frequentieverschil ook in de basisband. Een BPSK signaal met een klein verschil in draaggolf ziet er ongeveer als het onderstaande figuur uit, wat duidelijk niet zo handig is voor de demodulatie. We zullen dus elke frequentieverschuiving moeten verwijderen voordat we demoduleren.

.. image:: ../_images/carrier-offset.png
   :scale: 60 % 
   :align: center 

Frequentiesynchronisatie wordt meestal opgedeeld in de grove en fijne sync, waar de grove synchronisatie grote verschillen, van een kHz of meer, kan corrigeren, en de fijne sync corrigeert het overgebleven verschil. Grove correctie gebeurt voor tijdsynchronisatie en fijne correctie erna.

Wiskundig gezien, als een basisband signaal :math:`s(t)` een frequentie(draaggolf)verschuiving ervaar van :math:`f_o` Hz, dan is het ontvangen signaal :math:`r(t)` uit te drukken als:

.. math::

 r(t) = s(t) e^{j2\pi f_o t} + n(t)

Waar :math:`n(t)` de ruis is.

De eerste truc voor grove instchatting van de frequentieafwijking, is om het kwadraat van ons signaal te nemen. Wanneer we de afwijking weten, dan kunnen we het ongedaan maken. We negeren de ruis voor nu om het simpel te houden:

.. math::

 r^2(t) = s^2(t) e^{j4\pi f_o t}

Wat zou er gebeuren wanneer we het kwadraat nemen van een QPSK signaal? Kwadrateren van complexe getallen geeft een interessant resultaat, met name wanneer we de constellatiediagrammen van BPSK en QPSK bekijken. De volgende animatie laat zien wat er gebeurt wanneer we QPSK twee maal kwadrateren. Er is bewust voor QPSK gekozen zodat je ziet dat eenmaal kwadrateren een BPSK signaal geeft. Als je het nog een keer kwadrateert zie je een cluster. (Dank aan Ventrella voor deze gave app http://ventrella.com/ComplexSquaring/ .)

.. image:: ../_images/squaring-qpsk.gif
   :scale: 80 % 
   :align: center 

En nog een keer met een kleine fasedraaing en amplitudeverschillen toegepast om het realistischer te maken:
 
.. image:: ../_images/squaring-qpsk2.gif
   :scale: 80 % 
   :align: center 

It still becomes one cluster, just with a phase shift.  The main take-away here is that if you square QPSK twice (and BPSK once), it will merge all four clusters of points into one cluster.  Why is that useful?  Well by merging the clusters we are essentially removing the modulation!  If all points are now in the same cluster, that's like having a bunch of constants in a row.  It's as if there is no modulation anymore, and the only thing left is the sinusoid caused by the frequency offset (we also have noise but let's keep ignoring it for now).  It turns out that you have to square the signal N times, where N is the order of the modulation scheme used, which means that this trick only works if you know the modulation scheme ahead of time.  The equation is really:

.. math::

 r^N(t) = s^N(t) e^{j2N\pi f_o t}

For our case of BPSK we have an order 2 modulation scheme, so we will use the following equation for our coarse frequency sync:

.. math::

 r^2(t) = s^2(t) e^{j4\pi f_o t}

We discovered what happens to the :math:`s(t)` portion of the equation, but what about the sinusoid part (a.k.a. complex exponential)?  As we can see, it is adding the :math:`N` term, which makes it equivalent to a sinusoid at a frequency of :math:`Nf_o` instead of just :math:`f_o`.  A simple method for figuring out :math:`f_o` is to take the FFT of the signal after we square it N times and seeing where the spike occurs.  Let's simulate it in Python.  We will return to generating our BPSK signal, and instead of applying a fractional-delay to it, we will apply a frequency offset by multiplying the signal by :math:`e^{j2\pi f_o t}` just like we did in chapter :ref:`filters-chapter` to convert a low-pass filter to a high-pass filter.

Using the code from the beginning of this chapter, apply a +13 kHz frequency offset to your digital signal.  It could happen right before or right after the fractional-delay is added; it doesn't matter which. Regardless, it must happen *after* pulse shaping but before we do any receive-side functions such as time sync.

Now that we have a signal with a 13 kHz frequency offset, let's plot the FFT before and after doing the squaring, to see what happens.  By now you should know how to do an FFT, including the abs() and fftshift() operation.  For this exercise it doesn't matter whether or not you take the log or whether you square it after taking the abs().

First look at the signal before squaring (just a normal FFT):

.. code-block:: python

    psd = np.fft.fftshift(np.abs(np.fft.fft(samples)))
    f = np.linspace(-fs/2.0, fs/2.0, len(psd))
    plt.plot(f, psd)
    plt.show()

.. image:: ../_images/coarse-freq-sync-before.svg
   :align: center
   :target: ../_images/coarse-freq-sync-before.svg
   
We don't actually see any peak associated with the carrier offset.  It's covered up by our signal.

Now with the squaring added (just a power of 2 because it's BPSK):

.. code-block:: python

    # Add this before the FFT line
    samples = samples**2

We have to zoom way in to see which frequency the spike is on:

.. image:: ../_images/coarse-freq-sync.svg
   :align: center
   :target: ../_images/coarse-freq-sync.svg

You can try increasing the number of symbols simulated (e.g., 1000 symbols) so that we have enough samples to work with.  The more samples that go into our FFT, the more accurate our estimation of the frequency offset will be.  Just as a reminder, the code above should come *before* the timing synchronizer.

The offset frequency spike shows up at :math:`Nf_o`.  We need to divide this bin (26.6 kHz) by 2 to find our final answer, which is very close to the 13 kHz frequency offset we applied at the beginning of the chapter!  If you had played with that number and it's no longer 13 kHz, that's fine.  Just make sure you are aware of what you set it to.

Because our sample rate is 1 MHz, the maximum frequencies we can see are -500 kHz to 500 kHz.  If we take our signal to the power of N, that means we can only "see" frequency offsets up to :math:`500e3/N`, or in the case of BPSK +/- 250 kHz.  If we were receiving a QPSK signal then it would only be +/- 125 kHz, and carrier offset higher or lower than that would be out of our range using this technique.  To give you a feel for Doppler shift, if you were transmitting in the 2.4 GHz band and either the transmitter or receiver was traveling at 60 mph (it's the relative speed that matters), it would cause a frequency shift of 214 Hz.  The offset due to a low quality oscillator will probably be the main culprit in this situation.

Actually correcting this frequency offset is done exactly how we simulated the offset in the first place: multiplying by a complex exponential, except with a negative sign since we want to remove the offset.

.. code-block:: python

    max_freq = f[np.argmax(psd)]
    Ts = 1/fs # calc sample period
    t = np.arange(0, Ts*len(samples), Ts) # create time vector
    samples = samples * np.exp(-1j*2*np.pi*max_freq*t/2.0)

It's up to you if you want to correct it or change the initial frequency offset we applied at the start to a smaller number (like 500 Hz) to test out the fine frequency sync we will now learn how to do.

**********************************
Fine Frequency Synchronization
**********************************

Next we will switch gears to fine frequency sync.  The previous trick is more for coarse sink, and it's not a closed-loop (feedback type) operation.  But for fine frequency sync we will want a feedback loop that we stream samples through, which once again will be a form of PLL.  Our goal is to get the frequency offset to zero and maintain it there, even if the offset changes over time.  We have to continuously track the offset.  Fine frequency sync techniques work best with a signal that already has been synchronized in time at the symbol level, so the code we discuss in this section will come *after* timing sync.

We will use a technique called a Costas Loop.  It is a form of PLL that is specifically designed for carrier frequency offset correction for digital signals like BPSK and QPSK.  It was invented by John P. Costas at General Electric in the 1950's, and it had a major impact on modern digital communications.  The Costas Loop will remove the frequency offset while also fixing any phase offset.  The energy is aligned with the I axis.  Frequency is just a change in phase so they can be tracked as one.  The Costas Loop is summarized using the following diagram (note that 1/2s have been left out of the equations because they don't functionally matter).

.. image:: ../_images/costas-loop.svg
   :align: center 
   :target: ../_images/costas-loop.svg

The voltage controlled oscillator (VCO) is simply a sin/cos wave generator that uses a frequency based on the input.  In our case, since we are simulating a wireless channel, it isn't a voltage, but rather a level represented by a variable.  It determines the frequency and phase of the generated sine and cosine waves.  What it's doing is multiplying the received signal by an internally-generated sinusoid, in an attempt to undo the frequency and phase offset.  This behavior is similar to how an SDR downconverts and creates the I and Q branches.


Below is the Python code that is our Costas Loop:

.. code-block:: python

    N = len(samples)
    phase = 0
    freq = 0
    # These next two params is what to adjust, to make the feedback loop faster or slower (which impacts stability)
    alpha = 0.132
    beta = 0.00932
    out = np.zeros(N, dtype=np.complex)
    freq_log = []
    for i in range(N):
        out[i] = samples[i] * np.exp(-1j*phase) # adjust the input sample by the inverse of the estimated phase offset
        error = np.real(out[i]) * np.imag(out[i]) # This is the error formula for 2nd order Costas Loop (e.g. for BPSK)
        
        # Advance the loop (recalc phase and freq offset)
        freq += (beta * error)
        freq_log.append(freq * fs / (2*np.pi)) # convert from angular velocity to Hz for logging
        phase += freq + (alpha * error)
        
        # Optional: Adjust phase so its always between 0 and 2pi, recall that phase wraps around every 2pi
        while phase >= 2*np.pi:
            phase -= 2*np.pi
        while phase < 0:
            phase += 2*np.pi

    # Plot freq over time to see how long it takes to hit the right offset
    plt.plot(freq_log,'.-')
    plt.show()

There is a lot here so let's step through it.  Some lines are simple and others are super complicated.  :code:`samples` is our input, and :code:`out` is the output samples.  :code:`phase` and :code:`frequency` are like the :code:`mu` from the time sync code.  They contain the current offset estimates, and each loop iteration we create the output samples by multiplying the input samples by :code:`np.exp(-1j*phase)`.  The :code:`error` variable holds the "error" metric, and for a 2nd order Costas Loop it's a very simple equation.  We multiply the real part of the sample (I) by the imaginary part (Q), and because Q should be equal to zero for BPSK, the error function is minimized when there is no phase or frequency offset that causes energy to shift from I to Q.  For a 4th order Costas Loop, it's still relatively simple but not quite one line, as both I and Q will have energy even when there is no phase or frequency offset, for QPSK.  If you are curious what it looks like click below, but we won't be using it in our code for now.  The reason this works for QPSK is because when you take the absolute value of I and Q, you will get +1+1j, and if there is no phase or frequency offset then the difference between the absolute value of I and Q should be close to zero.

.. raw:: html

   <details>
   <summary>Order 4 Costas Loop Error Equation (for those curious)</summary>

.. code-block:: python

    # For QPSK
    def phase_detector_4(sample):
        if sample.real > 0:
            a = 1.0
        else:
            a = -1.0
        if sample.imag > 0:
            b = 1.0
        else:
            b = -1.0   
        return a * sample.imag - b * sample.real




.. raw:: html

   </details>

The :code:`alpha` and :code:`beta` variables define how fast the phase and frequency update, respectively.  There is some theory behind why I chose those two values; however, we won't address it here.  If you are curious you can try tweaking :code:`alpha` and/or :code:`beta` to see what happens.

We log the value of :code:`freq` each iteration so we can plot it at the end, to see how the Costas Loop converges on the correct frequency offset.  We have to multiply :code:`freq` by the sample rate and convert from angular frequency to Hz, by dividing by :math:`2\pi`.  Note that if you performed time sync prior to the Costas Loop, you will have to also divide by your :code:`sps` (e.g., 8), because the samples coming out of the time sync are at a rate equal to your original sample rate divided by :code:`sps`. 

Lastly, after recalculating phase, we add or remove enough :math:`2 \pi`'s to keep phase between 0 and :math:`2 \pi`,  which wraps phase around.

Our signal before and after the Costas Loop looks like this:

.. image:: ../_images/costas-loop-output.svg
   :align: center
   :target: ../_images/costas-loop-output.svg

And the frequency offset estimation over time, settling on the correct offset (a -300 Hz offset was used in this example signal):

.. image:: ../_images/costas-loop-freq-tracking.svg
   :align: center
   :target: ../_images/costas-loop-freq-tracking.svg

It takes nearly 70 samples for the algorithm to fully lock it on the frequency offset.  You can see that in my simulated example there were about -300 Hz left over after the coarse frequency sync.  Yours may vary.  Like I mentioned before, you can disable the coarse frequency sync and set the initial frequency offset to whatever value you want and see if the Costas Loop figures it out.

The Costas Loop, in addition to removing the frequency offset, aligned our BPSK signal to be on the I portion, making Q zero again.  It is a convenient side-effect from the Costas Loop, and it lets the Costas Loop essentially act as our demodulator.  Now all we have to do is take I and see if it's greater or less than zero.  We won't actually know how to make negative and positive to 0 and 1 because there may or may not be an inversion; there's no way for the Costas Loop (or our time sync) to know.  That is where differential coding comes into play.  It removes the ambiguity because 1's and 0's are based on whether or not the symbol changed, not whether it was +1 or -1.  If we added differential coding, we would still be using BPSK.  We would be adding a differential coding block right before modulation on the tx side and right after demodulation on the rx side.

Below is an animation of the time sync plus frequency sync running, the time sync actually happens almost immediately but the frequency sync takes nearly the entire animation to fully settle, and this was because :code:`alpha` and :code:`beta` were set too low, to 0.005 and 0.001 respectively.  The code used to generate this animation can be found `here <https://github.com/777arc/textbook/blob/master/figure-generating-scripts/costas_loop_animation.py>`_. 

.. image:: ../_images/costas_animation.gif
   :align: center 

***************************
Frame Synchronization
***************************

We have discussed how to correct any time, frequency, and phase offsets in our received signal.  But most modern communications protocols are not simply streaming bits at 100% duty cycle.  Instead, they use packets/frames.  At the receiver we need to be able to identify when a new frame begins.  Customarily the frame header (at the MAC layer) contains how many bytes are in the frame.  We can use that information to know how long the frame is, e.g., in units samples or symbols.  Nonetheless, detecting the start of frame is a whole separate task.  Below shows an example WiFi frame structure.  Note how the very first thing transmitted is a PHY-layer header, and the first half of that header is a "preamble".  This preamble contains a synchronization sequence that the receiver uses to detect start of frames, and it is a sequence known by the receiver beforehand.

.. image:: ../_images/wifi-frame.png
   :scale: 60 % 
   :align: center 

A common and straightforward method of detecting these sequences at the receiver is to cross-correlate the received samples with the known sequence.  When the sequence occurs, this cross-correlation resembles an autocorrelation (with noise added).  Typically the sequences chosen for preambles will have nice autocorrelation properties, such as the autocorrelation of the sequence creates a single strong spike at 0 and no other spikes.  One example is Barker codes, in 802.11/WiFi a length-11 Barker sequence is used for the 1 and 2 Mbit/sec rates:

.. code-block::

    +1 +1 +1 −1 −1 −1 +1 −1 −1 +1 −1

You can think of it as 11 BPSK symbols.  We can look at the autocorrelation of this sequence very easily in Python:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    x = [1,1,1,-1,-1,-1,1,-1,-1,1,-1]
    plt.plot(np.correlate(x,x,'same'),'.-')
    plt.grid()
    plt.show()
    
.. image:: ../_images/barker-code.svg
   :align: center
   :target: ../_images/barker-code.svg

You can see it's 11 (length of the sequence) in the center, and -1 or 0 for all other delays.  It works well for finding the start of a frame because it essentially integrates 11 symbols worth of energy in an attempt to create a 1 bit spike in the output of the cross-correlation.  In fact, the hardest part of performing start-of-frame detection is figuring out a good threshold.  You don't want frames that aren't actually part of your protocol to trigger it.  That means in addition to cross-correlation you also have to do some sort of power normalizing, which we won't consider here.  In deciding a threshold, you have to make a trade-off between probability of detection and probability of false alarms.  Remember that the frame header itself will have information, so some false alarms are OK; you will quickly find it is not actually a frame when you go to decode the header and the CRC inevitably fails (because it wasn't actually a frame).  Yet while some false alarms are OK, missing a frame detection altogether is bad.

Another sequence with great autocorrelation properties is Zadoff-Chu sequences, which are used in LTE.  They have the benefit of being in sets; you can have multiple different sequences that all have good autocorrelation properties, but they won't trigger each other (i.e., also good cross-correlation properties, when you cross-correlate different sequences in the set).  Thanks to that feature, different cell towers will be assigned different sequences so that a phone can not only find the start of the frame but also know which tower it is receiving from.











