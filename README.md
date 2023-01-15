# PySDR Textbook
<p align="center">
  <img src="https://raw.githubusercontent.com/777arc/textbook/master/_images/fft_logo_wide.gif" width="350"/>
</p>
This repo contains the source content used to generate my textbook, __PySDR: A Guide to SDR and DSP using Python__ , hosted at www.pysdr.org.

Feel free to submit an issue, or even a Pull Request (PR) with fixes or improvements.  Those who submit valuable feedback/fixes be permanently added to the acknowledgments section.  Not good at Git but have changes to suggest?  Feel free to email me at pysdr@vt.edu.

## Building:

On windows (this wont include the French version):

```
sphinx-build -b html -D imgmath_latex="C:\Program Files\MiKTeX 2.9\miktex\bin\x64\latex.exe" . _build
```

On Ubuntu with *latest* sphinx via apt-get (3.2.1 at the time of this writing) installed with pip, I had to add ~/.local/bin to PATH, and apt-get install texlive-latex-extra.  Also after dutch version was added I needed `apt-get install -y pdf2svg` and `pip install sphinxcontrib-tikz`.

```bash
sphinx-build -b html . _build
sphinx-build -b html -D exclude_patterns=_build,index.rst,content/* -D master_doc=index-fr . _build/fr/
make html-nl
```

## Getting pdf created (not working yet due to gifs)

```
sudo apt-get install -y latexmk
sphinx-build -b latex . _build/latex
make latexpdf
NEED TO REMOVE ALL GIFS FOR IT TO NOT ERROR OUT
``

## Misc

Ideas for future chapters:

* Equalization, would be the last step needed to finish the end-to-end comms link
* Cyclostationary analysis
* OFDM, simulating OFDM and CP, show via Python how it turns freq selective fading into flat fading
* How to create real-time SDR apps with GUIs in Python using pyqt and pyqtgraph, or even just matplotlib with updating
* Python code that lets the Pluto (or RTL-SDR) act as an FM receiver, like with sound output
* End to end example that shows how to detect start of packet and other concepts not covered in RDS chapter

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.
