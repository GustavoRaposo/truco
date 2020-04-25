from carta import Carta
import random

class Truco:

    def __init__(self, naipes, valores):
        self.naipes = naipes
        self.valores = valores
        self.baralho = []

    def criaBaralho(self):
        baralho = []
        for i in self.naipes:
            for j in self.valores:
                baralho.append(Carta(i,j))

        self.baralho = baralho

    def printaBaralho(self):
        for i in self.baralho:
            print(i.valor + " " + i.naipe + "\n")

    def embaralhaBaralho(self):
        random.shuffle(self.baralho)
