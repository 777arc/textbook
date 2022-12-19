.. _channel-coding-chapter:

#####################
Channel Coding
#####################

Dit hoofdstuk introduceert de basis van kanaalcodering, bekend als voorwaardse foutcorrectie (Forward Error Correction: FEC), de Shannon Limiet, Hamming codes, Turbo en LDPC codes.
Kanaalcodering is een enorm gebied binnen de draadloze communicatie. Het is een tak van de "informatie theorie" wat de studie is over kwantificatie, opslag en communicatie van informatie.

*************************************
Waarom we kanaalcodering nodig hebben
*************************************

Zoals we hebben geleerd in het :ref:`noise-chapter` hoofdstuk, hebben draadloze kanalen last van ruis en komen onze symbolen dus niet perfect bij de ontvanger aan.
Mocht je een cursus over netwerken hebben gedaan dan weet je waarschijnlijk al iets over cyclic redundancy checks (CRC) wat fouten **detecteert** bij de ontvanger.
Het doel van kanaalcodering is niet alleen om bij de ontvanger fouten te herkennen, maar ook te **repareren**.
Als we wat fouten toelaten dan is het mogelijk om een hogere order modulatieschema toe te passen zonder de verbinding te breken. 
Bekijk, voor een visueel voorbeeld, eens de onderstaande constellatiediagrammen voor QPSK (links) en 16QAM (rechts) met dezelfde hoeveelheid ruis.
QPSK geeft 2 bits per symbool, terwijl 16QAM en dubbele datasnelheid heeft van 4 bits per symbool. Maar zie hoe bij het QPSK diagram de symbolen niet de beslissingsgrens (x- en y-as) overlappen en dus de symbolen correct worden ontvangen. Tegelijkertijd in het 16QAM-diagram overlappen de clusters wel, met als resultaat dat er een hoop verkeerde symbolen worden ontvangen.

.. image:: ../_images/qpsk_vs_16qam.png
   :scale: 90 % 
   :align: center 

Een CRC fout resulteert meestal in het opnieuw verzenden van een pakket, bij een protocol als TCP.
Als Alice een bericht stuurt naar Bob we zouden we liever niet Bob nog een bericht naar Alice laten sturen om de informatie opnieuw aan te vragen.   
Het doel van kanaalcodering is om overtollige of **redundante** informatie te sturen.
Door redundante data mee te sturen bouwen we een failsafe in om foute pakketten, hertransmissies en verloren data te kunnen voorkomen. 

Nu we weten waarom het nodig is, laten we kijken waar het wordt toegepast inde communicatieketen:

.. image:: ../_images/tx_rx_chain.svg
   :align: center 
   :target: ../_images/tx_rx_chain.svg

Er vinden meerdere stappen van codering plaats in de keten. Broncodering , de eerste stap, is het hetzelfde als kanaalcodering; broncodering heeft als doel de data zoveel mogelijk te comprimeren voordat het verzonden wordt, net als een bestandje zippen voordat je het emailt.
In andere woorden, de uitgang van de broncodering zal **kleiner** zijn dan de dataingang, maar de uitgabg van kanaalcodering zal langer zijn dan de ingang want er is overtollige informatie toegevoegd.

***************************
Typen Codes
***************************

Om kanaalcodering uit te voeren moeten we een "foutcorrectiecode" gebruiken. 
Deze code vertelt ons, gegeven de te versturen bits, welke bits we echt moeten versturen.
De meest simpele vorm wordt een "herhalingscode" genoemd; we herhalen een bit N keer op een rij.
Voor een herhalings-3 code zouden we elk bit driemaal versturen:

.. role::  raw-html(raw)
    :format: html

- 0 :raw-html:`&rarr;` 000
- 1 :raw-html:`&rarr;` 111


Het bericht 10010110  wordt na de kanaalcodering dan verstuurt als 111000000111000111111000.

Sommige van de codes werken op blokken van bits terwijl anderen op een stroom van bits werken.
De de codes die op blokken werken worden "blokcodes" genoemd, de codes die op stromen werken heten "convolutionele codes". Dit zijn de twee primaire codes. Onze herhalings-3 code is een blokcode dat werkt op blokken van drie bits.

