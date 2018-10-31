"""
This file evokes the API ListaSenadorService e atualiza os banco de dados com os atuais políticos e seus históricos de votação.
O link da API: http://legis.senado.leg.br/dadosabertos/docs/ui/index.html
"""
import sqlite3
import requests
import objectpath


def update_current_senators():
    """"
    Updates the DB with the curret senators of Brazil.
    """
    # Get data in json format
    url_curr = "http://legis.senado.leg.br/dadosabertos/senador/lista/atual"
    header = {'Accept': 'application/json'}
    r = requests.get(url_curr, headers=header)
    data_json = r.json()
    
    # Search for Senators information
    parlamentares = []
    id = 
    query_names = "$"
    quer
    names = tree.execute()

    # Creates DB connection e execution
    conn = sqlite3.connect("database.db")    
    c = conn.cursor()

    # Saves the data

update_current_senators()

