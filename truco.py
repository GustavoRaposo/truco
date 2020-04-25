from carta import Carta
from jogador import Jogador
import random

class Truco:

    def __init__(self, naipes, valores):
        self.naipes = naipes
        self.valores = valores
        self.baralho = []
        self.jogador1 = Jogador()
        self.jogador2 = Jogador()
        self.cartaMesa = Carta("","")

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

    def distribuiCartas(self):
        for i in range(6):
            if (i % 2 == 0):
                self.jogador1.mao.append(self.baralho[i])
            else:
                self.jogador2.mao.append(self.baralho[i])
        self.cartaMesa = Carta(self.baralho[6].naipe,self.baralho[6].valor)

    def printaMao(self):
        print("_____________________")
        for i in range(len(self.jogador1.mao)):
            print(self.jogador1.mao[i].valor + " " + self.jogador1.mao[i].naipe + "\n")
        print("_____________________")
        for i in range(len(self.jogador2.mao)):
            print(self.jogador2.mao[i].valor + " " + self.jogador2.mao[i].naipe + "\n")
