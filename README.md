
# Partido para quê?

This is a Machine Learning project that applies clustering techniques on brazilians senators voting behavior.
A notebook that analyses voting behavior of brazilians congress men and women. The purpose of this notebook is to verify the need of 35 different parties in Brazil.

## Data Source

Brazilian Senate API: [http://legis.senado.leg.br/dadosabertos/docs/](http://legis.senado.leg.br/dadosabertos/docs/)

## Requirements

- Pandas >= 0.23.4
- SQLAlchemy >= 1.2.14
- Requests >= 2.18.4
- Numpy >= 1.15.2
- Scikit-Learn >= 0.20.2

## How to Run

1. First run the file `update_db.py`, this file update/creates the SQLLite database.
2. Run the `Partido_para_que.ipynb` Notebook and follow the instructions.