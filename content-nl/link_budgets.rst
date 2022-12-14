.. _link-budgets-chapter:

##################
Link Budgets
##################

In dit hoofdstuk gaan we het hebben over "link budgetten". Een groot deel hiervan is het begrip van zend- en ontvangstvermogen, transmissieverlies, antenneversterking, ruis en signaal-ruisverhouding (SNR). We zullen eindigen met een voorbeeldbudget voor ADS-B, een signaal wat door commerciele vliegtuigen wordt uitgezonden om hun positie en overige informatie door te geven.

*************************
Introductie
*************************

Een "link" budget is een opsomming van alle winsten en verliezen tussen de zender en ontvanger van een communicatiesysteem.
Het beschrijft een richting van een draadloos kanaal.
De meeste communicatiesystemen zijn echter bidirectioneel en hebben dus aparte up- en downlink budgetten.
Het resultaat van zo'n budget geeft je een grove inschatting van de signaal-ruisverhouding (SNR) die je kunt verwachten bij de ontvanger.
Na verdere analyse kun je dan besluiten of de SNR hoog genoeg is voor jouw doel.

We bestuderen linkbudgetten niet zodat je er zelf een op kunt stellen, maar meer om een beeld te krijgen van draadloze communicatie op systeem-niveau.

Eerst zullen we het budget van het ontvangen signaal beschouwen, dan het ruisvermogen budget en als laatste zullen we die combineren om de SNR te vinden (Signaalvermogen gedeeld door ruisvermogen).

*************************
Signaalvermogensbudget
*************************

Hieronder zie je het meest simpele diagram wat je zou kunnen opstellen voor een algemene draadloze keten.
In dit hoofdstuk zullen we een richting behandelen, namelijk vanaf de zender (Tx) naar ontvanger (Rx).
We weten voor een gegeven systeem wat het zendvermogen is; dit is meestal een instelling bij de zender.
Maar hoe bepalen we het vermogen wat aankomt bij de ontvanger?

