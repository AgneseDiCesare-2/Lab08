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
        self._best_soluzione = []
        self._best_clienti = 0

    #quindi maxH è il numero massimo di anni
    def worstCase(self, nerc, maxY, maxH):
        eventi_da_analizzare=self.getAllEvents_nerc(nerc, maxY) #sarà la soluzione parziale
        #DEVO CAPIRE QUALI GRUPPI DI ANNI CONVIENE ANALIZZARE
        #DEVO CAPIRE QUALI EVENTI TOGLIERE DA parziale AFFINCHE' SI RIMANGA NEI VINCOLI DI DURATA maxY
        self.ricorsione([], maxY, maxH, 0, eventi_da_analizzare)
        return self._best_soluzione

    def _is_anno(self, parziale, i, maxH):
        # i è l'elemento che sto provando ad aggiungere

        if len(parziale) == 0:
            return True

        anni = []

        for evento in parziale:
            anni.append(evento.anno)

        anni.append(i.anno)

        anno_min = min(anni)
        anno_max = max(anni)

        if anno_max - anno_min <= maxH:
            return True
        else:
            return False

    def _calcola_clienti(self, lista_eventi):
        tot = 0
        for e in lista_eventi:
            tot += e.customers_affected
        return tot

    def ricorsione(self, parziale, maxY, maxX, durata_tot, tutti_eventi):

        if len(tutti_eventi) == 0:

            clienti = self._calcola_clienti(parziale)

            if clienti > self._best_clienti:
                self._best_clienti = clienti
                self._best_soluzione = copy.deepcopy(parziale)

        else:

            # prendo il primo evento da analizzare
            i = tutti_eventi[0]

            nuovi_eventi = copy.deepcopy(tutti_eventi)
            nuovi_eventi.pop(0)

            nuova_durata = durata_tot + i.durata

            # RAMO 1: provo a prendere l'evento
            if nuova_durata <= maxY and self._is_anno(parziale, i, maxX):
                nuovo_parziale = copy.deepcopy(parziale)
                nuovo_parziale.append(i)

                self.ricorsione(
                    nuovo_parziale,
                    maxY,
                    maxX,
                    nuova_durata,
                    nuovi_eventi
                )

            # RAMO 2: provo a NON prendere l'evento
            self.ricorsione(
                parziale, #uso il vecchio parziale, in cui l'evento non c'è
                maxY,
                maxX,
                durata_tot, #vecchia durata
                nuovi_eventi #lo tolgo comunque dalla lista
            )

    def getAllEvents_nerc(self, nerc: Nerc, maxY):
        all = self.get_events(nerc)  # lista con tutti gli eventi del nerc
        durata_ok=[]
        for evento in all:
            durata = evento.durata
            if durata <= int(maxY): #max durata in ore
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

