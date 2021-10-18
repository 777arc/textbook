# PySDR Textbook
<p align="center">
  <img src="https://raw.githubusercontent.com/777arc/textbook/master/_images/fft_logo_wide.gif" width="350"/>
</p>
This repo contains the source content used to generate my textbook, **PySDR: A Guide to SDR and DSP using Python**, hosted at www.pysdr.org.

Feel free to submit an issue, or even a Pull Request (PR) with fixes or improvements.  Those who submit valuable feedback/fixes be permanently added to the acknowledgments section.  Not good at Git but have changes to suggest?  Feel free to email me at pysdr@vt.edu.

## Building:

On windows:

```
sphinx-build -b html -D imgmath_latex="C:\Program Files\MiKTeX 2.9\miktex\bin\x64\latex.exe" . _build
```

On Ubuntu with *latest* sphinx via apt-get (3.2.1 at the time of this writing) installed with pip, I had to add ~/.local/bin to PATH, and apt-get install texlive-latex-extra:

```bash
sphinx-build -b html . _build
```

## Misc

chapter name refs, for my reference when writing:

* sampling-chapter
* pulse-shaping-chapter
* pluto-chapter
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
* author-chapter

Ideas for future chapters:

* Equalization, would be the last step needed to finish the end-to-end comms link
* "Bringing it all together", discussion and Python+SDR implementation of a full receiver, perhaps ADS-B or RDS
* Cyclostationary, ask Chad if he wants to co-write it
* OFDM, simulating OFDM and CP, show via Python how it turns freq selective fading into flat fading
* How to create real-time SDR apps with GUIs in Python using pyqt and pyqtgraph, or even just matplotlib with updating
* Python code that lets the Pluto (or RTL-SDR) act as an FM receiver, like with sound output

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.
