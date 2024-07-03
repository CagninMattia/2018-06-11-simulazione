import copy
from geopy import distance

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        # Creo grafo
        self.grafo = nx.DiGraph()
        # Creo dizionario per nodi
        self.diz_vertici = {}
        self.lunghezza_max = None
        self.archi_cammino = []

    def get_anni(self):
        return DAO.get_anni()

    def get_num_apparizioni(self, a):
        return DAO.get_num_apparizioni(a)

    def crea_grafo(self, anno):
        self.grafo.clear()
        # Cancello diz o liste se le ho inizializzate se uno schiacca due volte pulsante non ci sono problemi
        self.diz_vertici.clear()
        nodi = DAO.get_vertici(anno)
        for n in nodi:
            self.diz_vertici[n.id] = n
            self.grafo.add_node(n)
        archi = DAO.get_archi(anno)
        for a in archi:
            self.grafo.add_edge(self.diz_vertici[a[0].upper()], self.diz_vertici[a[1].upper()])

    # Ritorno lunghezza nodi e archi
    def num_nodi(self):
        return len(self.grafo.nodes)

    def num_archi(self):
        return len(self.grafo.edges)

    def get_stati(self):
        return self.grafo.nodes

    def analizza_grafo(self, stato):
        stato = self.diz_vertici[stato]
        lista_suc = list(self.grafo.successors(stato))
        lista_prec = list(self.grafo.predecessors(stato))
        albero = nx.bfs_tree(self.grafo, stato)
        visitabili = list(albero.nodes)
        visitabili.remove(stato)  # Rimuovi lo stato stesso dalla lista
        return lista_suc, lista_prec, visitabili

    def get_ciclo_max(self, stato):
        self.lunghezza_max = -100000000
        self.archi_cammino.clear()
        self.ricorsione([self.diz_vertici[stato]], [])
        return self.lunghezza_max, self.archi_cammino

    def ricorsione(self, cammino_attuale, lista_archi):
        if len(cammino_attuale) > len(self.archi_cammino)+1:
            self.lunghezza_max = copy.deepcopy(len(cammino_attuale)-1)
            self.archi_cammino = copy.deepcopy(lista_archi)

        for nodo in self.grafo.successors(cammino_attuale[-1]):
            if [cammino_attuale[-1], nodo] not in lista_archi:
                lista_archi.append([cammino_attuale[-1], nodo])
                cammino_attuale.append(nodo)
                self.ricorsione(cammino_attuale, lista_archi)
                cammino_attuale.pop()
                lista_archi.pop()