Trouwens, deze codes worden niet alleen voor draadloze kanalen gebruikt. Ooit eens data op een harde schijf of SSD gezet en afgevraagd waarom dat altijd goed gaat? Geheugen schrijven en dan lezen is vergelijkbaar met een communicatiesysteem. Harde schijf/SSD controllers hebben foutcorrectie ingebouwd. Dit is volledig onzichtbaar voor het OS omdat het in de controller zit ingebouwd. CD-ROMs gebruikten de gestandaardiseerde Reed-Solomon codes .

***************************
Code-snelheid
***************************

Elke fourcorrectiecode bevat een vorm  van redundantie. Dit betekent dat wanneer we 100 bits aan informatie willen versturen dat we eigenlijk **meer dan** 100 bits nodig hebben.
De snelheid is dan de verhouding tussen de informatiebits en het totale aantal bits dat is verzonden (dus informatie plus de redundante bits).
Als we teruggaan naar ons voorbeeld van herhaling-3, als ik 100 bits aan informatie verstuur, dan kunnen we de snelheid als volgt bepalen:

- 300 bits worden verstuurt
- Slechts 100 bits aan informatie
- Code-snelheid = 100/300 = 1/3

De code-snelheid zal altijd minder zijn dan 1; er is een afweging tussen redundantie en doorvoersnelheid.
Een lagere code-snelheid betekent meer redundantie maar minder doorvoer.

***************************
Modulatie en codering
***************************

In het :ref:`modulation-chapter` hoofdstuk hebben we de invloed van ruis op modulatieschemas bekeken. Bij een lage signaalruisverhouding heb je lagere order van modulatieschema nodig (bijv. QPSK) om met de ruis om te kunnen gaan. Bij een hoge SNR kun je een schame als 256QAM toepassen om meer bits per seconden over te kunnen sturen. Kanaalcodering werkt hetzelfde; je wilt een lagere code-snelheid bij lage signaal-ruis verhoudingen en bij hoge signaal-ruis verhoudingen wil je een code-snelheid van bijna 1 gebruiken. Moderne communicatiesystemen hebben een combinaties van modulatie- en codeschemas, MCS. Elke MCS specificeert een modulatie- plus codeschema wat bij een specifieke SNR gebruikt moet worden.

Moderne systemen passen de MCS real-time aan op basis van de draadloze kanaalcondities. De ontvanger geeft feedback aan de zender over de kanaalkwaliteit.
Deze feedback moet gegeven worden voordat de de kwaliteit van het draadloze kanaal verandert, wat in ms kan gebeuren.
Deze adaptieve aanpak leid tot de hoogste doorvoersnelheid mogelijk, en wordt gebruikt door moderne technologien zoals LTE, 5G and wifi.
Hieronder zie je hoe een telefoontoren de MCS aanpast op basis van de afstand tot de gebruiker.

.. image:: ../_images/adaptive_mcs.svg
   :align: center 
   :target: ../_images/adaptive_mcs.svg

Wanneer MCS wordt aangepast, als je dit uitzet tegenover de SNR, dan krijg je een stapvormige grafiek zoals het figuur hieronder. Protocollen zoals LTE hebben vaak een tabel wat aangeeft welke MCS gebruikt zou moeten worden bij welke SNR.

.. image:: ../_images/adaptive_mcs2.svg
   :align: center 
   :target: ../_images/adaptive_mcs2.svg

***************************
Hamming Code
***************************

Laten we eens kijken naar simpele foutcorrectiecodes. De Hamming-code was de eerste niet-triviale code dat werkt ontwikkeld.
Aan het einde van 1940, bij Bell Laboratories, werkte Richard Hamming met een electromechanische computer die ponskaarten gebruikte.
Maar als er fouten werden gevonden dan moest de computer stoppen en de bedienden moesten de kaarten repareren.
Hamming raakte gefrustreerd dat zijn programma telkens bij een fout opnieuw opgestart moest worden.
Hij zei, "Damn it, als de machine een fout kan detecteren, waarom kan hij de fout niet vinden en ongedaan maken?".
De volgende paar jaren spendeerde hij tijd om de Hamming-code te ontwikkelen die precies dat voor elkaar kreeg.

