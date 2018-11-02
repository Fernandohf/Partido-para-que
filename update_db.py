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
    # Database format
    TABLES = {"Senadores": ["SenadorID", "NomeCompleto",
                            "Sexo", "PartidoSigla"],
              "Partidos": ["PartidoID", "NomeCompleto",
                           "Sigla", "PartidoSigla"],
              "Sessoes": ["SessaoID", "Secreta", "Data",
                          "DescricaoVotacao", "Resultado"],
              "Votos": ["VotoID", "SenadorID", "SessaoID",
                        "Valor"]}
    # API Dictionary
    API_DICT = {"Senadores": {"url": "http://legis.senado.leg.br/" +
                                     "dadosabertos/senador/lista/atual",
                              "default": ["ListaParlamentarEmExercicio",
                                          "Parlamentares", "Parlamentar"],
                              "values": {"SenadorID": ["Identificacao" +
                                                       "Parlamentar",
                                                       "CodigoParlamentar"],
                                         "NomeCompleto": ["Identificacao" +
                                                          "Parlamentar",
                                                          "NomeCompleto" +
                                                          "Parlamentar"],
                                         "Sexo": ["IdentificacaoParlamentar",
                                                  "SexoParlamentar"],
                                         "PartidoSigla": ["Identificacao" +
                                                          "Parlamentar",
                                                          "SiglaPartido" +
                                                          "Parlamentar"]}},
                "Partidos": {"url": "http://legis.senado.leg.br/dadosabertos" +
                                    "/senador/partidos?indAtivos=S&v=2",
                             "default": ["ListaPartidos", "Partidos",
                                         "Partido"],
                             "values": {"PartidoID": ["Codigo"],
                                        "NomeCompleto": ["Nome"],
                                        "Sigla": ["Sigla"]}},
                "Sessao": {"url": "http://legis.senado.leg.br/dadosabertos/" +
                                  "plenario/lista/votacao/",
                           "default": ["ListaVotacoes",
                                       "Votacoes", "Votacao"],
                           "values": {"SessaoID": ["CodigoSessao"],
                                      "Secreta": ["Secreta"],
                                      "Data": ["DataSessao"],
                                      "DescricaoVotacao": ["Descricao" +
                                                           "Votacao"]}},
                "Votos": {"url": "http://legis.senado.leg.br/dadosabertos" +
                                 "/senador/",
                          "default": ["VotacaoParlamentar",
                                      "Parlamentar", "Votacoes", "Votacao"],
                          "values": {"VotoID": ["SessaoPlenaria",
                                                "CodigoSessao"],
                                     "SenadorID": ["Secreta"],
                                     "SessaoID": ["SessaoPlenaria",
                                                  "CodigoSessao"],
                                     "Voto": ["DescricaoVoto"]}}}

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



