[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# COVID-19 Global Response

This repository contains code for data acquisition, preprocessing, and analysis for the COVID-19 global response paper.

## Contents

### `01-code-scripts/`

Contains all code used in data acquisition, preprocessing, and analysis.

* `clip-rasters.py`: Clips GeoTiff files to a defined areas of interest. Used to clip OMI/Aura nitrogen dioxide and Aqua/AIRS carbon monoxide data.
* `download-ges-order.py`: Download a GES DISC web order. Used to acquire OMI/Aura nitrogen dioxide and Aqua/AIRS carbon monoxide data.
* `download-laads-order.py`: Download a LAADS web order. Used to acquire VIIRS nighttime lights data.
* `mosaic-and-clip-rasters.py`: Mosaicks and clips GeoTiff files. Used to mosaick and clip VIIRS nighttime lights data.
* `mosaics.py`: Module containing a function used while mosaicking VIIRS nighttime lights data.
* `preprocess-nitrogen-dioxide.py`: Preprocess OMI/Aura nitrogen dioxide data.
* `preprocess-carbon-monoxide.py`: Preprocess Aqua/AIRS carbon monoxide data.
* `preprocess-nighttime-lights.py`: Preprocess VIIRS nighttime lights data.
* `viirs.py`: Module containing functions for preprocessing VIIRS nighttime lights data.

### `environment-py37.yml`

Contains information required to create the Conda environment for preprocessing VIIRS nighttime lights data, using Python 3.7.6.

### `environment-py38.yml`

Contains information required to create the Conda environment for all other data acquisition and preprocessing tasks, using Python 3.8.10.