In Hamming-code worden extra bits toegevoegd, pariteits- of controlebits, om redundantie in te bouwen.
Alle bitposities op machten van 2 zijn pariteitbits: 1,2,4,8, etc.
De andere bitposities bevatten de informatie.
De onderstaande tabel laat de pariteitsbits in het groen zien.
Elke pariteistbit :math:`p_x` is *verantwoordelijk* voor alle databits :math:`d_n` waarbij de bitpositie van de databits en de bitwise AND operatie met de pariteitsbit, een getal oplevert ongelijk aan 0.
Dit is met een rode X hieronder aangegeven.
Wanneer we dan een databit willen gebruiken, dan hebben we de pariteitsbits nodig die hier verantwoordelijk voor zijn. 
Om databit :math:`d_{11}` te gebruiken zouden we pariteitsbit :math:`p_8` ,en alle pariteitsbits die daarvoor kwamen, nodig hebben. 
De tabel verteld ons dan hoeveel pariteitsbits we nodig hebben voor elke databit. Dit patroon gaat oneindig door.

.. image:: ../_images/hamming.svg
   :align: center 
   :target: ../_images/hamming.svg

De hamming-code is een blokcode wat opereert op N databits per keer.
Met 3 pariteitsbits kunnen we opereren op een blok van 4 databits per keer.
Dit schema zouden we aangeven als Hamming(7,4), waarbij het eerste getal aangeeft hoeveel bits in totaal worden overgestuurd en het tweede getal hoeveel databits daarin zitten.

.. image:: ../_images/hamming2.svg
   :align: center 
   :target: ../_images/hamming2.svg

Hier volgen belangrijke eigenschappen van de Hamming-code:

- Het kan een bitfout repareren
- Het kan twee fouten detecteren maar niet repararen

Het proces van databits coderen met de hamming-code kan worden gaan door een matrixvermenigvuldiging met de "generator matrix".
In het onderstaande voorbeeld is 1011 de databit-vector dat we willen coderen en naar de ontvanger sturen.
De 2D matrix is de "generator matrix" dat het codeschema definitieert. Het resultaat van de vermenigvuldiging is een *code-woord* dat we willen versturen.

:math:`\vec{x}=\vec{a}G
=\begin{pmatrix}1&0&1&1\end{pmatrix}
\begin{pmatrix}1&0&0&0&1&1&0\\0&1&0&0&1&0&1\\0&0&1&0&0&1&1\\0&0&0&1&1&1&1\end{pmatrix}
=\begin{pmatrix}1&0&1&1&2&3&2\end{pmatrix}
=\begin{pmatrix}1&0&1&1&0&1&0\end{pmatrix}`

.. image:: ../_images/hamming3.png
   :scale: 60 % 
   :align: center 

The point of diving into Hamming codes was to give a taste of how error coding works.  Block codes tend to follow this type of pattern.  Convolutional codes work differently, but we won't get into it here; they often use Trellis-style decoding, which can be displayed in a diagram that looks like this:

.. image:: ../_images/trellis.svg
   :align: center 

***************************
Soft vs Hard Decoding
***************************

Recall that at the receiver demodulation occurs before decoding.  The demodulator can tell us its best guess as to which symbol was sent, or it can output the "soft" value.  For BPSK, instead of telling us 1 or 0, the demodulator can say 0.3423 or -1.1234, whatever the "soft" value of the symbol was.  Typically the decoding is designed to use hard or soft values.

- **Soft decision decoding** – uses the soft values
- **Hard decision decoding** – uses only the 1's and 0's

Soft is more robust because you are using all of the information at your disposal, but soft is also much more complicated to implement.  The Hamming Codes we talked about used hard decisions, while convolutional codes tend to use soft.

***************************
Shannon Limit
***************************

The Shannon limit or Shannon capacity is an incredible piece of theory that tell us how many bits per second of error-free information we can send:

.. math::
 C = B \cdot log_2 \left( 1 + \frac{S}{N}   \right)

- C – Channel capacity [bits/sec]
- B – Bandwidth of channel [Hz]
- S – Average received signal power [watts]
- N – Average noise power [watts]

