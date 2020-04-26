#encoding: utf-8

import sys

#Variáveis globais para definir o min e max
MAX = "max"
MIN = "min"

class Arvore:
    def __init__(self, nivel, info=None, peso=0):
        self.info = info
        self.peso = peso
        self.nivel = nivel
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

    #Cria uma nova adjacência
    #x = primeiro nó da adjacência
    #y = segundo nó da adjacência
    #peso = peso da adjacência
    #nivel = nível do nó, se ele vai ser min ou max
    def criaAdjacencia(self, x, y, peso, nivel):
        if self.info == x:
            if not self.existe(y):
                self.adjacencias.append(Arvore(nivel, info=y, peso=peso))
        else:
            if self.adjacencias:
                for i in self.adjacencias:
                    i.criaAdjacencia(x, y, peso, nivel)

    def criaAdjacenciaAtual(self, info, peso, nivel):
        if not self.existe(info):
            self.adjacencias.append(Arvore(nivel, info=info, peso=peso))

    #Imprime a árvore, esse método começa a imprime nó por nó em profundidade
    def printa(self):
        sys.stdout.write(self.info + " " + self.nivel + ", " + str(self.peso) + "\n")

        if self.adjacencias:
            for i in self.adjacencias:
                i.printa()
