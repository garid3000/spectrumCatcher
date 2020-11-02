# spectrumCatcher
This is a Python library for downloading &amp; analyzing Spectrum Catcher Data with Python.


# installation

option 1: (after download this repo and extract)
python setup.py install

option 2: (after download this repo and extract)
pip install dist/spectrumCathcer-0.1.0-py3-none-any.whl

option 3: (Not yet: it will uploaded into pypi)


# Usage
## Downloading:
>>> from spectrumCatcher import downloader
>>> d = downloader.Downloader("username", "password", "2020-03-26","path/for/downloaded/data")
>>> d.processHTML()
>>> d.download_all()