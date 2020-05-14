#encoding: utf-8

class Carta:
    def __init__(self, valor, naipe, peso):
        self.valor = valor
        self.naipe = naipe
        self.peso = peso

    def getFull(self):
        return self.valor + " " + self.naipe.nome

    def printa(self):
        print(self.valor + " " + self.naipe.nome)
