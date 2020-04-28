import sys

class Carta:
    def __init__(self, naipe, nome, valor, subvalor):
        self.naipe = naipe
        self.valor = valor
        self.nome = nome
        self.subvalor = subvalor

    def getFull(self):
        return str(self.nome) + " " + (self.naipe)

    def printa(self):
        print(self.nome + " " + self.naipe)
