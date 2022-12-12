.. _filters-chapter:

#############
Filters
#############

We gaan in dit hoofdstuk leren over digitale filters in Python.
We zullen type filters behandelen (FIR/IIR en laag-doorlaat/hoog-doorlaat/band-doorlaat/band-stop), hoe ze digitaal eruit zien, en hoe ze ontworpen worden.
Als laatste eindigen we met een introductie over 'pulse shaping' (Nederlands: pulsvorming), wat zal worden uitgediept in het :ref:`pulse-shaping-chapter` hoofdstuk.

*************************
Basis van Filters
*************************

Veel disciplines maken gebruik van filters.
Beelverwerking maakt bijvoorbeeld uitvoerig gebruik van 2D filters waarbij de in- en uitgang figuren betreft.
Wellicht gebruik je elke morgen een koffiefilter om de vaste en vloeibare stoffen te scheiden.
Maar in DSP worden filters voornamelijk gebruikt voor het:

1. Scheiden van gecombineerde signalen (dus het gewenste signaal extraheren)
2. Verwijderen van overbodige ruis na ontvangst van een signaal
3. Herstellen van signalen die zijn vervormt (een audio equalizer is bijv. een filter)

Natuurlijk zijn er nog meer toepassingen, maar de bedoeling van dit hoofdstuk is om het concept te introduceren in plaats van alle filter toepassingen.

Misschien denk je dat we alleen geintereseerd zijn in digitale filters; het is ten slotte een DSP boek.
Het is echter belangrijk om te begrijpen dat veel filters analoog zullen zijn, zoals de filters die in jouw SDR voor de ADC's zijn gezet.
Het volgende figuur plaatst een schema van een analoog filter tegenover het schematisch ontwerp van een digitaal filter.

.. annotate image in tikz with text.
.. tikz:: [font=\sffamily\Large\bfseries]
   \node[anchor=south west,inner sep=0](image) at (0,0) {\includegraphics[scale=1.5]{analog_digital_filter_nolabel.png}};
   \begin{scope}[x={(image.south east)},y={(image.north west)}]
      \node[] at (0.25,0.9) {Analoog filter};
      \node[] at (0.75,0.9) {Digitaal filter};
   \end{scope}
  
DSP's hebben signalen als in- en uitgangen. Een filter heeft een ingangsignaal en een uitgangsignaal:

.. tikz:: [font=\sffamily\Large\bfseries, scale=2]
   \definecolor{babyblueeyes}{rgb}{0.36, 0.61, 0.83}
   \node [draw,
    color=white,
    fill=babyblueeyes,
    minimum width=4cm,
    minimum height=2.4cm
   ]  (filter) {Filter};
   \draw[<-, very thick] (filter.west) -- ++(-2,0) node[left,align=center]{Ingang\\(tijddomein)} ;
   \draw[->, very thick] (filter.east) -- ++(2,0) node[right,align=center]{Uitgang\\(tijddomein)};   
   :libs: positioning

.. .. image:: ../_images/filter.png
..    :scale: 70 % 
..    :align: center 

Je kunt niet twee verschillende signalen in een enkel filter stoppen zonder ze eerst samen te voegen of een andere operatie uit te voeren.
Op dezelfde manier zal de uitgang altijd een signaal betreffen, bijv. een 1D array van getallen.

Er zijn vier basistypen van filters: laag-doorlaat, hoog-doorlaat, band-doorlaat en band-stop.
Elke type bewerkt signalen zodanig dat de focus op verschillende gebieden aan frequenties ligt.
De onderstaande grafieken laten voor elke van de typen zien hoe de frequenties worden gefilterd.
We merken op dat onderstaande figuren ook de negatieve frequenties tonen. Zolang de filters "reeel" zijn, zullen ook de filters gespiegeld zijn rondom 0 Hz.

.. the only way i could manage to get the tikz drawings next each other
.. was to use a html table... In a pdf the pictures would be beneath each
.. other
.. raw:: html

   <table><tbody><tr><td>

.. This draw the lowpass filter
.. tikz:: [font=\sffamily\Large]    
   \draw[->, thick] (-5,0) -- (5,0) node[below]{Frequentie};
   \draw[->, thick] (0,-0.5) node[below]{0 Hz} -- (0,5) node[left=1cm]{\textbf{Laag-doorlaat}};
   \draw[red, thick, smooth] plot[tension=0.5] coordinates{(-5,0) (-2.5,0.5) (-1.5,3) (1.5,3) (2.5,0.5) (5,0)};

.. raw:: html

   </td><td>

.. this draws the highpass filter
.. tikz:: [font=\sffamily\Large]    
   \draw[->, thick] (-5,0) -- (5,0) node[below]{Frequentie};
   \draw[->, thick] (0,-0.5) node[below]{0 Hz} -- (0,5) node[left=1cm]{\textbf{Hoog-doorlaat}};
   \draw[red, thick, smooth] plot[tension=0.5] coordinates{(-5,3) (-2.5,2.5) (-1.5,0.3) (1.5,0.3) (2.5,2.5) (5,3)};

.. raw:: html

   </td><td>

