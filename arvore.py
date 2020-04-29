#encoding: utf-8

import sys

class Arvore:
    def __init__(self, info):
        self.info = info
        self.adjacencias = []

    def existe(self, no):
        for i in self.adjacencias:
            if i.info == no:
                return True
        return False

    def getIndex(self, no):
        max = len(self.adjacencias)

        for i in range(max):
            if self.adjacencias[i].info == no:
                return i
        return False

    def criaAdjacencia(self, info):
        if not self.existe(info):
            self.adjacencias.append(Arvore(info))

    #Imprime a árvore, esse método começa a imprime nó por nó em profundidade
    def printa(self):
        if self.adjacencias:
            print(self.adjacencias)
            for i in self.adjacencias:
                i.printa()
