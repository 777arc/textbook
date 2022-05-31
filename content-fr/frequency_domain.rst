.. _freq-domain-chapter:

#####################
Domaine Fréquentiel
#####################

Ce chapitre présente le domaine fréquentiel et couvre les séries de Fourier, la transformée de Fourier, les propriétés de Fourier, la FFT, le fenêtrage et les spectrogrammes, à l'aide d'exemples Python.

L'un des effets secondaires les plus intéressants de l'apprentissage du DSP et des communications sans fil est que vous apprendrez également à penser dans le domaine des fréquences. L'expérience de la plupart des gens avec le *travail* dans le domaine fréquentiel se limite au réglage des boutons graves/moyens/aigus sur le système audio d'une voiture. L'expérience de la plupart des gens avec *visualiser* quelque chose dans le domaine fréquentiel se limite à voir un égaliseur audio, tel que ce clip :

.. image:: ../_images/audio_equalizer.webp
   :align: center
   
À la fin de ce chapitre, vous comprendrez ce que signifie réellement le domaine fréquentiel, comment convertir entre le temps et la fréquence (ainsi que ce qui se passe lorsque nous le faisons), et quelques principes intéressants que nous utiliserons tout au long de nos études sur DSP et SDR. À la fin de ce manuel, vous serez passé maître dans l'art de travailler dans le domaine fréquentiel, c'est garanti !

Tout d'abord, pourquoi aimons-nous regarder les signaux dans le domaine fréquentiel ? Eh bien, voici deux exemples de signaux, affichés à la fois dans le domaine temporel et fréquentiel.

.. image:: ../_images/time_and_freq_domain_example_signals.png
   :scale: 40 %
   :align: center   

Comme vous pouvez le voir, dans le domaine temporel, ils ressemblent tous les deux à du bruit, mais dans le domaine fréquentiel, nous pouvons voir différentes caractéristiques. Tout est dans le domaine temporel sous sa forme naturelle ; lorsque nous échantillonnons des signaux, nous les échantillonnons dans le domaine temporel, car vous ne pouvez pas *directement* échantillonner un signal dans le domaine fréquentiel. Mais les choses intéressantes se produisent généralement dans le domaine fréquentiel.

***************
Fourier Series
***************

Les bases du domaine fréquentiel commencent par comprendre que tout signal peut être représenté par des ondes sinusoïdales additionnées. Lorsque nous décomposons un signal en ses ondes sinusoïdales composites, nous l'appelons une série de Fourier. Voici un exemple de signal composé de seulement deux ondes sinusoïdales :

.. image:: ../_images/summing_sinusoids.svg
   :align: center
   :target: ../_images/summing_sinusoids.svg
   
Voici un autre exemple; la courbe rouge ci-dessous se rapproche d'une onde en dents de scie en additionnant jusqu'à 10 ondes sinusoïdales. Nous pouvons voir que ce n'est pas une reconstruction parfaite - il faudrait un nombre infini d'ondes sinusoïdales pour reproduire cette onde en dents de scie en raison des transitions nettes :

.. image:: ../_images/fourier_series_triangle.gif
   :scale: 70 %   
   :align: center  
   
Certains signaux nécessitent plus d'ondes sinusoïdales que d'autres, et certains nécessitent une quantité infinie, bien qu'ils puissent toujours être approximés avec un nombre limité. Voici un autre exemple de signal décomposé en une série d'ondes sinusoïdales :

.. image:: ../_images/fourier_series_arbitrary_function.gif
   :scale: 70 %   
   :align: center  

Pour comprendre comment nous pouvons décomposer un signal en ondes sinusoïdales, ou sinusoïdes, nous devons d'abord passer en revue les trois attributs d'une onde sinusoïdale :

#. Amplitude
#. Phase
#. La fréquence

**Amplitude** indique la "force" de l'onde, tandis que **phase** est utilisée pour représenter la manière dont l'onde sinusoïdale est décalée dans le temps, de 0 à 360 degrés (ou de 0 à :math:`2\pi `). **Fréquence** est le nombre d'ondes par seconde.

.. image:: ../_images/amplitude_phase_period.svg
   :align: center
   :target: ../_images/amplitude_phase_period.svg
   
À ce stade, vous avez peut-être réalisé qu'un "signal" n'est essentiellement qu'une fonction, généralement représentée "dans le temps" (c'est-à-dire l'axe des x). Un autre attribut facile à retenir est la **période**, qui est l'inverse de la **fréquence**. La **période** d'une sinusoïde est le temps, en secondes, nécessaire à l'onde pour terminer un cycle. Ainsi, l'unité de fréquence est 1/seconde, ou Hz.
   
