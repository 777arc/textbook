# textbook

In windows, open anaconda prompt with admin rights

first time I need to do:
conda install sphinx_rtd_theme

to build on windows:

sphinx-build -b html -D imgmath_latex="C:\Program Files\MiKTeX 2.9\miktex\bin\x64\latex.exe" . _build

On Ubuntu with *latest* sphinx  (3.1.1 at the time of this writing) installed with pip:

sphinx-build -b html . _build

chapter name references, for my reference when writing:

sampling-chapter
pulse-shaping-chapter
pluto-chapter
multipath-chapter
noise-chapter
modulation-chapter
link-budgets-chapter
iq-files-chapter
noise-chapter
intro-chapter
freq-domain-chapter
filters-chapter
channel-coding-chapter
