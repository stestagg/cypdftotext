# cypdftotext

[![PyPI Status](https://img.shields.io/pypi/v/pdftotext.svg)](https://pypi.python.org/pypi/pdftotext)
[![Travis Status](https://api.travis-ci.com/jalan/pdftotext.svg?branch=master)](https://travis-ci.com/jalan/pdftotext)
[![AppVeyor status](https://ci.appveyor.com/api/projects/status/uwcjxgu31kirkiuj/branch/master?svg=true)](https://ci.appveyor.com/project/jalan/pdftotext/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/jalan/pdftotext/badge.svg?branch=master)](https://coveralls.io/github/jalan/pdftotext?branch=master)
[![Downloads](https://img.shields.io/pypi/dm/pdftotext.svg)](https://pypistats.org/packages/pdftotext)

Cython port of pdftotext - A Simple PDF text extraction library

```python
import pdftotext

# Load your PDF
with open("lorem_ipsum.pdf", "rb") as f:
    pdf = pdftotext.PDF(f.read())

# How many pages?
print(len(pdf))

# Iterate over all the pages
for page in pdf:
    print(page)

# Read some individual pages
print(pdf[0])
print(pdf[1])

# Read all the text into one string
print("\n\n".join(pdf))
```

## Install

```
pip install pdftotext-cython
```