.. this draws the bandpass filter
.. tikz:: [font=\sffamily\Large]    
   \draw[->, thick] (-5,0) -- (5,0) node[below]{Frequentie};
   \draw[->, thick] (0,-0.5) node[below]{0 Hz} -- (0,5) node[left=1cm]{\textbf{Band-doorlaat}};
   \draw[red, thick, smooth] plot[tension=0.5] coordinates{(-5,0) (-4.5,0.3) (-3.5,3) (-2.5,3) (-1.5,0.3) (1.5, 0.3) (2.5,3) (3.5, 3) (4.5,0.3) (5,0)};

.. raw:: html

   </td><td>

.. and finally the bandstop filter
.. tikz:: [font=\sffamily\Large]    
   \draw[->, thick] (-5,0) -- (5,0) node[below]{Frequentie};
   \draw[->, thick] (0,-0.5) node[below]{0 Hz} -- (0,5) node[left=1cm]{\textbf{Band-stop}};
   \draw[red, thick, smooth] plot[tension=0.5] coordinates{(-5,3) (-4.5,2.7) (-3.5,0.3) (-2.5,0.3) (-1.5,2.7) (1.5, 2.7) (2.5,0.3) (3.5, 0.3) (4.5,2.7) (5,3)};   
   
.. raw:: html

   </td></tr></tbody></table>

.. .......................... end of filter plots in tikz

.. .. image:: ../_images/filter_types.png
..    :scale: 70 % 
..    :align: center 

Elke filter laat sommige frequenties in een signaal door terwijl het andere frequenties blokkeert.
Het bereik aan frequenties wat wordt doorgelaten heet de "doorlaatband", en wat wordt geblokkeert heet de "stopband".
In het geval van een laag-doorlaat filter worden lage frequenties doorgelaten en hoge frequenties geblokkeert, dus 0Hz zal altijd in de doorlaatband vallen.
Bij de hoog-doorlaat en band-doorlaat filters bevindt 0 Hz zich altijd in de stopband.

Verwar deze filtertypes niet met de implementatietypes (dus IIR en FIR).
Omdat we regelmatig signalen in de basisband gebruiken, wordt het laag-doorlaat filter (LPF) veruit het meeste gebruikt.
Een LPF staat ons toe om alles "rond" ons signaal, zoals ruis en andere signalen, weg te filteren.

*************************
Filter opbouw
*************************

De meeste digitale filters die we tegen zullen komen (zoals FIR) kunnen we beschrijven met een array van floating point getallen.
Filters die in het frequentiedomein symetrisch zijn hebben reeele getallen (ipv complex), en meestal zijn er een oneven aantal.
We noemen deze array van getallen "coëfficienten" of in het Engels "taps".
Meestal gebruiken we :math:`h` als symbol voor deze filter coefficienten/taps. 
Hier zijn een aantal voorbeeld taps van een enkel filter:

.. code-block:: python

    h =  [ 9.92977939e-04  1.08410297e-03  8.51595307e-04  1.64604862e-04
     -1.01714338e-03 -2.46268845e-03 -3.58236429e-03 -3.55412543e-03
     -1.68583512e-03  2.10562324e-03  6.93100252e-03  1.09302641e-02
      1.17766532e-02  7.60955496e-03 -1.90555639e-03 -1.48306750e-02
     -2.69313236e-02 -3.25659606e-02 -2.63400086e-02 -5.04184562e-03
      3.08099470e-02  7.64264738e-02  1.23536693e-01  1.62377258e-01
      1.84320776e-01  1.84320776e-01  1.62377258e-01  1.23536693e-01
      7.64264738e-02  3.08099470e-02 -5.04184562e-03 -2.63400086e-02
     -3.25659606e-02 -2.69313236e-02 -1.48306750e-02 -1.90555639e-03
      7.60955496e-03  1.17766532e-02  1.09302641e-02  6.93100252e-03
      2.10562324e-03 -1.68583512e-03 -3.55412543e-03 -3.58236429e-03
     -2.46268845e-03 -1.01714338e-03  1.64604862e-04  8.51595307e-04
      1.08410297e-03  9.92977939e-04]

Voorbeeldtoepassing
########################

Om te leren hoe onze filters worden gebruikt gaan we kijken naar een voorbeeld waarin we onze SDR afstemmen op een frequentie van een bestaand signaal. Rondom dat signaal zijn andere signalen die we weg willen halen.
Vergeet niet dat terwijl we onze SDR af stemmen op een RF frequentie, dat de monsters die de SDR teruggeeft in de basisband zitten. Dit betekent dat het signaal dus gecentreerd zal zijn rond de 0 Hz.
We moeten zelf onthouden op welke frequentie we de SDR hadden ingesteld.
Dit zouden we dan kunnen ontvangen:

.. annotate filter spectrum image in tikz with text.
.. tikz:: [font=\sffamily\Large\bfseries]
   \node[anchor=south west,inner sep=0](image) at (0,0) {\includegraphics[scale=0.7]{filter_use_case_nolabel.png}};
   \begin{scope}[x={(image.south east)},y={(image.north west)}]
      \draw[red, ->] (0.3, 0.7) node[above left, align=center]{Gewenste\\signaal} -- (0.45, 0.6);
      \draw[red, ->] (0.9, 0.8) node[above right, align=center]{Ongewenst\\signaal} -- (0.8, 0.7);
      \draw[red, ->] (0.25, 0.2) node[below, align=center]{Ruisvloer} -- (0.3, 0.4);      
   \end{scope}

