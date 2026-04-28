import copy

from database.DAO import DAO
from model.nerc import Nerc


class Model:
    def __init__(self):
        self.DAO = DAO()
        self._solBest = []
        self._listNerc = []
        self._listEvents = None
        self.loadNerc()
        self._soluzioni=[] #{num.clienti coivolti: soluzione parziale trovata}


    #quindi maxH è il numero massimo di anni
    def worstCase(self, nerc, maxY, maxH):
        eventi_da_analizzare=self.getAllEvents_nerc(nerc, maxY) #sarà la soluzione parziale
        #DEVO CAPIRE QUALI GRUPPI DI ANNI CONVIENE ANALIZZARE
        #DEVO CAPIRE QUALI EVENTI TOGLIERE DA parziale AFFINCHE' SI RIMANGA NEI VINCOLI DI DURATA maxY
        self.ricorsione([], maxY, maxH, 0, eventi_da_analizzare)
        return self._soluzioni

    def _is_anno(self, parziale, i, maxH):
        #i è l'elemento che sto aggiungendo
        if len(parziale)==0:
            return True #to aggiungendo il primo
        else:
            if parziale[-1].anno- i.anno <=maxH:
                return True
            else:
                return False

    def ricorsione(self, parziale, maxY, maxH, pos, tutti_eventi):
        # condizione terminale --> la durata massima è maxY (o se è maggiore in soluzione tolgo l'ultimo elemento)
        #clientiTot=0
        durata_tot=0
        #una roba del genere --> pos è l'indice dell'elemento di riferimento
        if pos==len(parziale):
            self._soluzioni.append(copy.deepcopy(parziale))
        else:
            #pos è l'elemento che sto ponendo come primo --> partiamo da zero
            for i in tutti_eventi: #i è l'evento
                durata_tot+=i.durata
                posizione=tutti_eventi.index(i)

                if durata_tot<=maxY and self._is_anno(parziale, i, maxH):
                    nuovo_parziale=copy.deepcopy(parziale)
                    nuovo_parziale.append(i)
                    self.ricorsione(nuovo_parziale, maxY, maxH, posizione , tutti_eventi)

                    #backtracking
                    parziale.pop()

    def getAllEvents_nerc(self, nerc: Nerc, maxY):
        all = self.get_events(nerc)  # lista con tutti gli eventi del nerc
        durata_ok=[]
        for evento in all:
            durata = evento.durata
            if durata <= maxY: #max durata in ore
               durata_ok.append(evento)
        return durata_ok #restituisce tutti gli eventi che rispettano i vincoli di nerc e durata

    #NB: DEVO POI RICONTROLLARE QUESTA LISTA PERCHE' LA SOMMA DELLE DURATE DEI SINGOLI EVENTI DEVE
    #COMUNQUE ESSERE MINORE DI MaxY

    # rimanenti è l'insieme delle soluzioni non ancora analizzate
    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def get_events(self, nerc):
        return self.DAO.getAllEvents(nerc)


    @property
    def listNerc(self):
        return DAO.getAllNerc()

