[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# COVID-19 Global Response

This repository contains code for data acquisition, preprocessing, and analysis for the COVID-19 global response paper.

## Contents

### `01-code-scripts/`

Contains all code used in data acquisition, preprocessing, and analysis.

* `download-ges-order.py`: Download a GES DISC web order. Used to acquire nitrogen dioxide and carbon monoxide data.
* `download-laads-order.py`: Download a LAADS web order. Used to acquire nighttime lights data.

### `environment-py37.yml`

Contains information required to create the Conda environment for preprocessing VIIRS data, using Python 3.7.6.

### `environment-py37.yml`

Contains information required to create the Conda environment for all other data acquisition and preprocessing scripts, using Python 3.8.10.