.. .. image:: ../_images/filter_use_case_nolabel.png
..    :scale: 40 % 
..    :align: center 

We weten dat we een laagdoorlaatfilter nodig hebben Omdat ons signaal al rond DC (0 Hz) is gecentreerd.
We moeten de "kantelfrequentie" (engels "cutoff") kiezen waar de doorlaatband overgaat in de stopband.
De kantelfrequentie wordt altijd in Hz gegeven.
In dit voorbeeld lijkt 3 kHz wel een goede waarde:

.. annotate filter spectrum image in tikz with text.
.. tikz:: [font=\sffamily\Large\bfseries]
   \node[anchor=south west,inner sep=0](image) at (0,0) {\includegraphics[scale=0.7]{filter_use_case_nolabel.png}};
   \begin{scope}[x={(image.south east)},y={(image.north west)}]
      \draw[red, ->] (0.3, 0.7) node[above left, align=center]{Gewenste\\signaal} -- (0.45, 0.6);
      \draw[red, ->] (0.9, 0.8) node[above right, align=center]{Ongewenst\\signaal} -- (0.8, 0.7);
      \draw[red, ->] (0.25, 0.2) node[below, align=center]{Ruisvloer} -- (0.3, 0.4); 
      \draw[red, dashed, very thick] (0.62, 0.1) -- (0.62,0.7);
   \end{scope}

Maar, gezien hoe de meeste laagdoorlaatfilters werken, zal de negatieve kantelfrequentie ook op (-)3 kHz liggen.
Het is dus symetrisch rond DC (later zien we waarom).
Onze kantelfrequenties zijn er dan ongeveer zo uit (de doorlaatband ligt tussen):

.. annotate filter spectrum image in tikz with text.
.. tikz:: [font=\sffamily\Large\bfseries]
   \node[anchor=south west,inner sep=0](image) at (0,0) {\includegraphics[scale=0.7]{filter_use_case_nolabel.png}};
   \begin{scope}[x={(image.south east)},y={(image.north west)}]
      \draw[red, ->] (0.3, 0.7) node[above left, align=center]{Gewenste\\signaal} -- (0.45, 0.6);
      \draw[red, ->] (0.9, 0.8) node[above right, align=center]{Ongewenst\\signaal} -- (0.8, 0.7);
      \draw[red, ->] (0.25, 0.2) node[below, align=center]{Ruisvloer} -- (0.3, 0.4); 
      \draw[red, dashed, very thick] (0.622, 0.1) -- (0.622,0.7);
      \draw[red, dashed, very thick] (0.455, 0.1) -- (0.455,0.7);
   \end{scope}

Na het maken en toepassen van een filter met een kantelfrequentie van 3 kHz krijgen we:

.. image:: ../_images/filter_use_case4.png
   :scale: 70 % 
   :align: center 


Dit gefilterde signaal ziet er misschien verwarrend uit todat je beseft dat de ruisvloer rond de groene lijn *zat* op -70 dB.
Ook al zien het signaal rond de 10 kHz nog steeds, het is *sterk* in vermogen afgenomen.
Het is zelfs zwakker geworden dan de oude ruisvloer!
Daarnaast hebben we dus ook de meeste ruis in de stopband verwijdert. 

Naast de kantelfrequetie  is een ander belangrijke instelling van ons laagdoorlaatfilter de transitiebreedte (Engels: "Transition width").
Dit wordt uitgedrukt in Hz en het verteld het filter hoe *snel* het moet overgaan van de doorlaatband naar de stopband, want een directe overgang is onmogelijk.

Laten we de transitiebreedte weergeven.
In het onderstaande figuur laat de :green:`groene` lijn de ideale filterrespontie zien met een transitiebreedte van 0 Hz.
De :red:`rode` lijn laat een realistisch filter zien, met een golvend gedrag in de doorlaat- en stopband en met een bepaalde transitiebreedte.
De frequentie in dit figuur is genormaliseerd met de bemonsteringsfrequentie.

.. image:: ../_images/realistic_filter.png
   :scale: 100 % 
   :align: center 

Nu vraag je je misschien af waarom we niet gewoon een zo'n kleine transitiebreedte als mogelijk kiezen. 
De reden daarvoor is voornamelijk dat een kleinere breedte zal resulteren in meer coefficienten, en hoe meer coefficienten hoe intensiever het wordt om te berekenen. 
Een filter met 50 coefficienten kan heel de dag draaien en nog geen 1% CPU kracht gebruiken op een Raspberry Pi, terwijl een filter met 50000 coefficienten de CPU doet ontploffen!
Meestal gebruiken we een filter ontwerpprogramma om te zien over hoe veel coefficienten het gaat. Als dit veel te veel is (bijv. meer dan 100) dan verbreden we de transitie. 
Natuurlijk hangt dit allemaal af van de toepassing en de hardware waarop het filter draait.

In het filtervoorbeeld hierboven hebben we een 3 kHz kantelfrequentie en een transitiebreedte van 1 kHz gebruikt. Het resulterende filter gebruikte 77 coefficienten.

