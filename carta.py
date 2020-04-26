import sys

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor

    def getFull(self):
        return self.valor + " " + self.naipe

    def printa(self):
        print(self.valor + " " + self.naipe)
