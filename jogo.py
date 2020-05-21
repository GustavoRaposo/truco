#encoding: utf-8

from arvore import Arvore
from copy import deepcopy
from random import randint
from random import shuffle
from numbers import Number
from itertools import permutations

MAX = 1000
MIN = -1000

class Jogo:
    def __init__(self, cartas, naipes, jogador1, jogador2):
        self.cartas = cartas
        self.naipes = naipes
        #Cartas para a rodada, elas são ponderadas de acordo com o vira
        self.cartasRodada = None
        self.baralho = None
        self.jogadores = [jogador1, jogador2]
        #-1 = ocorrendo
        #0 = jogador1 ganhou
        #1 = jogador2 ganhou
        self.estado = -1
        self.vira = None
        self.manilhas = None
        self.cartaMesa = None
        #Pontuação dos jogadores na partida
        #0 = jogador humano
        #1 = jogador cpu
        self.pontuacoes = [0, 0]
        #Pontuação para ganhar o jogo
        self.maxPontos = 12

    def inicia(self):
        self.baralho = deepcopy(self.cartas)
        self.cartasRodada = dict([(i.getFull(), i) for i in self.cartas])
        self.embaralhaBaralho()
        self.viraCarta()
        self.defineManilhas()
        self.ponderaCartas()
        self.distribuiCartas()

    def embaralhaBaralho(self):
        #Embaralha o baralho
        shuffle(self.baralho)

    def distribuiCartas(self):
        #Faz um cópia do baralho para poder modificar com segurança
        copiaBaralho = deepcopy(self.baralho)

        #Sorteia aleatóriamente 3 cartas para cada jogador, removendo elas da
        #cópia do baralho
        for i in self.jogadores:
            for j in range(3):
                index = randint(0, len(copiaBaralho) - 1)

                i.mao.append(copiaBaralho[index])
                del copiaBaralho[index]

        #Atualiza o baralho
        self.baralho = copiaBaralho

    def viraCarta(self):
        #Faz uma cópia do vira para manter seu valor original
        vira = deepcopy(self.baralho[0])
        #Atualiza a carta do vira
        self.vira = vira

    def defineManilhas(self):
        manilhas = []
        #Define qual o peso das manilhas
        maior = (self.vira.peso + 1) if (self.vira.peso + 1) <= 10 else 1

        #Adiciona as manilhas todas as cartas que contém o peso de manilha
        for i in self.cartasRodada:
            if self.cartasRodada[i].peso == maior:
                manilhas.append(self.cartasRodada[i])

        #Atualiza as manilhas
        self.manilhas = manilhas

    def ponderaCartas(self):
        #Cria um vetor com valor da carta e naipe para facilitar a comparação
        manilhasText = [i.valor + " " + i.naipe.nome for i in self.manilhas]
        #Faz uma cópia das cartas originais para não alterar elas
        cartasPonderadas = deepcopy(self.cartas)

        #Atribui valores maiores para as cartas com valores de vira e manilha
        for i in cartasPonderadas:
            if i.getFull() in manilhasText:
                i.peso = 11

        #Cria um novo dicionário para ponderar
        cartasPonderadasDict = dict((i.getFull(), i) for i in cartasPonderadas)

        self.cartasRodada = cartasPonderadasDict

    def reiniciaMao(self):
        for i in self.jogadores:
            i.mao = []

    def reiniciaPontos(self):
        for i in self.jogadores:
            i.pontuacao = 0

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
        mao1 = ["jogador1 " + i.getFull() for i in self.jogadores[0].mao]
        mao2 = ["jogador2 " + i.getFull() for i in self.jogadores[1].mao]
        cartas = mao1 + mao2
        #Todas as jogadas possíveis com as cartas, aqui não filtra se elas são válidas ou não
        todasCombinacoes = list(permutations(cartas))
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
        tree = Arvore(self.vira.getFull())
        cartas = []
        #Todos os estados válidos para montar a árvore
        estados = self.todosEstados()
        node = tree

        #Cria o primeiro nível da árvore com as cartas da IA
        for i in self.jogadores[1].mao:
            tree.criaAdjacencia(i.getFull())

        #Cria os níveis na árvore em profundidade
        for i in estados:
            size = len(i) - 1
            #Busca o nó inicial
            index = tree.getIndex(i[0])
            node = tree.adjacencias[index]

            for j in range(size):
                #Cria uma adjacencia entre o nó atual e a jogada
                node.criaAdjacencia(i[j + 1])

                #Define o próximo nó como o nó inserido acima
                index = node.getIndex(i[j + 1])
                node = node.adjacencias[index]
            node = tree

        return tree

    #Função personalizada para maior valor.
    #Heurística: Busca jogar a menor carta que ganhe da escolhida pelo jogador.
    def maior(self, carta0, carta1):
        if not isinstance(carta0, Number):
            peso_atual = 100
            card = 0
            for i in range(len(self.jogadores[1].mao)):
                if self.jogadores[1].mao[i].peso < peso_atual and self.jogadores[1].mao[i].peso > self.cartaMesa.peso:
                    peso_atual = self.jogadores[1].mao[i].peso
                    card = i
            self.jogadores[1].mao[card].info = self.jogadores[1].mao[card].valor + ' ' + self.jogadores[1].mao[card].naipe.nome
            return self.jogadores[1].mao[card]
        else:
            return carta1

    #Função personalizada para menor valor
    def menor(self, carta0, carta1):
        if not isinstance(carta0, Number):
            carta0busca = self.cartasRodada[carta0.info]
            carta1busca = self.cartasRodada[carta0.info]

            if carta0busca.peso > carta1busca.peso:
                return carta0
            elif carta0busca.peso < carta1busca.peso:
                return carta1
            elif carta0busca.peso == carta1busca.peso:
                if carta0busca.naipe.peso > carta1busca.naipe.peso:
                    return carta0
                elif carta0busca.naipe.peso < carta1busca.naipe.peso:
                    return carta1
                elif carta0busca.naipe.peso == carta1busca.naipe.peso:
                    return carta0
        else:
            return carta1

    #Função personalizada para menor igual
    def isMenorIgual(self, valor0, valor1):
        if not isinstance(valor0, Number):
            carta0busca = self.cartasRodada[valor0.info].peso
        else:
            carta0busca = valor0

        if not isinstance(valor1, Number):
            carta1busca = self.cartasRodada[valor1.info].peso
        else:
            carta1busca = valor1

        if carta0busca <= carta1busca:
            return True
        else:
            return False

    def alfabeta(self, profundidade, jogadorMax, estado, alpha, beta):
        #Condição de parada, se a recursão chegar em uma folha da árvore
        if profundidade == 0 or len(estado.adjacencias) <= 0:
            return estado

        if jogadorMax:
            melhorValor = MIN

            for i in estado.adjacencias:
                #Valor do próximo nó
                valor = self.alfabeta(profundidade - 1, not jogadorMax, i, alpha, beta)
                melhorValor = self.maior(melhorValor, valor)

                #Maior valor
                alpha = self.maior(alpha, melhorValor)

                if self.isMenorIgual(beta, alpha):
                    break

            return melhorValor

        else:
            melhorValor = MAX

            for i in estado.adjacencias:
                #Valor do próximo nó
                valor = self.alfabeta(profundidade - 1, not jogadorMax, i, alpha, beta)
                melhorValor = self.menor(melhorValor, valor)

                #Menor valor
                beta = self.menor(beta, melhorValor)

                if self.isMenorIgual(beta, alpha):
                    break

            return melhorValor

    def jogadaIa(self):
        print("Mão da CPU:")
        self.jogadores[1].printaMao()
        print("")

        if len(self.jogadores[1].mao) > 1:
            #Criação da árvore para a jogada da IA
            tree = self.montaArvore()
            #Definição da profundidade da árvore
            profundidade = len(self.jogadores[0].mao) + len(self.jogadores[1].mao)
            #Melhor jogada pela poda alfa beta
            melhorOpcao = self.alfabeta(profundidade, True, tree, MIN, MAX)

            print("Melhor Opção: " + melhorOpcao.info)

            carta = self.cartasRodada[melhorOpcao.info]
        else:
            carta = self.jogadores[1].mao[0]

        self.cartaMesa = carta
        self.jogadores[1].removeCarta(carta)
        print("CPU jogou: " + carta.getFull() + "\n")

        return carta

    def jogadaHumano(self):
        print("Sua mão:")

        escolhendo = True
        self.jogadores[0].printaMao()
        print("")

        while escolhendo:
            try:
                escolha = int(input("selecione entre 0 e " + str(len(self.jogadores[0].mao) -1) + ": "))
                carta = self.jogadores[0].mao[escolha]
                escolhendo = False
            except ValueError:
                print("Escolha inválida!")
            except IndexError:
                print("Escolha fora dos limites!")

        # carta = self.jogadores[0].mao[randint(0, len(self.jogadores[0].mao) - 1)]

        self.cartaMesa = carta
        self.jogadores[0].mao.remove(carta)
        print("\nVocê jogou: " + carta.getFull() + "\n")

        return carta

    def fimDeRodada(self):
        for i in range(len(self.jogadores)):
            if self.jogadores[i].pontuacao >= 3:
                self.pontuacoes[i] += 1

                print("=======================================\n")
                print(self.jogadores[i].nome + " Ganhou\n")
                print("============= nova rodada =============\n")

                return True

        return False

    def fimDeJogo(self):
        for i in range(len(self.jogadores)):
            if self.pontuacoes[i] == self.maxPontos:
                self.estado = i

                return True

        return False

    def executaJogada(self, cartaJogador, cartaCpu, pontos):
        #Jogador 1 pontua
        if cartaJogador.peso > cartaCpu.peso:
            self.jogadores[0].pontuacao += pontos
        #Jogador 2 pontua
        elif cartaJogador.peso < cartaCpu.peso:
            self.jogadores[1].pontuacao += pontos
        #Em caso de empate, o critério de desempate são os naipes
        elif cartaJogador.peso == cartaCpu.peso:
            #Jogador 1 pontua
            if cartaJogador.naipe.peso > cartaCpu.naipe.peso:
                self.jogadores[0].pontuacao += pontos
            #Jogador 2 pontua
            elif cartaJogador.naipe.peso < cartaCpu.naipe.peso:
                self.jogadores[1].pontuacao += pontos
            #Em caso de empate dos naipes, os dois pontuam
            elif cartaJogador.naipe.peso == cartaCpu.naipe.peso:
                self.jogadores[0].pontuacao += pontos
                self.jogadores[1].pontuacao += pontos

    def printInfoMesa(self):
        print("--------------------------\n")
        print("Vira: " + self.vira.getFull() + "\n")
        print("Pontuação\n" + self.jogadores[0].nome + ": " + str(self.pontuacoes[0]) +\
              "\n" + self.jogadores[1].nome + ": " + str(self.pontuacoes[1]))
        print("\n--------------------------\n")

    def joga(self):
        pontuacaoRodada = 1

        self.inicia()
        self.printInfoMesa()

        while True:
            cartaJogador = self.jogadaHumano()
            cartaCpu = self.jogadaIa()
            self.executaJogada(cartaJogador, cartaCpu, pontuacaoRodada)

            if self.fimDeRodada():
                if self.fimDeJogo():
                    return self.jogadores[self.estado].nome

                self.reiniciaPontos()
                self.reiniciaMao()
                self.inicia()
                self.printInfoMesa()

                pontuacaoRodada = 1
            else:
                pontuacaoRodada += 1
