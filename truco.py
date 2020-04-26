import random
import arvore
import itertools
from carta import Carta
from jogador import Jogador

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

    def limpaMao(self):
        self.jogador1.mao.clear()
        self.jogador2.mao.clear()

    def fimDeJogo(self):
        if(self.jogador1.pontos >= 12 or self.jogador2.pontos >= 12):
            return False
        else:
            return True

    def rodada(self):
        countP1 = 0
        countP2 = 0
        pontosDaRodada = 1
        self.criaBaralho()
        self.limpaMao()
        self.distribuiCartas()

        while (countP1 == 2 or countP2 == 2):

            if self.jogador1.prioridade:
                self.jogada(self.jogador1)
                self.jogada(self.jogador2)
            else:
                self.jogada(self.jogador2)
                self.jogada(self.jogador1)

        if countP1 == 2:
            self.jogador1.pontos += pontosDaRodada
        if countP2 == 2:
            self.jogador2.pontos += pontosDaRodada
        self.baralho.clear()

    def zeraPontos(self):
        self.jogador1.pontos = 0
        self.jogador2.pontos = 0

    def estadoValido(self, estado):
        size = len(estado)
        #Sample é o número de posições que precisam ser válidas
        sample = [i for i in range(size)]
        valid = []

        #Esse loop verifica se a ordem das jogadas do estado alterna entre
        #jogador 2 e jogador 1, caso exista um estado onde tenha mais de uma jogada
        #consecutiva de qualquer jogador, ela é inválida
        for i in range(size):
            #Os ifs abaixo adicionam os indíces válidos, ou seja, se o índice for
            #par, a carta precisa ser do jogador 2, se o índice for ímpar, a carta precisa
            #ser do jogador 1, caso nenhuma dessas condições sejam atinjidas, o estado é inválido
            if i % 2 == 0 and "jogador2" in estado[i]:
                valid.append(i)
            elif i % 2 == 1 and "jogador1" in estado[i]:
                valid.append(i)

        if valid == sample:
            return True
        else:
            return False

    def todosEstados(self):
        estados = []
        #Cria uma cópia das duas mãos, uma para cada jogador, cada carta possui
        #uma identificação de quem é a carta
        mao1 = ["jogador1 " + i.getFull() for i in self.jogador1.mao]
        mao2 = ["jogador2 " + i.getFull() for i in self.jogador2.mao]
        cartas = mao1 + mao2
        #Todas as jogadas possíveis com as cartas, aqui não filtra se elas são válidas ou não
        todasCombinacoes = list(itertools.permutations(cartas))
        #Todas as jogadas que podem ser executadas com base no primeiro nível da árvore
        combinacoesPossiveis = [i for i in todasCombinacoes if i[0] in mao2]

        for i in combinacoesPossiveis:
            #Validação do estado que está sendo percorrido
            if self.estadoValido(i):
                #Remove a marcação do nome dos jogadores nas cartas
                estado = [j.replace("jogador2 ", "").replace("jogador1 ", "") for j in i]
                estados.append(estado)

        return estados

    def montaArvore(self):
        #Cria uma árvore tendo como raíz a carta atual na mesas
        tree = arvore.Arvore(arvore.MAX, info=self.cartaMesa.getFull())
        cartas = []
        #Todos os estados válidos para montar a árvore
        estados = self.todosEstados()
        node = tree
        nivel = arvore.MAX

        #Cria o primeiro nível da árvore com as cartas da IA
        for i in self.jogador2.mao:
            tree.criaAdjacenciaAtual(i.getFull(), 0, arvore.MIN)

        #Cria os níveis na árvore em profundidade
        for i in estados:
            size = len(i) - 1
            for j in range(size):
                tree.criaAdjacencia(i[j], i[j + 1], 0, nivel)
                #Troca o tipo do nível a cada nó criado
                nivel = arvore.MIN if nivel == arvore.MAX else arvore.MAX

        return tree

    def jogadaIa(self):
        #Criação da árvore para a jogada da IA
        tree = self.montaArvore()

    def jogo(self):
        self.jogador1.prioridade = True
        self.jogador2.prioridade = False
        self.zeraPontos()

        while self.fimDeJogo() == True:
            self.jogadaIa()
            self.jogador2.pontos = 13
            self.fimDeJogo()
