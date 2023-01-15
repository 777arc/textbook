.. _intro-chapter:

#############
Introductie
#############

***************************
Doel en doelgroep
***************************

Als eerste een paar belangrijke termen:

**Software-Defined Radio (SDR):**
    Of in het Nederlands een software gedefinieerde radio. Een radio dat software gebruikt om signaalbewerkingstaken uit te voeren die normaal in hardware werden gedaan    
  
**Digital signal Processing (DSP):**
    Of in het Nederlands: digitale signaalbewerking. Op een digitale manier signalen bewerken, in ons geval RF-signalen

Dit boek dient als een praktische introductie op de gebieden van DSP, SDR en draadloze communicatie. Het is ontworpen voor iemand die:

#. Coole dingen wilt *doen* met SDR's
#. Goed kan omgaan met Python
#. Relatief onbekend is met digitale signaalbewerking, draadloze communicatie en SDR
#. Liever (visueel) leert door animaties dan door vergelijkingen
#. Vergelijken beter begrijpt *na* het leren van de concepten
#. Op zoek is naar een korte uitleg en niet een boek van 1000 pagina's.

Als voorbeeld een student die interesse heeft in banen die te maken hebben met draadloze communicatie, of iedereen met een beetje programmeerervaring die graag leert over SDR. 
Om deze reden bevat dit boek de benodigde theorie om DSP-technieken te begrijpen zonder de intense wiskunde dat normaal in DSP-cursussen wordt gebruikt. 
In plaats van onszelf ingraven met vergelijkingen wordt een overvloed aan figuren en animaties gebruikt om de concepten te brengen, zoals de Fourierreeks animatie hieronder. 
Ik geloof dat vergelijkingen het beste worden begrepen *na* de concepten te hebben geleerd door middel van visuele en praktische oefeningen. 
Door het zware gebruik van animaties zal PySDR ook nooit als fysiek boek verschijnen op Amazon.

.. image:: ../_images/fft_logo_wide.gif
   :scale: 70 %   
   :align: center
   
Dit boek heeft als doel concepten snel en vloeiend te introduceren waardoor de lezer in staat is om DSP toe te passen en SDR’s intelligent te gebruiken. 
Het is niet bedoelt als verwijzing naar alle DSP/SDR onderwerpen; er zijn al veel geweldige boeken zoals `Analog Device's SDR boek
<https://www.analog.com/en/education/education-library/software-defined-radio-for-engineers.html>`_ en `dspguide.com <http://www.dspguide.com/>`_.  Je kunt altijd Google gebruiken om goniometrische identiteiten of de limiet van Shannon op te zoeken. Zie dit boek als een poort tot de wereld van DSP en SDR: het is makkelijker en minder tijd en geld consumerend alternatief vergeleken met traditionele cursussen en boeken. 

Om de basis DSP-theorie te behandelen, is een heel semester aan "Signalen en Systemen", een typische cursus bij elektrotechniek, samengevoegd tot een paar hoofdstukken. 
Wanneer de basis is behandeld, springen we naar SDR's, hoewel door het boek heen DSP- en draadloze-communicatie-concepten voorbij blijven komen.

De programmavoorbeelden worden gegeven in Python. 
Ze maken gebruik van NumPy, dit is de standaard bibliotheek van Python voor het gebruikt van arrays en abstracte wiskunde. 
De voorbeelden leunen ook op Matplotlib, een Python bibliotheek waarmee op een gemakkelijke manier signalen, arrays en complexe getallen gevisualiseerd kunnen worden. 
Terwijl Python "langzamer" is dan C/C++ worden bijna alle functies in Python/NumPy geïmplementeerd in C/C++ en hevig geoptimaliseerd. 
Op dezelfde manier bestaat de Python API dat we gebruiken uit functieverwijzingen naar C/C++ functies/klassen. 
Diegenen die een stevigere fundatie hebben met Matlab, Ruby of Perl dan met Python, zullen waarschijnlijk geen problemen ondervinden na het bekijken van de Python syntax.

***************
Meehelpen
***************

Als ook maar iets van dit boek hebt gelezen en je stuurt me een email (pysdr@vt.edu) met vragen/opmerkingen/suggesties dan, gefeliciteerd. Je hebt bijgedragen aan dit boek!

Op een grotere manier kun je meehelpen aan dit boek op dezelfde manier als elk ander open-source project; door Git. Dit boek mag wel de vorm hebben van een website. Maar het bronmateriaal wordt gegenereerd op basis van de `GitHub pagina <https://github.com/777arc/textbook>`_ van dit boek. Voel je vrij om een issue of zelfs een Pull Request (PR) met verbeteringen of opmerkingen aan te maken. Zij die waardevolle terugkoppeling bieden zullen permanent worden toegevoegd aan de bedragenlijst hieronder. Ben je niet zo bekwaam met Git, maar je hebt wel opmerkingen? Voel je vrij mij te e-mailen op pysdr@vt.edu. 

De website en dit boek worden zonder reclame aangeboden omdat we reclame haten. Ik accepteer ook geen donaties op PayPal of Bitcoin. Er is letterlijk geen manier voor mij om betaald te worden voor dit boek. In plaats hiervan raad ik aan dit boek te delen met collega's, studenten en andere levenslange studenten die geïnteresseerd zijn in dit onderwerp.

*****************
Erkenning
*****************

Bedankt aan iedereen die dit boek heeft gelezen en van feedback heeft voorzien, en met name aan:

- `Barry Duggan <http://github.com/duggabe>`_
- Matthew Hannon
- James Hayek
- Deidre Stuffer
- Tarik Benaddi voor het `vertalen van PySDR naar het Frans <https://pysdr.org/fr/index-fr.html>`_


**********************
Nederlandse vertaling
**********************

Bij het vertalen van dit boek heb ik de bewuste keuze gemaakt om een aantal termen in Engelse vorm te gebruiken. De belangrijkste hiervan is "sample". Een "sample" nemen heet in het Nederlands een "monster" nemen. Wanneer we het echter gaan hebben over dingen als bemonsteringsfrequentie dan gaan we in mijn mening het doel voorbij van dingen duidelijk overbrengen. Sample-frequentie is leesbaarder en herkenbaar uit vele online bronnen. Om deze reden heb ik "sample" i.p.v. "monster" aangehouden.

Ook hou ik de standaard afkortingen aan zoals SDR, DSP, FIR, IIR, LPF etc. Ik geef de Nederlandse vertaling van de termen waarna ik vervolgens de Engelse afkortingen gebruik.