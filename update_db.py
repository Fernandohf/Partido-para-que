"""
This file evokes the API ListaSenadorService e atualiza os banco de dados
com os atuais políticos e seus históricos de votação.
O link da API: http://legis.senado.leg.br/dadosabertos/docs/ui/index.html
               http://legis.senado.leg.br/dadosabertos/docs/resource_PlenarioService.html#resource_PlenarioService_listaVotacoesSessaoXml_GET
70/votacoes?ano=2018
"""
import sqlite3
import requests


class DatabaseUpdater():
    """
    Class that controlls the database updating and retrieving information.
    """

    def __init__(self, nome='database.db'):
        # File name of the updater
        self.file_name = nome
    
    def update_senator_tables(self):
        """"
        Updates the Senator's and Partidos' table in the DB.
        """
        # Get data in json format
        url_curr = ("http://legis.senado.leg.br/dadosabertos/senador" +
                    "/lista/atual")
        header = {'Accept': 'application/json'}
        response = requests.get(url_curr, headers=header)
        data_json = response.json()
        data_parsed = []

        # Search for Senators information
        parlamentares = (data_json["ListaParlamentarEmExercicio"]
                         ["Parlamentares"]["Parlamentar"])

        # For each senator
        for senator in parlamentares:
            identification = senator["IdentificacaoParlamentar"]
            cod = int(identification["CodigoParlamentar"])
            nome = identification["NomeCompletoParlamentar"]
            sexo = identification["SexoParlamentar"]
            estado = identification["UfParlamentar"]
            partido = identification["SiglaPartidoParlamentar"]
            data_parsed.append((cod, nome, sexo, estado, partido))

        # Creates DB connection
        conn = sqlite3.connect(self.file_name)
        db_cursor = conn.cursor()

        # Saves the data
        db_cursor.executemany("INSERT INTO Senadores VALUES (?,?,?,?,?)",
                              data_parsed)

        # Commites the changes abd closes the connection
        conn.commit()
        conn.close()

    def update_votes_table(self):
        """
        Updates the votes table. OBS.: SLOW!!
        """
        # Get data in json format
        url_curr = ("http://legis.senado.leg.br/dadosabertos/senador" +
                    "/lista/atual")
        header = {'Accept': 'application/json'}
        response = requests.get(url_curr, headers=header)
        data_json = response.json()
        data_parsed = []

        # Search for Senators information
        parlamentares = (data_json["ListaParlamentarEmExercicio"]
                         ["Parlamentares"]["Parlamentar"])

        # For each senator
        for senator in parlamentares:
            identification = senator["IdentificacaoParlamentar"]
            cod = int(identification["CodigoParlamentar"])
            nome = identification["NomeCompletoParlamentar"]
            sexo = identification["SexoParlamentar"]
            estado = identification["UfParlamentar"]
            partido = identification["SiglaPartidoParlamentar"]
            data_parsed.append((cod, nome, sexo, estado, partido))

        # Creates DB connection
        conn = sqlite3.connect(self.file_name)
        db_cursor = conn.cursor()

        # Saves the data
        db_cursor.executemany("INSERT INTO Senadores VALUES (?,?,?,?,?)",
                              data_parsed)

        # Commites the changes abd closes the connection
        conn.commit()
        conn.close()        



