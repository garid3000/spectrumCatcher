# spectrumCatcher
This is a Python library for downloading &amp; analyzing Spectrum Catcher Data with Python.

[PYPI](https://pypi.org/project/spectrumCatcher/)


# Installation
1. option 1:
``` pip install spectrumCatcher ```

2. option 1: (after download this repo and extract)
```python setup.py install```
3. option 2: (after download this repo and extract)
```pip install dist/spectrumCathcer-0.1.0-py3-none-any.whl```


# Usage
## Downloading:
```
>>> from spectrumCatcher import downloader
>>> d = downloader.Downloader("username", "password", "2020-03-26","path/for/downloaded/data")
>>> d.processHTML()
>>> d.download_all()
```


## Copying Data Directly from Phone
```
>>>
```
