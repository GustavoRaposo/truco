#encoding: utf-8

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        #Pontuação para cada rodada da partida
        self.pontuacao = 0

    def removeCarta(self, carta):
        for i in self.mao:
            if i.getFull() == carta.getFull():
                self.mao.remove(i)

    def printaMao(self):
        max = len(self.mao)

        for i in range(max):
            print(str(i) + ") " + self.mao[i].getFull())
