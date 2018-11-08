"""
This file evokes the API ListaSenadorService e atualiza os banco de dados
com os atuais políticos e seus históricos de votação.
O link da API: http://legis.senado.leg.br/dadosabertos/docs/ui/index.html
               http://legis.senado.leg.br/dadosabertos/docs/resource_PlenarioService.html#resource_PlenarioService_listaVotacoesSessaoXml_GET
70/votacoes
Legenda: 
MIS-Presente(art.40 - em Missão)
P-NRV-Presente-Não registrou voto
P-OD-Presente(obstrução declarada)
REP-Presente(art.67/13 - em Representação da Casa)
Ncom - Não compareceu
AP-art.13, caput-Atividade política/cultural
LA-art.43, §6º-Licença à adotante
LAP-art.43, §7º-Licença paternidade ou ao adotante
LC - art.44-A-Candidatura à Presidência/Vice-Presidência
LS - Licença saúde
LG - art.43, §5-Licença à gestante
NA-dispositivo não citado
"""
import sqlite3
import warnings
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
        for i, senator in enumerate(parlamentares):
            senator_info = senator["IdentificacaoParlamentar"]
            s_id = i + 1
            cod = int(senator_info["CodigoParlamentar"])
            nome = senator_info["NomeCompletoParlamentar"]
            sexo = senator_info["SexoParlamentar"]
            estado = senator_info["UfParlamentar"]
            partido = senator_info["SiglaPartidoParlamentar"]
            data_parsed.append((s_id, cod, nome, sexo, estado, partido))

        # Creates DB connection
        conn = sqlite3.connect(self.file_name)
        db_cursor = conn.cursor()

        # Saves the data
        db_cursor.executemany("INSERT OR IGNORE INTO Senadores (SenadorID, " +
                              "SenadorCod, NomeCompleto, Sexo, Estado," +
                              " PartidoSigla) VALUES (?,?,?,?,?,?)",
                              data_parsed)

        # Commites the changes abd closes the connection
        conn.commit()
        conn.close()

    def update_votes_table(self, year_considered=('2018', '2017', '2016')):
        """
        Updates the votes table. OBS.: SLOW!!
        """

        # Basic url and header
        url_votes = "http://legis.senado.leg.br/dadosabertos/senador/"
        header = {'Accept': 'application/json'}

        # Creates DB connection
        conn = sqlite3.connect(self.file_name)
        db_cursor = conn.cursor()

        # Get each senator code
        db_cursor.execute("SELECT SenadorID FROM Senadores")
        senators_code = db_cursor.fetchall()
        conn.close()

        # Data placeholder
        data_parsed = []
        counter = 0
        # For each senator
        for senator_id in senators_code:
            # Senator id
            senator_info = senator_id[0]

            # Search url
            url_senator = (url_votes + str(senator_info) +
                           "/votacoes")

            # API response
            response = requests.get(url_senator, headers=header)
            data_json = response.json()

            # List of votes sessions
            try:
                sessions = (data_json["VotacaoParlamentar"]
                            ["Parlamentar"]["Votacoes"]["Votacao"])
            except KeyError:
                warnings.warn("Sessão nenhuma votação encontrada" +
                              "para o parlamenta de código " +
                              str(senator_info))
                continue

            # For each non-secret vote session
            for vote in sessions:
                session_not_secret = vote["IndicadorVotacaoSecreta"] == "Não"
                if session_not_secret:
                    # Year of the session
                    year = vote["SessaoPlenaria"]["DataSessao"].split("-")[0]
                    if year in year_considered:
                        # Session id and vote
                        session_id = int(vote["SessaoPlenaria"]
                                         ["CodigoSessao"])
                        vote = vote["DescricaoVoto"]
                        data_parsed.append((counter, senator_info,
                                            session_id, vote))
                        counter += 1

        # Creates DB connection
        conn = sqlite3.connect(self.file_name)
        db_cursor = conn.cursor()

        # Saves the data
        db_cursor.executemany("INSERT OR IGNORE INTO votos (VotoID," +
                              "SenadorID, SessaoID, Voto) VALUES (?,?,?,?)",
                              data_parsed)

        # Commites the changes and closes the connection
        conn.commit()
        conn.close()


DBU = DatabaseUpdater()
DBU.update_senator_tables()
DBU.update_votes_table()
