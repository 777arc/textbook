# PySDR Textbook

This repo contains the source content used to generate my textbook, **PySDR: A Guide to SDR and DSP using Python**, hosted at www.pysdr.org.

Feel free to submit an issue, or even a Pull Request (PR) with fixes or improvements.  Those who submit valuable feedback/fixes be permanently added to the acknowledgments section.  Not good at Git but have changes to suggest?  Feel free to email me at pysdr@vt.edu.

## Notes to self:

to build on windows:

sphinx-build -b html -D imgmath_latex="C:\Program Files\MiKTeX 2.9\miktex\bin\x64\latex.exe" . _build

On Ubuntu with *latest* sphinx via apt-get (3.2.1 at the time of this writing) installed with pip, I had to add ~/.local/bin to PATH, and apt-get install texlive-latex-extra:

sphinx-build -b html . _build

chapter name references, for my reference when writing:

* sampling-chapter
* pulse-shaping-chapter
* pluto-chapter
* pluto-adv-chapter
* multipath-chapter
* noise-chapter
* modulation-chapter
* link-budgets-chapter
* iq-files-chapter
* noise-chapter
* intro-chapter
* freq-domain-chapter
* filters-chapter
* channel-coding-chapter
