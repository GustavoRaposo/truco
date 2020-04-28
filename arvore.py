#encoding: utf-8

import sys

class Arvore:
    def __init__(self, info=None):
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

    #Cria uma nova adjacência
    #x = primeiro nó da adjacência
    #y = segundo nó da adjacência
    #peso = peso da adjacência
    #nivel = nível do nó, se ele vai ser min ou max
    def criaAdjacencia(self, x, y):
        if self.info == x:
            if not self.existe(y):
                self.adjacencias.append(Arvore(info))
        else:
            if self.adjacencias:
                for i in self.adjacencias:
                    i.criaAdjacencia(x, y)

    def criaAdjacenciaAtual(self, info):
        if not self.existe(info):
            self.adjacencias.append(Arvore(info))

    #Imprime a árvore, esse método começa a imprime nó por nó em profundidade
    def printa(self):
        sys.stdout.write(self.info + "\n")

        if self.adjacencias:
            for i in self.adjacencias:
                i.printa()

#encoding: utf-8

import random

#Variáveis para definir valor inicial do min e max
MAX = 1000
MIN = -1000

# Returns optimal value for current player
#(Initially called for root and maximizer)

def alfabeta(profundidade, indiceNode, jogadorMax, estados, alfa, beta, profundidadeMaxima=3):
    #Condição de parada, se a recursão chegar em uma folha da árvore
    if profundidade == profundidadeMaxima:
        return estados[indiceNode]

    if jogadorMax:
        melhorOpcao = MIN

        #Busca recursiva para os nós esquerdo e direito, para o jogador maximizador
        for i in range(0, 2):
            #Próximo node
            indiceProximoNode = (indiceNode + indiceNode + i)
            #Valor acima do node atual
            acima = alfabeta(profundidade + 1, indiceProximoNode, False, estados, alfa, beta)
            #Maior valor entre melhorOpcao e val
            melhorOpcao = max(melhorOpcao, acima)
            #Maior valor entre alfa e melhorOpcao
            alfa = max(alfa, melhorOpcao)

            #Poda alfa beta
            if beta <= alfa:
                break

        return melhorOpcao

    else:
        melhorOpcao = MAX

        #Busca recursiva para os nós esquerdo e direito, para o jogador minimizador
        for i in range(0, 2):
            indiceProximoNode = (indiceNode + indiceNode + i)
            #Valor acima do node atual
            acima = alfabeta(profundidade + 1, indiceProximoNode, True, estados, alfa, beta)
            #Menor valor entre melhorOpcao e val
            melhorOpcao = min(melhorOpcao, acima)
            #Menor acimaor entre beta e melhorOpcao
            beta = min(beta, melhorOpcao)

            #Poda alfa beta
            if beta <= alfa:
                break

        return melhorOpcao

def alfabeta2(profundidade, jogadorMax, estado, alfa, beta):
    #Condição de parada, se a recursão chegar em uma folha da árvore
    if profundidade == 0:
        return estado

    if jogadorMax:
        valorMax = MIN

        #Busca recursiva para os nós esquerdo e direito, para o jogador maximizador
        #for i in range(0, 2):]
        print(estado)
        for i in estado:
            valor = alfabeta2(profundidade - 1, not jogadorMax, i.adjacencias, alfa, beta)
            print(valorMax)
            print(valor)
            valorMax = max(valorMax, valor)

            #Poda alfa beta
            #if beta <= alfa:
            #    break

        return valorMax

    else:
        valorMin = MAX

        #Busca recursiva para os nós esquerdo e direito, para o jogador minimizador
        #for i in range(0, 2):
        for i in estado:
            valor = alfabeta2(profundidade - 1, not jogadorMax, i.adjacencias, alfa, beta)
            valorMin = min(valorMin, valor)

            #Poda alfa beta
            #if beta <= alfa:
            #    break

        return valorMin

estados = [3, 5, 6, 9, 1, 2, 0, -1]
#estados = [random.randint(0, 15) for i in range(36)]
#print(estados)
#print("The optimal value is :", alfabeta2(3, 0, True, estados, MIN, MAX))
#print("The optimal value is :", alfabeta(0, 0, True, estados, MIN, MAX))
# This code is contributed by Rituraj Jain
