# Bibtex Scraper

Scrape bibtex from websites such as Microsoft Academic, Core (TODO), Base (TODO).

Usage:
```python
from bibtex_scraper import query
bibtex_entry = query('Dropout: a simple way to prevent neural networks from overfitting')

"""
bibtex_entry: ['@article{srivastava2014dropout,\n\ttitle="Dropout: a simple way to prevent
neural networks from overfitting",\n\tauthor="Nitish {Srivastava} and Geoffrey E. {Hinton}
and Alex {Krizhevsky} and Ilya {Sutskever} and Ruslan R. {Salakhutdinov}",\n\tjournal=
"Journal of Machine Learning Research",\n\tvolume="15",\n\tnumber="1",\n\tpages="1929--1958",
\n\tyear="2014"\n}\n\n']
"""

```

This will return the bibtex of the first entry that matches the title 'Dropout: a simple way to prevent neural networks from overfitting'.


## Requirements

- Selenium
  - Firefox Gecko Driver
 

