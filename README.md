
# Partido para quê ?
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Fernandohf/Partido-para-que/master) [![GitHub license](https://img.shields.io/github/license/Fernandohf/Partido-para-que.svg?logo=GPL)](https://github.com/Fernandohf/Partido-para-que/blob/master/LICENSE)


This is a Machine Learning project that applies clustering techniques on brazilians senators voting behavior.
It contains a notebook that analyses voting behavior of brazilians congress men and women. The purpose of this notebook is to verify the necessity of 35 different parties in Brazil. Additionally, This could be used to identify independent senators and likely detect who is more open to negotiation.

## Data Source

Brazilian Senate API Docs: [http://legis.senado.leg.br/dadosabertos/docs/](http://legis.senado.leg.br/dadosabertos/docs/)

## Requirements

Libraries | Minimum Version
:---|:---:
Pandas | 0.23.4
SQLAlchemy| 1.2.14
Requests| 2.18.4
Numpy| 1.15.2
Scikit-Learn| 0.20.2

## How to Run

1. Create the conda environment with conda `conda env create -f environment.yml`.
2. Activate the environment `pt`.
3. Run the file `update_db.py`, this file update/creates the SQLite database.
4. Run the `Partido_para_que.ipynb` Notebook and follow the instructions.