This equation represents the best any MCS can do when operating at a high enough SNR to be error-free.  It makes more sense to plot the limit in bits/sec/Hz, i.e., bits/sec per amount of spectrum:

.. math::
 \frac{C}{B} = log_2 \left( 1 + \mathrm{SNR}   \right)

with SNR in linear terms (not dB).  However, when plotting it, we usually represent SNR in dB for convenience:

.. image:: ../_images/shannon_limit.svg
   :align: center 

If you see Shannon limit plots elsewhere that look a little different, they are probably using an x-axis of "energy per bit" or :math:`E_b/N_0`, which is just an alternative to working in SNR.

It might help simplify things to realize when the SNR is fairly high (e.g., 10 dB or higher), the Shannon limit can be approximated as :math:`log_2 \left( \mathrm{SNR} \right)`, which is roughly :math:`\mathrm{SNR_{dB}}/3` (`explained here <https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem#Bandwidth-limited_case>`_).  For example, at 24 dB SNR you're looking at 8 bits/sec/Hz, so if you have 1 MHz to use, that's 8 Mbps.  You might be thinking, "well that's just the theoretical limit", but modern communications get fairly close to that limit, so at a minimum it gives you a rough ballpark.  You can always cut that number in half to take into account packet/frame overhead and non-ideal MCS.

The max throughput of 802.11n WiFi operating in the 2.4 GHz band (which uses 20 MHz wide channels), according to the specs, is 300 Mbps.  Obviously you could sit right next to your router and get an extremely high SNR, maybe 60 dB, but to be reliable/practical the max throughput MCS (recall the staircase curve from above) is unlikely to require an SNR that high.  You can even take a look at the `MCS list for 802.11n <https://en.wikipedia.org/wiki/IEEE_802.11n-2009#Data_rates>`_.  802.11n goes up to 64-QAM, and combined with channel coding, it requires a SNR around 25 dB according to `this table <https://d2cpnw0u24fjm4.cloudfront.net/wp-content/uploads/802.11n-and-802.11ac-MCS-SNR-and-RSSI.pdf>`_.  That means, even at 60 dB SNR your WiFi will still use 64-QAM.  So at 25 dB the Shannon limit is roughly 8.3 bits/sec/Hz, which given 20 MHz of spectrum is 166 Mbps.  However, when you take into account MIMO, which we will cover in a future chapter, you can get four of those streams running in parallel, resulting in 664 Mbps.  Cut that number in half and you get something very close to the advertised max speed of 300 Mbps for 802.11n WiFi in the 2.4 GHz band.

The proof behind the Shannon limit is pretty crazy; it involves math that looks like this:

.. image:: ../_images/shannon_limit_proof.png
   :scale: 70 % 
   :align: center

For more information see `here <https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem>`_.

***************************
State of the Art Codes
***************************

Currently, the best channel coding schemes are:

1. Turbo codes, used in 3G, 4G, NASA’s spacecraft.
2. LDPC codes, used in DVB-S2, WiMAX, IEEE 802.11n.

Both of these codes approach the Shannon limit (i.e., almost hit it under certain SNRs).  Hamming codes and other simpler codes get nowhere near the Shannon limit.  From a research point of view, there is not much room left to improve in terms of the codes themselves.  Current research is focusing more on making the decoding more computationally efficient and adaptive to channel feedback.

Low-density parity-check (LDPC) codes are a class of highly efficient linear block codes.  They were first introduced by Robert G. Gallager in his PhD dissertation in 1960 at MIT.  Due to the computational complexity in implementing them, they were ignored until the 1990's!  He is 89 at the time of this writing (2020), is still alive, and has won many prizes for his work (decades after he did it).  LDPC is not patented and therefore free to use (unlike turbo codes), which is why it was used in many open protocols.

Turbo codes are based on convolutional codes.  It's a class of code that combines two or more simpler convolutional codes and an interleaver.  The fundamental patent application for turbo codes was filed on April 23, 1991.  The inventors were French, so when Qualcomm wanted to use turbo codes in CDMA for 3G they had to create a fee-bearing patent license agreement with France Telecom.  The primary patent expired August 29, 2013. 