Lorsque nous décomposons un signal en une somme d'ondes sinusoïdales, chacune aura une certaine **amplitude**, **phase** et **fréquence**. L'**amplitude** de chaque onde sinusoïdale nous indiquera la force de la **fréquence** dans le signal d'origine. Ne vous inquiétez pas trop de **phase** pour l'instant, à part réaliser que la seule différence entre sin() et cos() est un déphasage (décalage temporel).

Il est plus important de comprendre le concept sous-jacent que les équations réelles à résoudre pour une série de Fourier, mais pour ceux qui sont intéressés par les équations, je vous renvoie à l'explication concise de Wolfram : https://mathworld.wolfram.com/FourierSeries.html.

***********************
Couples Temps-Fréquence
***********************

Nous avons établi que les signaux peuvent être représentés comme des ondes sinusoïdales, qui ont plusieurs attributs. Maintenant, apprenons à tracer des signaux dans le domaine fréquentiel. Alors que le domaine temporel montre comment un signal change dans le temps, le domaine fréquentiel affiche la quantité d'un signal dans quelles fréquences. Au lieu que l'axe des x soit le temps, ce sera la fréquence. Nous pouvons tracer un signal donné à la fois en temps * et * en fréquence. Regardons quelques exemples simples pour commencer.

Voici à quoi ressemble une onde sinusoïdale, de fréquence f, dans le domaine temporel et fréquentiel :

.. image:: ../_images/sine-wave.png
   :scale: 70 % 
   :align: center  

Le domaine temporel devrait vous sembler très familier. C'est une fonction oscillante. Ne vous inquiétez pas à quel moment du cycle il commence ou combien de temps il dure. Le point à retenir est que le signal a une **fréquence unique**, c'est pourquoi nous voyons un seul pic/pic dans le domaine fréquentiel. Quelle que soit la fréquence à laquelle l'onde sinusoïdale oscille, nous verrons le pic dans le domaine fréquentiel. Le nom mathématique d'un pic comme celui-ci s'appelle une "impulsion".

Et si nous avions une impulsion dans le domaine temporel ? Imaginez un enregistrement sonore de quelqu'un frappant dans ses mains ou frappant un clou avec un marteau. Ce couple temps-fréquence est un peu moins intuitif.

.. image:: ../_images/impulse.png
   :scale: 70 % 
   :align: center  

Comme nous pouvons le voir, un pic/impulsion dans le domaine temporel est plat dans le domaine fréquentiel, et théoriquement il contient toutes les fréquences. Il n'y a pas d'impulsion théoriquement parfaite car elle devrait être infiniment courte dans le domaine temporel. Comme l'onde sinusoïdale, peu importe où dans le domaine temporel l'impulsion se produit. Le point important à retenir ici est que des changements rapides dans le domaine temporel entraînent l'apparition de nombreuses fréquences.

Examinons ensuite les tracés des domaines temporel et fréquentiel d'une onde carrée :

.. image:: ../_images/square-wave.svg
   :align: center 
   :target: ../_images/square-wave.svg
   
Celui-ci est également moins intuitif, mais nous pouvons voir que le domaine fréquentiel a un fort pic à 10 Hz, qui est la fréquence de l'onde carrée, mais il semble également continuer. Cela est dû au changement rapide de domaine temporel, tout comme dans l'exemple précédent. Mais ce n'est pas plat en fréquence. Il a des pointes à intervalles réguliers et le niveau diminue lentement (bien qu'il continue indéfiniment). Une onde carrée dans le domaine temporel a un motif sin(x)/x dans le domaine fréquentiel (alias la fonction sinc).

Et si nous avions un signal constant dans le domaine temporel ? Un signal constant n'a pas de "fréquence". Voyons voir:

.. image:: ../_images/dc-signal.png
   :scale: 100 % 
   :align: center 
   
