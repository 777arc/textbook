sphinx-build -b html . _build
sphinx-build -b html -D exclude_patterns=_build,index.rst,content/* -D master_doc=index-fr . _build/fr/
