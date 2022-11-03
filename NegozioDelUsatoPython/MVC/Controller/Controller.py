from MVC.Model.Attività.Account import Account
from MVC.Model.Attività.Amministratore import Amministratore
from MVC.Model.Attività.User import User
from MVC.Model.Servizio.Prodotto import Prodotto


class Controller(object):


    def userLoginController(self, email, password):
        return User().login(email, password)

    def amministratoresaveProdottoBtn(self, nomeLe, idAccountLe, dataEsposizione, prezzoLe, idCategoriaLe, idScaffaleLe):
        return Amministratore().inserisciProdotto(idCategoriaLe, dataEsposizione, idAccountLe, nomeLe, prezzoLe, idScaffaleLe)

    def recuperaListaProdottiInVendita(self):
        return Prodotto().recuperaListaProdottiInVendita()

    def saveCLienteBtnClicked(self, nomeLe, cognomeLe, dataNascitaLe, emailLe, passwordLe, telefonoLe, capLe,
                              cittaLe, viaLe, piazzaLe, civicoLe, citofonoLe):
        return Amministratore().inserisciAccount(nomeLe, cognomeLe, dataNascitaLe, emailLe, passwordLe, telefonoLe, capLe, citofonoLe, cittaLe, civicoLe, piazzaLe, viaLe)
        #TODO verificare esistenza di probabile bug con l'iserimento di date DD-MM-YY rispetto a quello che restituisce il
        # metodo datetime.today()

    def recuperaListaAccounts(self):
        return Account().recuperaListaOggetti()

    def effettuaBackup(self):
        Amministratore().effettuaBackup()