Parce qu'il n'y a pas de fréquence, dans le domaine fréquentiel, nous avons un pic à 0 Hz. Cela a du sens si vous y réfléchissez. Le domaine fréquentiel ne sera pas "vide" car cela ne se produit que lorsqu'il n'y a pas de signal présent (c'est-à-dire, domaine temporel de 0). Nous appelons 0 Hz dans le domaine fréquentiel "DC", car il est causé par un signal DC dans le temps (un signal constant qui ne change pas). Notez que si nous augmentons l'amplitude de notre signal DC dans le domaine temporel, le pic à 0 Hz dans le domaine fréquentiel augmentera également.

Plus tard, nous apprendrons ce que signifie exactement l'axe des ordonnées dans le tracé du domaine fréquentiel, mais pour l'instant, vous pouvez le considérer comme une sorte d'amplitude qui vous indique quelle quantité de cette fréquence était présente dans le signal du domaine temporel.
 
*****************
Fourier Transform
*****************

Mathématiquement, la "transformée" que nous utilisons pour passer du domaine temporel au domaine fréquentiel et inversement s'appelle la transformée de Fourier. Il est défini comme suit :

.. math::
   X(f) = \int x(t) e^{-j2\pi ft} dt

Pour un signal x(t), nous pouvons obtenir la version dans le domaine fréquentiel, X(f), en utilisant cette formule. Nous représenterons la version temporelle d'une fonction avec x(t) ou y(t), et la version fréquentielle correspondante avec X(f) et Y(f). Notez le « t » pour le temps et le « f » pour la fréquence. Le "j" est simplement l'unité imaginaire. Vous l'avez peut-être vu comme "i" en cours de mathématiques au lycée. Nous utilisons "j" en ingénierie et en informatique car "i" fait souvent référence au courant, et en programmation, il est souvent utilisé comme itérateur.

Pour revenir au domaine temporel à partir de la fréquence, c'est presque la même chose, à part un facteur d'échelle et un signe négatif :

.. math::
   x(t) = \frac{1}{2 \pi} \int X(f) e^{j2\pi ft} df

Notez que de nombreux manuels et autres ressources utilisent :math:`w` à la place de :math:`2\pi f`. :math:`w` est la fréquence angulaire en radians par seconde, tandis que :math:`f` est en Hz. Tout ce que vous devez savoir, c'est que

.. math::
   \omega = 2 \pi f

Même s'il ajoute un terme :math:`2 \pi` à de nombreuses équations, il est plus facile de s'en tenir à la fréquence en Hz. En fin de compte, vous travaillerez avec Hz dans votre application SDR.

L'équation ci-dessus pour la transformée de Fourier est la forme continue, que vous ne verrez que dans les problèmes mathématiques. La forme discrète est beaucoup plus proche de ce qui est implémenté dans le code :

.. math::
   X_k = \sum_{n=0}^{N-1} x_n e^{-\frac{j2\pi}{N}kn}
   
Notez que la principale différence est que nous avons remplacé l'intégrale par une sommation. L'indice :math:`k` va de 0 à N-1.

Ce n'est pas grave si aucune de ces équations ne signifie beaucoup pour vous. Nous n'avons en fait pas besoin de les utiliser directement pour faire des choses sympas avec DSP et SDR!

*************************
Time-Frequency Propriétés
*************************

Plus tôt, nous avons examiné des exemples de la façon dont les signaux apparaissent dans le domaine temporel et le domaine fréquentiel. Maintenant, nous allons couvrir cinq "propriétés de Fourier" importantes. Ce sont des propriétés qui nous disent si nous faisons ____ à notre signal dans le domaine temporel, alors ____ arrive à notre signal dans le domaine fréquentiel. Cela nous donnera un aperçu important du type de traitement numérique du signal (DSP) que nous effectuerons sur les signaux du domaine temporel dans la pratique.

1. Linearity Propriété:

.. math::
   a x(t) + b y(t) \leftrightarrow a X(f) + b Y(f)

Cette propriété est probablement la plus facile à comprendre. Si nous ajoutons deux signaux dans le temps, la version du domaine fréquentiel sera également les deux signaux du domaine fréquentiel additionnés. Cela nous indique également que si nous multiplions l'un ou l'autre par un facteur d'échelle, le domaine fréquentiel sera également mis à l'échelle du même montant. L'utilité de cette propriété deviendra plus évidente lorsque nous additionnerons plusieurs signaux.

2. Frequency Shift Propriété:

.. math::
   e^{2 \pi j f_0 t}x(t) \leftrightarrow X(f-f_0)

Le terme à gauche de x(t) est ce que nous appelons une "sinusoïde complexe" ou une "exponentielle complexe". Pour l'instant, tout ce que nous devons savoir, c'est qu'il s'agit essentiellement d'une onde sinusoïdale à la fréquence :math:`f_0`. Cette propriété nous dit que si nous prenons un signal :math:`x(t)` et le multiplions par une onde sinusoïdale, alors dans le domaine fréquentiel nous obtenons :math:`X(f)` sauf décalé d'une certaine fréquence, :maths:`f_0`. Ce changement de fréquence peut être plus facile à visualiser :

.. image:: ../_images/freq-shift.svg
   :align: center 
   :target: ../_images/freq-shift.svg

Le décalage de fréquence fait partie intégrante du DSP car nous voudrons décaler les signaux de haut en bas en fréquence pour de nombreuses raisons. Cette propriété nous indique comment faire cela (multiplier par une onde sinusoïdale). Voici une autre façon de visualiser cette propriété :

.. image:: ../_images/freq-shift-diagram.svg
   :align: center
   :target: ../_images/freq-shift-diagram.svg
   
3. Scaling in Time Propriété:

.. math::
   x(at) \leftrightarrow X\left(\frac{f}{a}\right)

Sur le côté gauche de l'équation, nous pouvons voir que nous mettons à l'échelle notre signal x(t) dans le domaine temporel. Voici un exemple d'un signal mis à l'échelle dans le temps, puis ce qui arrive aux versions du domaine fréquentiel de chacun.

.. image:: ../_images/time-scaling.svg
   :align: center
   :target: ../_images/time-scaling.svg

La mise à l'échelle dans le temps réduit ou étend essentiellement le signal sur l'axe des x. Ce que cette propriété nous dit, c'est que la mise à l'échelle dans le domaine temporel provoque une mise à l'échelle inverse dans le domaine fréquentiel. Par exemple, lorsque nous transmettons des bits plus rapidement, nous devons utiliser plus de fréquences. La propriété aide à expliquer pourquoi les signaux à débit de données plus élevé occupent plus de bande passante/spectre. Si la mise à l'échelle temps-fréquence était proportionnelle au lieu d'être inversement proportionnelle, les opérateurs cellulaires seraient capables de transmettre tous les bits par seconde qu'ils voulaient sans payer des milliards pour le spectre ! Malheureusement ce n'est pas le cas.

Ceux qui connaissent déjà cette propriété peuvent remarquer qu'il manque un facteur d'échelle ; il est omis par souci de simplicité. Pour des raisons pratiques, cela ne fait aucune différence.

4. Convolution in Time Propriété:

.. math::
   \int x(\tau) y(t-\tau) d\tau  \leftrightarrow X(f)Y(f)

C'est ce qu'on appelle la propriété de convolution parce que dans le domaine temporel nous convoluons x(t) et y(t). Vous ne connaissez peut-être pas encore l'opération de convolution, alors imaginez-la pour l'instant comme une corrélation croisée. Lorsque nous convoluons des signaux dans le domaine temporel, cela équivaut à multiplier les versions dans le domaine fréquentiel de ces deux signaux. C'est très différent de l'addition de deux signaux. Lorsque vous ajoutez deux signaux, comme nous l'avons vu, rien ne se passe vraiment, vous additionnez simplement la version du domaine fréquentiel. Mais lorsque vous convoluez deux signaux, c'est comme créer un nouveau troisième signal à partir d'eux. La convolution est la technique la plus importante dans DSP, bien que nous devions d'abord comprendre comment fonctionnent les filtres pour bien la saisir.

Avant de continuer, pour expliquer brièvement pourquoi cette propriété est si importante, considérez cette situation : vous avez un signal que vous souhaitez recevoir, et il y a un signal interférant à côté.

.. image:: ../_images/two-signals.svg
   :align: center
   :target: ../_images/two-signals.svg
   
Le concept de masquage est fortement utilisé en programmation, alors utilisons-le ici. Et si nous pouvions créer le masque ci-dessous et le multiplier par le signal ci-dessus afin de masquer celui que nous ne voulons pas ?

.. image:: ../_images/masking.svg
   :align: center
   :target: ../_images/masking.svg

Nous effectuons généralement des opérations DSP dans le domaine temporel, utilisons donc la propriété de convolution pour voir comment nous pouvons effectuer ce masquage dans le domaine temporel. Disons que x(t) est notre signal reçu. Soit Y(f) le masque que nous voulons appliquer dans le domaine fréquentiel. Eh bien, cela signifie que y(t) est la représentation dans le domaine temporel de notre masque, et si nous le convoluons avec x(t), nous pouvons "filtrer" le signal que nous ne voulons pas.

.. image:: ../_images/masking-equation.png
   :scale: 100 % 
   :align: center 
   
Lorsque nous discutons du filtrage, la propriété de convolution aura plus de sens.

5. Convolution in Frequency Propriété:

Enfin, je tiens à souligner que la propriété de convolution fonctionne à l'envers, même si nous ne l'utiliserons pas autant que la convolution dans le domaine temporel :

.. math::
   x(t)y(t)  \leftrightarrow  \int X(g) Y(f-g) dg

Il existe d'autres propriétés, mais les cinq ci-dessus sont les plus cruciales à comprendre à mon avis. Même si nous n'avons pas parcouru la preuve pour chaque propriété, le fait est que nous utilisons les propriétés mathématiques pour avoir un aperçu de ce qui arrive aux signaux réels lorsque nous effectuons une analyse et un traitement. Ne vous laissez pas prendre aux équations. Assurez-vous de bien comprendre la description de chaque propriété.


******************************
Fast Fourier Transform (FFT)
******************************

Revenons maintenant à la transformée de Fourier. Je vous ai montré l'équation de la transformée de Fourier discrète, mais ce que vous utiliserez lors du codage 99,9 % du temps sera la fonction FFT, fft(). La transformée de Fourier rapide (FFT) est simplement un algorithme pour calculer la transformée de Fourier discrète. Il a été développé il y a des décennies, et même s'il existe des variations dans l'implémentation, il reste le leader en titre pour le calcul d'une transformée de Fourier discrète. Heureusement, étant donné qu'ils ont utilisé "Fast" dans le nom.

La FFT est une fonction à une entrée et une sortie. Il convertit un signal de temps en fréquence :

.. image:: ../_images/fft-block-diagram.svg
   :align: center
   :target: ../_images/fft-block-diagram.svg
   
Nous ne traiterons que des FFT à 1 dimension dans ce manuel (la 2D est utilisée pour le traitement d'images et d'autres applications). Pour nos besoins, considérons la fonction FFT comme ayant une entrée : un vecteur d'échantillons et une sortie : la version dans le domaine fréquentiel de ce vecteur d'échantillons. La taille de la sortie est toujours la même que la taille de l'entrée. Si j'introduis 1 024 échantillons dans la FFT, j'en sortirai 1 024. La partie déroutante est que la sortie sera toujours dans le domaine fréquentiel, et donc la "portée" de l'axe des x si nous devions le tracer ne change pas en fonction du nombre d'échantillons dans l'entrée du domaine temporel. Visualisons cela en examinant les tableaux d'entrée et de sortie, ainsi que les unités de leurs indices :

.. image:: ../_images/fft-io.svg
   :align: center
   :target: ../_images/fft-io.svg

Étant donné que la sortie est dans le domaine fréquentiel, l'étendue de l'axe des x est basée sur la fréquence d'échantillonnage, que nous aborderons au chapitre suivant. Lorsque nous utilisons plus d'échantillons pour le vecteur d'entrée, nous obtenons une meilleure résolution dans le domaine fréquentiel (en plus de traiter plus d'échantillons à la fois). Nous ne "voyons" pas réellement plus de fréquences en ayant une entrée plus grande. Le seul moyen serait d'augmenter le taux d'échantillonnage (diminuer la période d'échantillonnage :math:`\Delta t`).

Comment traçons-nous réellement cette sortie ? A titre d'exemple, disons que notre taux d'échantillonnage était de 1 million d'échantillons par seconde (1 MHz). Comme nous l'apprendrons au chapitre suivant, cela signifie que nous ne pouvons voir que des signaux jusqu'à 0,5 MHz, quel que soit le nombre d'échantillons que nous alimentons dans la FFT. La façon dont la sortie de la FFT est représentée est la suivante :

.. image:: ../_images/negative-frequencies.svg
   :align: center
   :target: ../_images/negative-frequencies.svg

C'est toujours le cas; la sortie de la FFT affichera toujours :math:`\text{-} f_s/2` à :math:`f_s/2` où :math:`f_s` est la fréquence d'échantillonnage. C'est-à-dire que la sortie aura toujours une partie négative et une partie positive. Si l'entrée est complexe, les parties négatives et positives seront différentes, mais si elles sont réelles, elles seront identiques.

En ce qui concerne l'intervalle de fréquence, chaque bin correspond à :math:`f_s/N` Hz, c'est-à-dire que l'alimentation de plus d'échantillons à chaque FFT conduira à une résolution plus granulaire de votre sortie. Un détail très mineur qui peut être ignoré si vous êtes nouveau : mathématiquement, le tout dernier index ne correspond pas *exactement* à :math:`f_s/2`, c'est plutôt :math:`f_s/2 - f_s/N` qui pour un grand :math:`N` sera approximativement :math:`f_s/2`.

********************
Fréquences négatives
********************

Qu'est-ce qu'une fréquence négative ? Pour l'instant, sachez simplement qu'ils ont à voir avec l'utilisation de nombres complexes (nombres imaginaires) - il n'y a pas vraiment de "fréquence négative", c'est juste une représentation que nous utilisons. Voici une façon intuitive d'y penser. Considérons que nous disons à notre SDR de se régler sur 100 MHz (la bande radio FM) et d'échantillonner à une fréquence de 10 MHz. En d'autres termes, nous verrons le spectre de 95 MHz à 105 MHz. Il y a peut-être trois signaux présents :

.. image:: ../_images/negative-frequencies2.svg
   :align: center
   :target: ../_images/negative-frequencies2.svg
   
Lorsque le SDR nous donnera les échantillons, il apparaîtra comme ceci :

.. image:: ../_images/negative-frequencies3.svg
   :align: center
   :target: ../_images/negative-frequencies3.svg

Rappelez-vous que nous avons réglé le SDR sur 100 MHz. Ainsi, le signal qui était à environ 97,5 MHz apparaît à -2,5 MHz, qui est une fréquence négative. En réalité, c'est juste une fréquence inférieure à la fréquence centrale. Cela aura plus de sens lorsque nous en apprendrons davantage sur l'échantillonnage et utiliserons nos SDR.

******************************************
L'ordre dans le temps n'a pas d'importance
******************************************
Une dernière propriété avant de sauter dans les FFT. La fonction FFT "mélange autour" le signal d'entrée pour former la sortie, qui a une échelle et des unités différentes. Nous ne sommes plus dans le domaine temporel après tout. Un bon moyen d'internaliser cette différence entre les domaines consiste à réaliser que le fait de changer l'ordre dans lequel les événements se produisent dans le domaine temporel ne modifie pas les composantes de fréquence du signal. C'est-à-dire que la FFT des deux signaux suivants aura les deux mêmes pics car le signal n'est que deux ondes sinusoïdales à des fréquences différentes. Changer l'ordre dans lequel les ondes sinusoïdales se produisent ne change pas le fait qu'il s'agit de deux ondes sinusoïdales à des fréquences différentes.

.. image:: ../_images/fft_signal_order.png
   :scale: 50 % 
   :align: center 
   
Techniquement, la phase de la FFT va changer à cause du décalage temporel des sinusoïdes ; cependant, 99% du temps, nous ne nous préoccupons que de l'ampleur de la FFT, comme nous l'apprendrons bientôt.
   
*******************
FFT in Python
*******************

Maintenant que nous avons appris ce qu'est une FFT et comment la sortie est représentée, regardons en fait du code Python et utilisons la fonction FFT de Numpy, np.fft.fft(). Il est recommandé d'utiliser une console/IDE Python complète sur votre ordinateur, mais à la rigueur, vous pouvez utiliser la console Python en ligne liée au bas de la barre de navigation à gauche.

Nous devons d'abord créer un signal dans le domaine temporel. N'hésitez pas à suivre avec votre propre console Python. Pour simplifier les choses, nous allons faire une simple onde sinusoïdale à 0,15 Hz. Nous utiliserons également une fréquence d'échantillonnage de 1 Hz, ce qui signifie que nous échantillonnons dans le temps à 0, 1, 2, 3 secondes, etc.

.. code-block:: python

 import numpy as np
 t = np.arange(100)
 s = np.sin(0.15*2*np.pi*t)

Si nous traçons s, cela ressemble à :

.. image:: ../_images/fft-python1.png
   :scale: 70 % 
   :align: center 

Utilisons ensuite la fonction FFT de Numpy :

.. code-block:: python

 S = np.fft.fft(s)

Si nous regardons S, nous voyons qu'il s'agit d'un tableau de nombres complexes :

.. code-block:: python

    S =  array([-0.01865008 +0.00000000e+00j, -0.01171553 -2.79073782e-01j,0.02526446 -8.82681208e-01j,  3.50536075 -4.71354150e+01j, -0.15045671 +1.31884375e+00j, -0.10769903 +7.10452463e-01j, -0.09435855 +5.01303240e-01j, -0.08808671 +3.92187956e-01j, -0.08454414 +3.23828386e-01j, -0.08231753 +2.76337148e-01j, -0.08081535 +2.41078885e-01j, -0.07974909 +2.13663710e-01j,...

Astuce : quoi que vous fassiez, si jamais vous rencontrez des nombres complexes, essayez de calculer la magnitude et la phase et voyez s'ils ont plus de sens. Faisons exactement cela, et traçons la magnitude et la phase. Dans la plupart des langages, abs() est une fonction de magnitude d'un nombre complexe. La fonction de phase varie, mais en Python c'est :code:`np.angle()`.

.. code-block:: python

 import matplotlib.pyplot as plt
 S_mag = np.abs(S)
 S_phase = np.angle(S)
 plt.plot(t,S_mag,'.-')
 plt.plot(t,S_phase,'.-')

.. image:: ../_images/fft-python2.png
   :scale: 80 % 
   :align: center 

À l'heure actuelle, nous ne fournissons aucun axe x aux tracés, c'est juste l'index du tableau (en partant de 0). Pour des raisons mathématiques, la sortie de la FFT a le format suivant :

.. image:: ../_images/fft-python3.svg
   :align: center
   :target: ../_images/fft-python3.svg
   
Mais nous voulons 0 Hz (DC) au centre et des fréquences négatives à gauche (c'est comme ça que nous aimons visualiser les choses). Donc, chaque fois que nous faisons une FFT, nous devons effectuer un "décalage FFT", qui est juste une simple opération de réarrangement de tableau, un peu comme un décalage circulaire mais plus un "mettre ceci ici et cela là". Le schéma ci-dessous définit pleinement ce que fait l'opération de décalage FFT :

.. image:: ../_images/fft-python4.svg
   :align: center
   :target: ../_images/fft-python4.svg

Pour notre commodité, Numpy a une fonction de décalage FFT, :code:`np.fft.fftshift()`. Remplacez la ligne np.fft.fft() par :

.. code-block:: python

 S = np.fft.fftshift(np.fft.fft(s))

Nous devons également déterminer les valeurs/étiquettes de l'axe des x. Rappelez-vous que nous avons utilisé une fréquence d'échantillonnage de 1 Hz pour simplifier les choses. Cela signifie que le bord gauche du tracé du domaine fréquentiel sera de -0,5 Hz et le bord droit sera de 0,5 Hz. Si cela n'a pas de sens, il le sera après avoir lu le chapitre sur :ref:`sampling-chapter`. Tenons-nous en à cette hypothèse selon laquelle notre fréquence d'échantillonnage était de 1 Hz et traçons l'amplitude et la phase de la sortie FFT avec une étiquette d'axe x appropriée. Voici la version finale de cet exemple Python et le résultat :

.. code-block:: python

 import numpy as np
 import matplotlib.pyplot as plt
 
 Fs = 1 # Hz
 N = 100 # number of points to simulate, and our FFT size
 
 t = np.arange(N) # because our sample rate is 1 Hz
 s = np.sin(0.15*2*np.pi*t)
 S = np.fft.fftshift(np.fft.fft(s))
 S_mag = np.abs(S)
 S_phase = np.angle(S)
 f = np.arange(Fs/-2, Fs/2, Fs/N)
 plt.figure(0)
 plt.plot(f, S_mag,'.-')
 plt.figure(1)
 plt.plot(f, S_phase,'.-')
 plt.show()

.. image:: ../_images/fft-python5.png
   :scale: 80 % 
   :align: center 

Notez que nous voyons notre pic à 0,15 Hz, qui est la fréquence que nous avons utilisée lors de la création de l'onde sinusoïdale. Cela signifie donc que notre FFT a fonctionné ! Si nous ne connaissions pas le code utilisé pour générer cette onde sinusoïdale, mais que nous venions de recevoir la liste des échantillons, nous pourrions utiliser la FFT pour déterminer la fréquence. La raison pour laquelle nous voyons un pic également à -0,15 Hz est liée au fait qu'il s'agissait d'un signal réel, pas complexe, et nous approfondirons cela plus tard.

******************************
Windowing
******************************

Lorsque nous utilisons une FFT pour mesurer les composantes de fréquence de notre signal, la FFT suppose qu'il reçoit un morceau d'un signal *périodique*. Il se comporte comme si le morceau de signal que nous avons fourni continuait à se répéter indéfiniment. C'est comme si le dernier échantillon de la tranche se reconnectait au premier échantillon. Il découle de la théorie de la transformée de Fourier. Cela signifie que nous voulons éviter les transitions soudaines entre le premier et le dernier échantillon car les transitions soudaines dans le domaine temporel ressemblent à de nombreuses fréquences et, en réalité, notre dernier échantillon ne se connecte pas réellement à notre premier échantillon. Pour faire simple : si nous faisons une FFT de 100 échantillons, en utilisant :code:`np.fft.fft(x)`, nous voulons :code:`x[0]` et :code:`x[99] ` pour être égal ou proche en valeur.

La façon dont nous compensons cette propriété cyclique est par le "fenêtrage". Juste avant la FFT, nous multiplions la tranche de signal par une fonction de fenêtre, qui est n'importe quelle fonction qui se rétrécit à zéro aux deux extrémités. Cela garantit que la tranche de signal commencera et se terminera à zéro et se connectera. Les fonctions de fenêtre courantes incluent Hamming, Hanning, Blackman et Kaiser. Lorsque vous n'appliquez aucun fenêtrage, cela s'appelle utiliser une fenêtre "rectangulaire" car c'est comme multiplier par un tableau de uns. Voici à quoi ressemblent plusieurs fonctions de fenêtre :

.. image:: ../_images/windows.svg
   :align: center
   :target: ../_images/windows.svg

Une approche simple pour les débutants consiste à simplement s'en tenir à une fenêtre de Hamming, qui peut être créée en Python avec :code:`np.hamming(N)` où N est le nombre d'éléments dans le tableau, qui est votre taille FFT. Dans l'exercice ci-dessus, nous appliquerions la fenêtre juste avant la FFT. Après la 2ème ligne de code, nous insérerions :

.. code-block:: python

 s = s * np.hamming(100)

Si vous avez peur de choisir la mauvaise fenêtre, ne le soyez pas. La différence entre Hamming, Hanning, Blackman et Kaiser est très minime par rapport au fait de ne pas utiliser de fenêtre du tout, car ils se réduisent tous à zéro des deux côtés et résolvent le problème sous-jacent.


*******************
FFT Sizing
*******************

La dernière chose à noter est le dimensionnement FFT. La meilleure taille de FFT est toujours d'ordre 2 en raison de la manière dont la FFT est implémentée. Vous pouvez utiliser une taille qui n'est pas de l'ordre de 2, mais ce sera plus lent. Les tailles courantes se situent entre 128 et 4 096, bien que vous puissiez certainement aller plus loin. En pratique, nous devrons peut-être traiter des signaux longs de millions ou de milliards d'échantillons, nous devons donc décomposer le signal et effectuer de nombreuses FFT. Cela signifie que nous obtiendrons de nombreuses sorties. Nous pouvons soit les calculer en moyenne, soit les tracer dans le temps (en particulier lorsque notre signal change dans le temps). Vous n'avez pas besoin de mettre * chaque * échantillon d'un signal dans une FFT pour obtenir une bonne représentation dans le domaine fréquentiel de ce signal. Par exemple, vous ne pouvez FFT que 1 024 échantillons sur 100 000 dans un signal et cela aura probablement l'air correct, tant que le signal est toujours activé.

*********************
Spectrogram/Waterfall
*********************

Un spectrogramme est le graphique qui montre la fréquence dans le temps. Il s'agit simplement d'un tas de FFT empilées (verticalement, si vous voulez une fréquence sur l'axe horizontal). Nous pouvons également le montrer en temps réel, souvent appelé cascade. Un analyseur de spectre est l'équipement qui affiche ce spectrogramme/cascade. Voici un exemple de spectrogramme, avec la fréquence sur l'axe horizontal/x et le temps sur l'axe vertical/y. Le bleu représente l'énergie la plus faible et le rouge la plus élevée. Nous pouvons voir qu'il y a une forte pointe à DC (0 Hz) au centre avec un signal variable autour de lui. Le bleu représente notre plancher de bruit.

.. image:: ../_images/waterfall.png
   :scale: 120 % 
   :align: center 

Comme exercice, essayez d'écrire le code Python nécessaire pour produire un spectrogramme. N'oubliez pas qu'il ne s'agit que de rangées de FFT empilées les unes sur les autres, chaque rangée correspond à 1 FFT. Assurez-vous de trancher dans le temps votre signal d'entrée en tranches de la taille de votre FFT (par exemple, 1024 échantillons par tranche). Pour garder les choses simples, vous pouvez entrer un signal réel et simplement jeter la moitié négative des fréquences avant de tracer le spectrogramme. Voici un exemple de signal que vous pouvez utiliser, c'est simplement une tonalité dans un bruit blanc :

.. code-block:: python

 import numpy as np
 import matplotlib.pyplot as plt
 
 sample_rate = 1e6
 
 # Generate tone plus noise
 t = np.arange(1024*1000)/sample_rate # time vector
 f = 50e3 # freq of tone
 x = np.sin(2*np.pi*f*t) + 0.2*np.random.randn(len(t))

Voici à quoi cela ressemble dans le domaine temporel (first 200 samples) :

.. image:: ../_images/spectrogram_time.svg
   :align: center
   :target: ../_images/spectrogram_time.svg

.. raw:: html

   <details>
   <summary>Example spectrogram code (try to write it yourself first!)</summary>

.. code-block:: python

 # simulate the signal above, or use your own signal
  
 fft_size = 1024
 num_rows = int(np.floor(len(x)/fft_size))
 spectrogram = np.zeros((num_rows, fft_size))
 for i in range(num_rows):
     spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)
 spectrogram = spectrogram[:,fft_size//2:] # get rid of negative freqs because we simulated a real signal
 
 plt.imshow(spectrogram, aspect='auto', extent = [0, sample_rate/2/1e6, 0, len(x)/sample_rate])
 plt.xlabel("Frequency [MHz]")
 plt.ylabel("Time [s]")
 plt.show()

Ce qui devrait produire le spectrogramme suivant, qui n'est pas le plus intéressant car il n'y a pas de comportement variant dans le temps. Comme exercice supplémentaire, essayez d'ajouter un comportement variant dans le temps, par exemple, voyez si vous pouvez faire démarrer et arrêter la tonalité.

.. image:: ../_images/spectrogram.svg
   :align: center
   :target: ../_images/spectrogram.svg
   
.. raw:: html

   </details>