.. tikz:: [auto, node distance=2cm,>=latex',font=\sffamily]
  \tikzset{block/.style = {draw, fill=white, rectangle,
                    minimum height=3em, minimum width=2cm},
          input/.style = {coordinate},
          output/.style = {coordinate},
          pinstyle/.style = {pin edge={to-,t,black}}
      }
  \node[block](tx)                          {zender};
  \node[antenna](txant) at (tx.north) {};
  \draw[snake=expanding waves] (txant.north east) -- ++(1,0);
  \node[block,right = 6cm of tx](rx)        {ontvanger};
  \node[antenna,xscale=-1] at (rx.north) {};
  :libs: positioning,shapes,arrows,snakes
  :xscale: 80

.. .. image:: ../_images/tx_rx_system.svg
..    :align: center 
..    :target: ../_images/tx_rx_system.svg

We hebben vier systeemparameters nodig om het ontvangenvermogen te bepalen. Deze zijn hieronder opgesomt samen met de meestgebruikte (Engelstalige) afkortingen.
We zullen ieder apart behandelen in dit hoofdstuk.

- **Pt** - Vermogen van zender (Power transmitter)
- **Gt** - Antenneversterking zender (Gain transmitter)
- **Gr** - Antenneversterking ontvanger (Gain receiver)
- **Lt** - Afstande tussen zender en ontvanger dus hoeveelheid transmissieverlies (Path Loss)

.. tikz:: [auto, node distance=2cm,>=latex',font=\sffamily\small]
  \tikzset{block/.style = {draw, fill=white, rectangle,
                    minimum height=3em, minimum width=2cm},
          input/.style = {coordinate},
          output/.style = {coordinate},
          pinstyle/.style = {pin edge={to-,t,black}}
      }
  \node[block](tx)                            {zender};
  \node[block,right = 6cm of tx](rx)          {ontvanger};
  \node[antenna](txant) at (tx.north) {};
  \node[antenna,xscale=-1](rxant) at (rx.north) {};
  \draw[snake=expanding waves] 
    (txant.east) -- ++(1,0) coordinate(begin);
  \draw[ultra thick,gray] 
    (begin) -- ++(2,0) coordinate(midden);
  \draw[->,ultra thick, gray] 
    (midden) -- ++(2,0) node[right,align=center]  {Ontvangen\\vermogen \textbf{Pr}};
  \draw (midden) node[align=center, below]        {transmissieverlies\\\textbf{Lp}};
  \node[above=1cm of txant.north,align=center]    {Antenneversterking\\zender \textbf{Gt}};
  \node[above=1cm of rxant.north,align=center]    {Antenneversterking\\ontvanger \textbf{Gr}};
  \node[above right = 1 cm of txant.east,align=center]     {Zendvermogen\\\textbf{Gt}};
  :libs: positioning,shapes,arrows,snakes
  :xscale: 100

.. .. image:: ../_images/tx_rx_system_params.svg
..    :align: center 
..    :target: ../_images/tx_rx_system_params.svg

Zendvermogen
#####################

Zendvermogen is vrij simpel; het is uitgedrukt in Watt, dBW or dBm (dBm is een afkorting voor dBmW).
Elke zender heeft een of meerdere versterkers,  het zendvermogen is voornamelijk een eigenschap van die versterkers.
Een analogie voor zendvermogen is het vermogen van een lamp: hoe meer vermogen in Watt, hoe meer licht wordt uitgezonden door de lamp.
Hieronder staan wat gemiddelde vermogens van verschillende technologien:

==================  =====  =======
\                       Power    
------------------  --------------
Bluetooth           10 mW  -20 dBW   
WiFi                100mW  -10 dBW
LTE station         1W     0 dBW
FM station          10kW   40 dBW
==================  =====  =======

Antenneversterking
#####################

De antenneversterking van zend- en ontvangstantenne's zijn een cruciaal onderdeel van linkbudgetten.
Maar wat is antenneversterking?
Het is een indicatie van de richtingskarakteristiek.
Soms wordt het vermogensversterking genoemd, maar laat je niet misleiden, de enige manier voor een antenne om een hogere versterking te hebben is door de energie/straling te bundelen in een kleiner gebied.

Versterkingsfactoren worden uitgedrukt in dB (zonder eenheid), zie het :ref:`noise-chapter` hoofdstuk voor een opfriscursus.
Antennes zijn of omnidirectioneel (omni-antenne), dus het vermogen straalt in alle richtingen, of directioneel (richtantenne), het vermogen straalt een specifieke kant op.
Omni-antennes hebben een versterking tussen 0 dB en 3 dB.
Een richtantenne heeft een hogere versterking van 5 dB tot ongeveer 60 dB.

.. image:: ../_images/antenna_gain_patterns.png
   :scale: 80 % 
   :align: center 

Wanneer een richtantenne wordt toegepast zal het de juiste kant op moeten wijzen.
Als het een fase gestuurde antenne is dan kan het ook elektronish worden gericht (dus met software).

.. image:: ../_images/antenna_steering.png
   :scale: 80 % 
   :align: center 

Omni-antennes worden gebruikt wanneer je niet de richting aan kunt geven, zoals voor een mobiele telefoon of laptop.
Bij 5G kan een telefoon op hogere frequentiebanden werken zoals 26 GHz met een array van antennes en het elektronisch regelen van de bundelrichting.

Bij het opstellen van een linkbudget moeten we ervan uit gaan dat een richtantenne (zender of ontvanger) de juiste richting opwijst.
Als het niet de juiste kant opwijst dan is ons budget niet precies en vindt er verlies van communicatie plaats (wanneer bijvoorbeeld de tv-schotel verdraait door een bal).
Over het algemeen gaat ons linkbudget van een ideale situatie uit terwijl we de verliezen van zoveel mogelijke echte factoren meenemen.

Transmissieverlies (Path Loss)
##############################

Wanneer een signaal zich door de lucht (of vaccuum) beweegt, verliest het kracht.
Stel je voor dat je een klein zonnepaneel voor een lamp houdt.
Hoe verder je van de lamp afstaat, hoe minder energie het kan absorberen.
In de natuur- en wiskunde wordt **flux** gebruikt om aan te geven hoeveel "spul door je ding" gaat.
We willen bepalen hoeveel vermogen we kwijtraken voor een gegeven afstand.

.. image:: ../_images/flux.png
   :scale: 80 % 
   :align: center 

Free Space Path Loss (FSPL) of transmissieverlies in vrije ruimte verteld ons het verlies wanneer er geen obstakels tussen zender en ontvanger staan.
In het algemeen :math:`\mathrm{FSPL} = ( 4\pi d / \lambda )^2`. 
Google Friis transmissieformule voor meer informatie.
(Leuk weetje: signalen ervaren 377 ohm aan impedantie wanneer ze door de vrije ruimte bewegen.)
Bij het opstellen van ons linkbudget kunnen we dezelfde formule toepassen, maar omgezet naar dB:

.. math::
 \mathrm{FSPL}_{dB} = 20 \log_{10} d + 20 \log_{10} f - 147.55 \left[ dB \right]

Dit wordt uigedrukt in de eenheidsloze vorm dB omdat het een verlies betreft.
:math:`d` is de afstand tussen zender en ontvanger in meters.
:math:`f` is de draaggolffrequentie in Hz.
Er is alleen een probleem met deze vergelijking; er staan bijna altijd obstakels tussen zender en ontvanger.
Binnenshuis stuiteren signalen ook nog eens (de meeste frequenties gaan door gipsmuren heen, maar niet (goed) door metaal of dikke baksteen muren).
In deze situaties worden andere modellen gebruikt.
Een veelgebruikt model voor steden en bewoonde gebieden is het Okumura–Hata model:

.. math::
 L_{path} = 69.55 + 26.16 \log_{10} f - 13.82 \log_{10} h_B - C_H + \left[ 44.9 - 6.55 \log_{10} h_B \right] \log_{10} d

Hierbij is :math:`L_{path}` het transmissieverlies in dB, :math:`h_B` is de hoogte van de antenne boven de grond in meters, :math:`f` is de draaggolffrequentie in MHz, :math:`d` is de afstand tussen zender en ontvanger in km en :math:`C_H` wordt de "antenne correctiefactor" genoemd en wordt gedefinieerd aan de hand van het frequentiebereik en de grootte van de stad:

:math:`C_H` voor dorpen:

.. math::
 C_H = 0.8 + (1.1 \log_{10} f - 0.7 ) h_M - 1.56 \log_{10} f

:math:`C_H` voor steden met :math:`f` onder 200 MHz:

.. math::
 C_H = 8.29 ( log_{10}(1.54 h_M))^2 - 1.1
 
:math:`C_H` voor steden met :math:`f` tussen 200 MHz en 1.5 GHz:

.. math::
 C_H = 3.2 ( log_{10}(11.75 h_M))^2 - 4.97

waarbij :math:`h_M` de hoogte van de ontvangstantenne is boven de grond in meters.

Maak je geen zorgen als dit allemaal verwarrend is; het wordt hier getoond om te laten zien dat het model met obstakels veel ingewikkelder is dan de simpele FSPL vergelijking. Het resultaat van deze modellen is een enkel getal dat we kunnen gebruiken in ons linkbudget. We blijven FSPL gebruiken voor de rest van dit hoofdstuk.

Overige verliezen
#####################

In our link budget we also want to take into account miscellaneous losses.  We will lump these together into one term, usually somewhere between 1 – 3 dB.  Examples of miscellaneous losses:

- Cable loss
- Atmospheric Loss
- Antenna pointing imperfections
- Precipitation

The plot below shows atmospheric loss in dB/km over frequency (we will usually be < 40 GHz).  If you take some time to understand the y-axis, you'll see that short range communications below 40 GHz **and** less than 1 km have 1 dB or less of atmospheric loss, and thus we generally ignore it.  When atmospheric loss really comes into play is with satellite communications, where the signal has to travel many km through the atmosphere. 

.. image:: ../_images/atmospheric_attenuation.svg
   :align: center 
   :target: ../_images/atmospheric_attenuation.svg

Signal Power Equation
#####################

Now it's time to put all of these gains and losses together to calculate our signal power at the receiver, :math:`P_r`:

.. math::
 P_r = P_t + G_t + G_r - L_p - L_{misc} \quad \mathrm{dBW}

Overall it's an easy equation. We add up the gains and losses. Some might not even consider it an equation at all.  We usually show the gains, losses, and total in a table, similar to accounting, like this:

.. list-table::
   :widths: 15 10
   :header-rows: 0
   
   * - Pt = 1.0 W
     - 0 dBW
   * - Gt = 100
     - 20.0 dB
   * - Gr = 1
     - 0 dB
   * - Lp
     - -162.0 dB
   * - Lmisc
     - -1.0 dB
   * - **Pr**
     - **-143.0 dBW**


*************************
Noise Power Budget
*************************

Now that we know the received signal power, let's change topic to received noise, since we need both to calculate SNR after all.  We can find received noise with a similar style power budget.

Now is a good time to talk about where noise enters our comms link.  Answer: **At the receiver!**  The signal is not corrupted with noise until we go to receive it.  It is *extremely* important to understand this fact! Many students don't quite internalize it, and they end up making a foolish error as a result.  There is not noise floating around us in the air. The noise comes from the fact that our receiver has an amplifier and other electronics that are not perfect and not at 0 degrees Kelvin (K).

A popular and simple formulation for the noise budget uses the "kTB" approach:

.. math::
 P_{noise} = kTB

- :math:`k` – Boltzmann’s constant = 1.38 x 10-23 J/K = **-228.6 dBW/K/Hz**.  For anyone curious, Boltzmann’s constant is a physical constant relating the average kinetic energy of particles in a gas with the temperature of the gas.
- :math:`T` – System noise temperature in K (cryocoolers anyone?), largely based on our amplifier.  This is the term that is most difficult to find, and is usually very approximate.  You might pay more for an amplifier with a lower noise temperature. 
- :math:`B` – Signal bandwidth in Hz, assuming you filter out the noise around your signal.  So an LTE downlink signal that is 10 MHz wide will have :math:`B` set to 10 MHz, or 70 dBHz.

Multiplying out (or adding in dB) kTB gives our noise power, i.e., the bottom term of of our SNR equation.

*************************
SNR
*************************

Now that we have both numbers, we can take the ratio to find SNR, (see the :ref:`noise-chapter` chapter for more information about SNR):

.. math::
   \mathrm{SNR} = \frac{P_{signal}}{P_{noise}}

.. math::
   \mathrm{SNR_{dB}} = P_{signal\_dB} - P_{noise\_dB}

We typically shoot for an SNR > 10 dB, although it really depends on the application.  In practice, SNR can be verified by looking at the FFT of the received signal or by calculating the power with and without the signal present (recall variance = power).  The higher the SNR, the more bits per symbol you can manage without too many errors.

***************************
Example Link Budget: ADS-B
***************************

Automatic Dependent Surveillance-Broadcast (ADS-B) is a technology used by aircraft to broadcast signals that share their position and other status with air traffic control ground stations and other aircraft.  ADS–B is automatic in that it requires no pilot or external input; it depends on data from the aircraft's navigation system and other computers.  The messages are not encrypted (yay!).  ADS–B equipment is currently mandatory in portions of Australian airspace, while the United States requires some aircraft to be equipped, depending on the size.

.. image:: ../_images/adsb.jpg
   :scale: 120 % 
   :align: center 
   
The Physical (PHY) Layer of ADS-B has the following characteristics:

- Transmitted on 1,090 MHz
- Signal has 50 kHz of bandwidth (which is very small)
- PPM modulation
- Messages carry 15 bytes of data each, so multiple messages are usually needed
- Multiple access is achieved by having messages broadcast with a period that ranges randomly between 0.4 and 0.6 seconds.  This randomization is designed to prevent aircraft from having all of their transmissions on top of each other (some may still collide but that’s fine)
- ADS-B antennas are vertically polarized
- Transmit power varies, but should be in the ballpark of 100 W (20 dBW)
- Transmit antenna gain is omnidirectional but only pointed downward, so let's say 3 dB
- ADS-B receivers also have an omnidirectional antenna gain, so let's say 0 dB

The path loss depends on how far away the aircraft is from our receiver.  As an example, it's about 30 km between the University of Maryland (where the course that this textbook's content originated from was taught) and the BWI airport.  Let's calculate FSPL for that distance and a frequency of 1,090 MHz:

.. math::
    \mathrm{FSPL}_{dB} = 20 \log_{10} d + 20 \log_{10} f - 147.55  \left[ \mathrm{dB} \right]
    
    \mathrm{FSPL}_{dB} = 20 \log_{10} 30e3 + 20 \log_{10} 1090e6 - 147.55  \left[ \mathrm{dB} \right]

    \mathrm{FSPL}_{dB} = 122.7 \left[ \mathrm{dB} \right]

Another option is to leave :math:`d` as a variable in the link budget and figure out how far away we can hear signals based on a required SNR. 

Now because we definitely won't have free space, let's add another 3 dB of miscellaneous loss.  We will make the miscellaneous loss 6 dB total, to take into account our antenna not being well matched and cable/connector losses.  Given all of this criteria, our signal link budget looks like:

.. list-table::
   :widths: 15 10
   :header-rows: 0
   
   * - Pt
     - 20 dBW
   * - Gt
     - 3 dB
   * - Gr
     - 0 dB
   * - Lp
     - -122.7 dB
   * - Lmisc
     - -6 dB
   * - **Pr**
     - **-105.7 dBW**

For our noise budget:

- B = 50 kHz = 50e3 = 47 dBHz
- T we have to approximate, let's say 300 K, which is 24.8 dBK.  It will vary based on quality of the receiver
- k is always -228.6 dBW/K/Hz 

.. math::
 P_{noise} = k + T + B = -156.8 \quad \mathrm{dBW}
 
Therefore our SNR is -105.7 - (-156.8) = **51.1 dB**.  It's not surprising it is a huge number, considering we are claiming to only be 30 km from the aircraft under free space.  If ADS-B signals couldn't reach 30 km then ADS-B wouldn't be a very effective system--no one would hear each other until they were very close.  Under this example we can easily decode the signals; pulse-position modulation (PPM) is fairly robust and does not require that high an SNR.  What's difficult is when you try to receive ADS-B while inside a classroom, with an antenna that is very poorly matched, and a strong FM radio station nearby causing interference.  Those factors could easily lead to 20-30 dB of losses.

This example was really just a back-of-the-envelope calculation, but it demonstrated the basics of creating a link budget and understanding the important parameters of a comms link. 



