Terug naar de filteropbouw.
Ook al laten we een lijst van coefficienten zien voor een filter, meestal visualiseren we een filter in het frequentiedomein.
Dit wordt de frequentierespontie genoemd van het filter en laat het gedrag in frequentie zien.
Het is de frequentierespontie van het filter dat we zojuist gebruikten:

.. image:: ../_images/filter_use_case5.png
   :scale: 100 % 
   :align: center 

Let op dat wat hier getoond wordt *niet* een signaal is, het is de frequentierespontie van het filter.
Misschien is dit moeilijk om je vinger op te leggen maar terwijl we voorbeelden en programma's bekijken zal het duidelijk worden.

Een filter heeft ook een tijddomein-versie; dit heet de "impulsrespons" van het filter omdat dit de filteruitgang in de tijd is wanneer we een impuls aan de ingang geven. (Google de "dirac delta functie" voor meer informatie over zo'n impuls)
Voor een geven FIR filter is de impulsrespons gelijk aan de coefficienten zelf.
Voor dat filter met 77 coefficienten van eerder is dat:

.. code-block:: python

    h =  [-0.00025604525581002235, 0.00013669139298144728, 0.0005385575350373983,
    0.0008378280326724052, 0.000906112720258534, 0.0006353431381285191,
    -9.884083502996931e-19, -0.0008822851814329624, -0.0017323142383247614,
    -0.0021665366366505623, -0.0018335371278226376, -0.0005912294145673513,
    0.001349081052467227, 0.0033936649560928345, 0.004703888203948736,
    0.004488115198910236, 0.0023609865456819534, -0.0013707970501855016,
    -0.00564080523326993, -0.008859002031385899, -0.009428252466022968,
    -0.006394983734935522, 4.76480351940553e-18, 0.008114570751786232,
    0.015200719237327576, 0.018197273835539818, 0.01482443418353796,
    0.004636279307305813, -0.010356673039495945, -0.025791890919208527,
    -0.03587324544787407, -0.034922562539577484, -0.019146423786878586,
    0.011919975280761719, 0.05478153005242348, 0.10243935883045197,
    0.1458890736103058, 0.1762896478176117, 0.18720689415931702,
    0.1762896478176117, 0.1458890736103058, 0.10243935883045197,
    0.05478153005242348, 0.011919975280761719, -0.019146423786878586,
    -0.034922562539577484, -0.03587324544787407, -0.025791890919208527,
    -0.010356673039495945, 0.004636279307305813, 0.01482443418353796,
    0.018197273835539818, 0.015200719237327576, 0.008114570751786232,
    4.76480351940553e-18, -0.006394983734935522, -0.009428252466022968,
    -0.008859002031385899, -0.00564080523326993, -0.0013707970501855016,
    0.0023609865456819534, 0.004488115198910236, 0.004703888203948736,
    0.0033936649560928345, 0.001349081052467227, -0.0005912294145673513,
    -0.0018335371278226376, -0.0021665366366505623, -0.0017323142383247614,
    -0.0008822851814329624, -9.884083502996931e-19, 0.0006353431381285191,
    0.000906112720258534, 0.0008378280326724052, 0.0005385575350373983,
    0.00013669139298144728, -0.00025604525581002235]

Ook al hebben we nog niets geleerd over filterontwerp, hieronder kun je de code van dat filter vinden:

.. code-block:: python

    import numpy as np
    from scipy import signal
    import matplotlib.pyplot as plt

    num_taps = 51 # aantal coefficiente
    cut_off = 3000 # kantelfrequentie in Hz
    sample_rate = 32000 # Hz

    # laag-doorlaatfilter
    h = signal.firwin(num_taps, cut_off, nyq=sample_rate/2)

    # impulsrespons weergeven
    plt.plot(h, '.-')
    plt.show()

Wanneer we deze coefficienten in de tijd weergeven dan krijgen we de impulsrepons:

.. image:: ../_images/impulse_response.png
   :scale: 100 % 
   :align: center 

De code om de frequentierespontie te geven van eerder wordt hieronder getoond. 
Dit is iets ingewikkelder omdat we een x-as voor de frequenties moeten opzetten.

.. code-block:: python

    # Frequentierespontie
    H = np.abs(np.fft.fft(h, 1024)) # neem een 1024-punten FFT met modulus
    H = np.fft.fftshift(H) # frequenties op juiste plek zetten
    w = np.linspace(-sample_rate/2, sample_rate/2, len(H)) # x-as
    plt.plot(w, H, '.-')
    plt.show()

Reele vs Complexe filters
#########################

Voorzover hadden de filters reeele coefficienten maar de coefficienten kunnen ook complex zijn. 
Of de coefficienten reeel of complex zijn heeft niets te maken met de ingang, je kunt een reeel signaal in een complex filter stoppen en andersom.
Waneer de coëfficiënten reeel zijn dan is de frequentierespontie symetrisch rondom DC (0Hz).
We gebruiken complexe coefficienten alleen wanneer we een asymmetrisch filter willen, wat niet vaak het geval is.


.. draw real vs complex filter
.. tikz:: [font=\sffamily\Large,scale=2] 
   \definecolor{babyblueeyes}{rgb}{0.36, 0.61, 0.83}   
   \draw[->, thick] (-5,0) node[below]{$-\frac{f_s}{2}$} -- (5,0) node[below]{$\frac{f_s}{2}$};
   \draw[->, thick] (0,-0.5) node[below]{0 Hz} -- (0,1);
   \draw[babyblueeyes, smooth, line width=3pt] plot[tension=0.1] coordinates{(-5,0) (-1,0) (-0.5,2) (0.5,2) (1,0) (5,0)};
   \draw[->,thick] (6,0) node[below]{$-\frac{f_s}{2}$} -- (16,0) node[below]{$\frac{f_s}{2}$};
   \draw[->,thick] (11,-0.5) node[below]{0 Hz} -- (11,1);
   \draw[babyblueeyes, smooth, line width=3pt] plot[tension=0] coordinates{(6,0) (11,0) (11,2) (11.5,2) (12,0) (16,0)};
   \draw[font=\huge\bfseries] (0,2.5) node[above,align=center]{Een laagdoorlaatfilter met\\reële coëfficiënten};
   \draw[font=\huge\bfseries] (11,2.5) node[above,align=center]{Een laagdoorlaatfilter met\\complexe coëfficiënten};

.. .. image:: ../_images/complex_taps.png
..    :scale: 80 % 
..    :align: center 

Als een voorbeeld voor complexe coëfficiënten kunnen we de eerder signalen er weer bij pakken, maar deze keer zullen we het andere signaal proberen te ontvangen zonder de SDR opnieuw in te stellen.
Dit betekent dat we een banddoorlaatfilter willen gebruiken, maar niet een symetrische.
We will alleen de frequenties rond 7 tot 13 kHz gebruiken, maar niet de frequenties van -13 tot -7 kHz:

.. image:: ../_images/filter_use_case6.png
   :scale: 70 % 
   :align: center 

Een manier om dit filter te maken is om een laagdoorlaatfilter te nemen met een kantelfrequentie van 3 kHz en daarna op teschuiven in frequentie.
We kunnen een frequentieverschuiving aan x(t) (tijddomein) geven door het te vermenigvuldigen met :math:`e^{j2\pi f_0t}`.  
In dit geval moet dan :math:`f_0` 10 kHz zijn wat het filter 10 kHz zou opschuiven.
In het bovenstaande voorbeeld beschreef :math:`h` de coëfficiënten van het laagdoorlaatfilter.
Dus om ons banddoorlaatfilter te maken zullen we de coëfficiënten moeten vermenigvuldigen met :math:`e^{j2\pi f_0t}`, dit houdt in dat we aan elke monster (coëfficiënt) de juiste tijd moeten koppelen (de inverse van onze bemonsteringsfrequentie):

.. code-block:: python

    # (h staat in eerder gegeven code)

    # Verschuif het filter in frequentie door te vermenigvuldigen met exp(j*2*pi*f0*t)
    f0 = 10e3 # we verschuiven 10k
    Ts = 1.0/sample_rate # bemonsteringsfrequentie
    t = np.arange(0.0, Ts*len(h), Ts) # vector met tijden van monsters. (start, stop, stap)
    exponential = np.exp(2j*np.pi*f0*t) # dit is een complexe sinus

    h_band_pass = h * exponential # verschuiving uitvoeren

    # impulsresponsie weergeven
    plt.figure('impulse')
    plt.plot(np.real(h_band_pass), '.-')
    plt.plot(np.imag(h_band_pass), '.-')
    plt.legend(['real', 'imag'], loc=1)

    # frequentieresponsie weergeven
    H = np.abs(np.fft.fft(h_band_pass, 1024)) # 1024-punts FFT met modulus
    H = np.fft.fftshift(H) # frequenties op juiste plek zetten
    w = np.linspace(-sample_rate/2, sample_rate/2, len(H)) # x-as
    plt.figure('freq')
    plt.plot(w, H, '.-')
    plt.xlabel('Frequency [Hz]')
    plt.show()

De impuls- en frequentieresponsie worden hieronder weergeven:

.. annotate filter spectrum image in tikz with text.
.. tikz:: [font=\sffamily\Large\bfseries]
   \node[anchor=south west,inner sep=0](image) at (0,0) {\includegraphics[scale=0.7]{shifted_filter_nolabel.png}};
   \begin{scope}[x={(image.south east)},y={(image.north west)}]
      \draw 
      (0.25, 0) node[align=center] {Tijddomein}
      (0.25, 1) node[align=center] {Impulsresponsie}
      (0.75, 1) node[align=center] {Frequentieresponsie};
   \end{scope}

.. .. image:: ../_images/shifted_filter.png
..    :scale: 60 % 
..    :align: center 

Omdat ons filter niet symmetrisch is rond 0 Hz moeten we complexe coëfficiënten gebruiken en hebben we twee lijnen nodig om het te weergeven.
Wat aan de linkerkant van het bovenstaande figuur te zien is, is deze complexe impulsreponsie.
De rechterkant valideert dat we inderdaad het gewenste filter hebben verkregen; het filtert alles weg, behalve de frequenties rondom 10 kHz.
Let nogmaals op dat het bovenstaande signaal *geen* signaal is, maar de responsie van het filter.
Dit kan lastig zijn om te vatten want we passen het filter toe op een signaal en weergeven de uitgang in het frequentiedomein wat in veel gevallen bijna overeenkomt met de frequentieresponse van het filter.

Maak je geen zorgen als dit stuk nog meer verwarring heeft verzoorzaakt, 99% van de tijd gebruiken we alleen laagdoorlaatfilters met reële coëfficiënten.

*************************
Filterimplementatie
*************************

We zullen niet te diep in de stof van filterimplementatie duiken.
Ik leg liever de nadruk op filterontwerp (je kunt toch bruikbare implementaties vinden voor elke taal).
Voor nu draait het om een ding: Om een signaal met een FIR filter te filteren voer je convolutie uit tussen de impulsresponsie (de coefficienten) en het ingangssignaal.
De de discrete wereld gebruiken we een digitale convolutie (voorbeeld hieronder).

De driehoeken met een :math:`b_x` ernaast zijn de coefficienten en de driehoeken met :math:`z^{-1}` geven een vertraging aan van 1 tijdstap.

.. image:: ../_images/discrete_convolution.png
   :scale: 80 % 
   :align: center 

Je ziet nu miscshien wel waarom de coefficienten in het engels "taps" worden genoemd, dit komt voort uit hoe het filter wordt geimplementeerd.

FIR vs IIR
##############

Eer zijn grofweg twee verschillende typen filters: FIR en IIR

1. Finite impulse response (FIR)
2. Infinite impulse response (IIR)

We zullen niet diep op theorie gaan maar onthoud voor nu dat FIR filters gemakkelijker te ontwerpen zijn en alles kimmem doen wat je wilt als er maar genoeg coefficienten worden gegeven.
IIR filters zijn efficienter en zouden hetzelfde kunnen bereiken met minder coefficienten maar met het risico dat het filter onstabiel wordt en niet goed werkt.
Een gegeven lijst coefficienten zijn over het algemeen voor een FIR filter.
Als er wordt gesproken over "polen" dan betreft het een IIR filter.
In dit boek zullen we et bij FIR filters houden.

Het onderstaande figuur laat het verschil zien tussen een FIR en IIR filter. Ze hebben hetzelfde gedrag maar het FIR filter gebruikt 50 coefficienten en het IIR filter maar 12. Toch hebben ze beiden ongeveer dezelfde transitiebreedte.

.. image:: ../_images/FIR_IIR.png
   :scale: 70 % 
   :align: center 

Wat je hieruit kunt leren is dat het FIR filter veel meer computerkracht vereist dan een IIR filter voor hetzelfde gedrag.

Hieronder wat voorbeelden van FIR en IIR filters die je misschien in het echt al hebt gebruikt.

Wanneer je een "moving average" (voortschrijdend gemiddelde) filter over een lijst getallen toepast, dan is dat gewoon een FIR filter met coefficienten van 1.  
Het is ook een laagdoorlaatfilter; waarom? Wat is het verschil tussen 1'en en coefficienten die richting 0 vervallen?

.. raw:: html

   <details>
   <summary>Antwoorden</summary>

Een "moving average" filter is een laagdoorlaatfilter omdat het snelle veranderingen uitsmeert, de reden waarom mensen het willen gebruiken.
Een reden om coeffcienten te gebruiken die richting 0 gaan aan beide kanten is om plotselinge verandering aan de uitgang te voorkomen, zoals zou gebeuren als de ingang een tijd nul is en dan plotseling omhoog springt.

.. raw:: html

   </details>

Voor een IIR voorbeeld. Als je zoiets hebt gedaan:

    x = x*0.99 + new_value*0.01

waar de 0.99 en 0.01 de snelheid aangeeft waarmee de waarde verandert.
Dit is een handige manier om een variabele te veranderen zonder de vorige waarden te onthouden.
Dit is een laagdoorlaat IIR filter (omdat het de vorige uitgang gebruikt).
Hopelijk kun je zien waarom dit minder stabiel is. De waarden zullen nooit volledig verdwijnen!

*************************
Filterontwerptools
*************************

In practice, most people will use a filter designer tool or a function in code that designs the filter.  There are plenty of different tools, but for students I recommend this easy-to-use web app by Peter Isza that will show you impulse and frequency response: http://t-filter.engineerjs.com.  Using the default values, at the time of writing this at least, it's set up to design a low-pass filter with a passband from 0 to 400 Hz and stopband from 500 Hz and up.  The sample rate is 2 kHz, so the max frequency we can "see" is 1 kHz.

.. image:: ../_images/filter_designer1.png
   :scale: 70 % 
   :align: center 

Click the "Design Filter" button to create the taps and plot the frequency response.

.. image:: ../_images/filter_designer2.png
   :scale: 70 % 
   :align: center 

Click "Impulse Response" text above the graph to see the impulse response, which is a plot of the taps since this is an FIR filter.

.. image:: ../_images/filter_designer3.png
   :scale: 70 % 
   :align: center 

This app even includes the C++ source code to implement and use this filter.  The web app does not include any way to design IIR filters, which are in general much more difficult to design.


*************************
Convolution
*************************

We will take a brief detour to introduce the convolution operator. Feel free to skip this section if you are already familiar with it.

Adding two signals together is one way of combining two signals into one. In the :ref:`freq-domain-chapter` chapter we explored how the linearity property applies when adding two signals together.  Convolution is another way to combine two signals into one, but it is very different than simply adding them.  The convolution of two signals is like sliding one across the other and integrating.  It is *very* similar to a cross-correlation, if you are familiar with that operation.  In fact it is equivalent to a cross-correlation in many cases.

I believe the convolution operation is best learned through examples.  In this first example, we convolve two square pulses together:


.. image:: ../_images/convolution_animation1.gif
   :scale: 100 % 
   :align: center 
   
Because it's just a sliding integration, the result is a triangle with a maximum at the point where both square pulses lined up perfectly.  Let's look at what happens if we convolve a square pulse with a triangular pulse:

.. image:: ../_images/convolution_animation2.gif
   :scale: 150 % 
   :align: center 

In both examples, we have two input signals (one red, one blue), and then the output of the convolution is displayed.  You can see that the output is the integration of the two signals as one slides across the other.  Because of this "sliding" nature, the length of the output is actually longer than the input.  If one signal is :code:`M` samples and the other signal is :code:`N` samples, the convolution of the two can produce :code:`N+M-1` samples.  However, functions such as :code:`numpy.convolve()` have a way to specify whether you want the whole output (:code:`max(M, N)` samples) or just the samples where the signals overlapped completely (:code:`max(M, N) - min(M, N) + 1` if you were curious).  No need to get caught up in this detail. Just know that the length of the output of a convolution is not just the length of the inputs.

So why does convolution matter in DSP?  Well for starters, to filter a signal, we can simply take the impulse response of that filter and convolve it with the signal.  FIR filtering is simply a convolution operation.

.. image:: ../_images/filter_convolve.png
   :scale: 70 % 
   :align: center 

It might be confusing because earlier we mentioned that convolution takes in two *signals* and outputs one.  We can treat the impulse response like a signal, and convolution is a math operator after all, which operates on two 1D arrays.  If one of those 1D arrays is the filter's impulse response, the other 1D array can be a piece of the input signal, and the output will be a filtered version of the input.

Let's see another example to help this click.  In the example below, the triangle will represent our filter's impulse response, and the :green:`green` signal is our signal being filtered.

.. image:: ../_images/convolution.gif
   :scale: 70 % 
   :align: center 

The :red:`red` output is the filtered signal.  

Question: What type of filter was the triangle?

.. raw:: html

   <details>
   <summary>Answers</summary>

It smoothed out the high frequency components of the green signal (i.e., the sharp transitions of the square) so it acts as a low-pass filter.

.. raw:: html

   </details>


Now that we are starting to understand convolution, I will present the mathematical equation for it.  The asterisk (*) is typically used as the symbol for convolution:

.. math::

 (f * g)(t) = \int f(\tau) g(t - \tau) d\tau
 
In this above expression, :math:`g(t)` is the signal or input that is flipped and slides across :math:`f(t)`, but :math:`g(t)` and :math:`f(t)` can be swapped and it's still the same expression.  Typically, the shorter array will be used as :math:`g(t)`.  Convolution is equal to a cross-correlation, defined as :math:`\int f(\tau) g(t+\tau)`, when :math:`g(t)` is symmetrical, i.e., it doesn't change when flipped about the origin.

*************************
Filter Design in Python
*************************

Now we will consider one way to design an FIR filter ourselves in Python.  While there are many approaches to designing filters, we will use the method of starting in the frequency domain and working backwards to find the impulse response. Ultimately that is how our filter is represented (by its taps).

You start by creating a vector of your desired frequency response.  Let's design an arbitrarily shaped low-pass filter shown below:

.. image:: ../_images/filter_design1.png
   :scale: 70 % 
   :align: center 

The code used to create this filter is fairly simple:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    H = np.hstack((np.zeros(20), np.arange(10)/10, np.zeros(20)))
    w = np.linspace(-0.5, 0.5, 50)
    plt.plot(w, H, '.-')
    plt.show()


:code:`hstack()` is one way to concatenate arrays in numpy.  We know it will lead to a filter with complex taps. Why?

.. raw:: html

   <details>
   <summary>Answer</summary>

It's not symmetrical around 0 Hz.

.. raw:: html

   </details>

Our end goal is to find the taps of this filter so we can actually use it.  How do we get the taps, given the frequency response?  Well, how do we convert from the frequency domain back to the time domain?  Inverse FFT (IFFT)!  Recall that the IFFT function is almost exactly the same as the FFT function.  We also need to IFFTshift our desired frequency response before the IFFT, and then we need yet another IFFshift after the IFFT (no, they don't cancel themselves out, you can try).  This process might seem confusing. Just remember that you always should FFTshift after an FFT and IFFshift after an IFFT.

.. code-block:: python

    h = np.fft.ifftshift(np.fft.ifft(np.fft.ifftshift(H)))
    plt.plot(np.real(h))
    plt.plot(np.imag(h))
    plt.legend(['real','imag'], loc=1)
    plt.show()

.. image:: ../_images/filter_design2.png
   :scale: 90 % 
   :align: center 

We will use these taps shown above as our filter.  We know that the impulse response is plotting the taps, so what we see above *is* our impulse response.  Let's take the FFT of our taps to see what the frequency domain actually looks like.  We will do a 1,024 point FFT to get a high resolution:

.. code-block:: python

    H_fft = np.fft.fftshift(np.abs(np.fft.fft(h, 1024)))
    plt.plot(H_fft)
    plt.show()

.. image:: ../_images/filter_design3.png
   :scale: 70 % 
   :align: center 

See how the frequency response not very straight... it doesn't match our original very well, if you recall the shape that we initially wanted to make a filter for.  A big reason is because our impulse response isn't done decaying, i.e., the left and right sides don't reach zero.  We have two options that will allow it to decay to zero:

**Option 1:** We "window" our current impulse response so that it decays to 0 on both sides.  It involves multiplying our impulse response with a "windowing function" that starts and ends at zero.

.. code-block:: python

    # After creating h using the previous code, create and apply the window
    window = np.hamming(len(h))
    h = h * window

.. image:: ../_images/filter_design4.png
   :scale: 70 % 
   :align: center 


**Option 2:** We re-generate our impulse response using more points so that it has time to decay.  We need to add resolution to our original frequency domain array (called interpolating).

.. code-block:: python

    H = np.hstack((np.zeros(200), np.arange(100)/100, np.zeros(200)))
    w = np.linspace(-0.5, 0.5, 500)
    plt.plot(w, H, '.-')
    plt.show()
    # (the rest of the code is the same)

.. image:: ../_images/filter_design5.png
   :scale: 60 % 
   :align: center 

.. image:: ../_images/filter_design6.png
   :scale: 70 % 
   :align: center 


.. image:: ../_images/filter_design7.png
   :scale: 50 % 
   :align: center 

Both options worked.  Which one would you choose?  The second method resulted in more taps, but the first method resulted in a frequency response that wasn't very sharp and had a falling edge wasn't very steep.  There are numerous ways to design a filter, each with their own trade-offs along the way. Many consider filter design an art.


*************************
Intro to Pulse Shaping
*************************

We will briefly introduce a very interesting topic within DSP, pulse shaping. We will consider the topic in depth in its own chapter later, see :ref:`pulse-shaping-chapter`. It is worth mentioning alongside filtering because pulse shaping is ultimately a type of filter, used for a specific purpose, with special properties.

As we learned, digital signals use symbols to represent one or more bits of information.  We use a digital modulation scheme like ASK, PSK, QAM, FSK, etc., to modulate a carrier so information can be sent wirelessly.  When we simulated QPSK in the :ref:`modulation-chapter` chapter, we only simulated one sample per symbol, i.e., each complex number we created was one of the points on the constellation--it was one symbol.  In practice we normally generate multiple samples per symbol, and the reason has to do with filtering.

We use filters to craft the "shape" of our symbols because the shape in the time domain changes the shape in the frequency domain.  The frequency domain informs us how much spectrum/bandwidth our signal will use, and we usually want to minimize it.  What is important to understand is that the spectral characteristics (frequency domain) of the baseband symbols do not change when we modulate a carrier; it just shifts the baseband up in frequency while the shape stays the same, which means the amount of bandwidth it uses stays the same.  When we use 1 sample per symbol, it's like transmitting square pulses. In fact BPSK using 1 sample per symbol *is* just a square wave of random 1's and -1's:

.. image:: ../_images/bpsk.svg
   :align: center 
   :target: ../_images/bpsk.svg

And as we have learned, square pulses are not efficient because they use an excess amount of spectrum:

.. image:: ../_images/square-wave.svg
   :align: center 

So what we do is we "pulse shape" these blocky-looking symbols so that they take up less bandwidth in the frequency domain.  We "pulse shape" by using a low-pass filter because it discards the higher frequency components of our symbols.  Below shows an example of symbols in the time (top) and frequency (bottom) domain, before and after a pulse-shaping filter has been applied:

.. image:: ../_images/pulse_shaping.png
   :scale: 70 % 
   :align: center 

|

.. image:: ../_images/pulse_shaping_freq.png
   :scale: 90 % 
   :align: center 

Note how much quicker the signal drops off in frequency. The sidelobes are ~30 dB lower after pulse shaping; that's 1,000x less!  And more importantly, the main lobe is narrower, so less spectrum is used for the same amount of bits per second.

For now, be aware that common pulse-shaping filters include:

1. Raised-cosine filter
2. Root raised-cosine filter
3. Sinc filter
4. Gaussian filter

These filters generally have a parameter you can adjust to decrease the bandwidth used.  Below demonstrates the time and frequency domain of a raised-cosine filter with different values of :math:`\beta`, the parameter that defines how steep the roll-off is.

.. image:: ../_images/pulse_shaping_rolloff.png
   :scale: 40 % 
   :align: center 

You can see that a lower value of :math:`\beta` reduces the spectrum used (for the same amount of data). However, if the value is too low then the time domain symbols take longer to decay to zero. Actually when :math:`\beta=0` the symbols never fully decay to zero, which means we can't transmit such symbols in practice.  A :math:`\beta` value around 0.35 is common.

You will learn a lot more about pulse shaping, including some special properties that pulse shaping filters must satisfy, in the :ref:`pulse-shaping-chapter` chapter.





