from Database.PathDatabase import PathDatabase

from MVC.model.Attività.Indirizzo import Indirizzo
from MVC.model.Attività.User import User
from MVC.model.Interfacce.attivitàInterface.AmministratoreInterface import AmministratoreInterface
from MVC.model.Servizio.Categoria import Categoria
from MVC.model.Servizio.Prodotto import Prodotto
from MVC.model.SistemService.Backup import Backup
from MVC.model.Attività.Account import Account
from MVC.model.Servizio.Ricevuta import Ricevuta
from MVC.model.SistemService.Filtri import Filtri
from MVC.model.SistemService.Logging import Logging
from MVC.model.SistemService.Notifica import Notifica
from MVC.model.SistemService.Statistiche import Statistiche
from resourcesForUsatoBeato.AmministratoreViews.ExceptHandler import ExceptHandler


# Classe per gestire tutte le funzioni disponibili ad un amministratore del negozio
class Amministratore(User, AmministratoreInterface):

    def __init__(self):
        super().__init__()
        self.email = "admin"
        self.password = "password"

    # Metodo che aggiorna un account in base ai parametri passati dall'amministratore
    def aggiornaAccount(self, nome, cognome, dataDiNascitaStr, email, idAccount, numeroTelefonico, residenza):
        account = Account().aggiornaAccount(nome, cognome, dataDiNascitaStr, email, idAccount, numeroTelefonico,
                                            residenza)
        return account

    # Metodo che aggiorna un prodotto in base ai parametri passati dall'amministratore
    def aggiornaProdotto(self, nomeCategoria, dataEsposizione,
                         nomeProdotto, prezzoOriginale, nomeScaffale, idProdotto):
        Prodotto().aggiornaProdotto(nomeCategoria, None, nomeProdotto, prezzoOriginale, nomeScaffale, idProdotto)

    # Metodo che effettua il backup del sistema in maniera manuale dall amministratore
    # mentre il metodo nella classe Backup verra' richiamato dal sistema ad una determinata ora
    def effettuaBackup(self):
        Backup().effettuaBackup()

    # Metodo che elimina un account dal database
    def eliminaAccount(sel, idAccount):
        Account().eliminaAccount(idAccount)

    def eliminaAccountTramiteListaId(self, listaId):
        for id in listaId:
            self.eliminaAccount(id)

    # Metodo che elimina un prodotto dagli oggetti in vendita a quelli eliminati
    def eliminaProdotto(self, idProdotto):
        Prodotto().eliminaProdotto(idProdotto)
        try:
            Notifica().gestioneEmailDiEliminazione(idProdotto)
        except:
            pass

    # Metodo che rimuove i prodotti tramite una lista di id
    def eliminaProdottiTramiteListaId(self, listaId):
        for id in listaId:
            self.eliminaProdotto(id)

    # Metodo che rimuove i prodotti tramite una lista di id
    def vendiProdottiTramiteListaId(self, listaId):
        prodottiTrovati = Prodotto().recuperaListaProdottiInVendita()
        prodottiFiltrati = list()
        for prodotto in prodottiTrovati:
            for id in listaId:
                if id == prodotto.idProdotto:
                    prodottiFiltrati.append(prodotto)
        ricevuta = self.vendiProdotti(prodottiFiltrati)
        return ricevuta

    # Metodo che filtra i clienti in base al nome o al cognome
    # return = lista delle persone con dati passati
    def filtraClienti(self, nome, cognome):
        return Filtri().filtraClienti(nome, cognome)

    # Metodo per inserire un prodotto nel database
    def inserisciProdotto(self, dataEsposizione, idAccount,
                          nomeProdotto, prezzoOriginale, nomeScaffaleLe, nomeCategoria):
        categoria = Categoria().trovaCategoriaTramiteNome(nomeCategoria)
        if categoria == None:
            categoria = Categoria()
            categoria.aggiungiCategoria(nomeCategoria)
        try:
            idAccount = int(idAccount)
        except:
            pass
        try:
            prezzoOriginale = float(prezzoOriginale)
        except:
            pass
        try:
            nomeScaffaleLe = nomeScaffaleLe.lower()
        except:
            pass
        prodotto = Prodotto()
        prodotto.aggiungiProdotto(categoria.idCategoria, dataEsposizione, idAccount, nomeProdotto, prezzoOriginale,
                                  nomeScaffaleLe, nomeCategoria)
        prodotto.mettiOggettoSuListaNelFile()
        # if nomeScaffaleLe != "": Scaffale().associaProdottoAScaffale(prodotto)
        if idAccount != None: Account().associaProdottoAdAccount(prodotto)
        if nomeCategoria != "": Categoria().aggiungiProdottiInCategoria(prodotto)
        return prodotto

    # Metodo che serve per l'inserimento di un cliente Proprietario all'interno del database e la comunicazione delle
    # credenziali via emailProdotto().recuperaListaOggetti
    # credenziali via emailProdotto().recuperaListaOggetti
    def inserisciAccount(self, nome, cognome, dataDiNascita, email, password,
                         numeroTelefonico, cap, citofono, citta, civico, piazza, via):
        account = Account()
        if account.checkEmailUtente(email) == True:
            ExceptHandler().erroreCreazioneAdmin()
            return False
        indirizzo = Indirizzo(cap, citofono, citta, civico, piazza, via)
        account = Account().aggiungiAccount(nome, cognome, dataDiNascita, email, numeroTelefonico, password, indirizzo)
        logging = Logging()
        logging.aggiungiLogging(account.idAccount)
        logging.inserisciLoggingNelDatabase()
        Notifica().gestioneEmailDIRegistrazione(email, password)
        return account

    # Metodo di passaggio per la ricerca di un account
    def ricercaAccount(self, id):
        return Account().trovaOggettoTramiteId(id)

    # Metodo per la vendita di una lista di oggetti
    # prodottoList = lista di prodotti di vendere al cliente
    # return = dizionario con info di oggetti venduti
    def vendiProdotti(self, prodottoList):
        listaInfo = list()  # lista per scontrino
        for prodotto in prodottoList:
            Prodotto().spostaProdotto(prodotto.idProdotto, PathDatabase().inVenditaTxt, PathDatabase().vendutiTxt)
            listaInfo.append(Ricevuta().getInfoProdotto(prodotto))
        ricevuta = Ricevuta()
        ricevuta.aggiungiProdotti(listaInfo)
        ricevuta.salvaRicevuta()
        Notifica().gestioneEmailDiVendita(prodottoList)
        return ricevuta

    # Metodo che recupera le statistiche sul sistema
    def visualizzaStatistiche(self):
        Statistiche().visualizzaStatistiche()
