# textbook

In windows, open anaconda prompt with admin rights

first time I need to do:
conda install sphinx_rtd_theme

to build on windows:

sphinx-build -b html -D imgmath_latex="C:\Program Files\MiKTeX 2.9\miktex\bin\x64\latex.exe" . _build

On Ubuntu with latest sphinx installed with pip:

python3 /usr/local/lib/python3.6/dist-packages/sphinx/cmd/build.py -b html . _build
