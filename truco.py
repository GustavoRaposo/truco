import random
import arvore
import itertools
from carta import Carta
from jogador import Jogador

MAX = 1000
MIN = -1000

class Truco:
    def __init__(self, naipes, nome, valores):
        self.naipes = naipes
        self.valores = valores
        self.valoresAux = dict()
        self.baralho = []
        self.baralhoAux = dict()
        self.jogador1 = Jogador()
        self.jogador2 = Jogador()
        self.cartaMesa = Carta("", "", "", "")
        self.nome = nome

    def criaBaralho(self):
        baralho = []
        baralhoAux = dict()
        valoresAux = dict()
        subvalor = 1

        for i in self.naipes:
            for j in range(10):
                carta = Carta(i,self.nome[j], self.valores[j], subvalor)
                baralhoAux[carta.getFull()] = carta
                valoresAux[carta.nome] = carta.valor

                baralho.append(carta)
            subvalor = subvalor + 1

        self.baralho = baralho
        self.baralhoAux = baralhoAux
        self.valoresAux = valoresAux

    def printaBaralho(self):
        for i in self.baralho:
            print(i.valor + " " + i.naipe + "\n")

    def embaralhaBaralho(self):
        random.shuffle(self.baralho)

    def distribuiCartas(self):
        self.cartaMesa = self.baralho[0]
        self.baralho.remove(self.baralho[0])

        for k in range(len(self.baralho)):
            if self.baralho[k].valor == 1 and self.cartaMesa.valor == 10:
                self.baralho[k].valor = 11
            else:
                if self.baralho[k].valor == self.cartaMesa.valor + 1:
                    self.baralho[k].valor = 11
        for i in range(6):
            if (i % 2 == 0):
                self.jogador1.mao.append(self.baralho[i])
            else:
                self.jogador2.mao.append(self.baralho[i])

    def printaMao(self, jogador):
        print("Manilha: " + self.cartaMesa.nome + " " + self.cartaMesa.naipe)
        print("_____________________")
        for i in range(len(jogador.mao)):
            #print(jogador.mao[i].nome + " " + jogador.mao[i].naipe + " " + str(jogador.mao[i].valor) + " " +str(jogador.mao[i].subvalor) + "\n")
            jogador.mao[i].printa()

    def limpaMao(self):
        self.jogador1.mao.clear()
        self.jogador2.mao.clear()

    def fimDeJogo(self):
        if(self.jogador1.pontos >= 2 or self.jogador2.pontos >= 2):
            print("ACABOU!")
            return False
        else:
            return True

    def acabou(self, c1, c2):
        if c1 == 2 or c2 == 2:
            return True
        else:
            return False

    def zeraPontos(self):
        self.jogador1.pontos = 0
        self.jogador2.pontos = 0

    def maiorQueMesa(self, carta):
        if carta.valor > self.cartaMesa.valor:
            return True
        else:
            return False

    def menorQueMesa(self, carta):
        if carta.valor < self.cartaMesa.valor:
            return True
        else:
            return False

    def cartaMaior(self, cartas):
        #Se houver somente uma carta na mao, retorna ela, caso contrário, é realizada uma
        #busca da maior carta
        if(type(cartas) != "list"):
            return cartas
        else:
            maior = cartas[0]

            for i in cartas:
                if self.maiorQueMesa(self.baralhoAux[i.info]):
                    maior = i

            return maior

    def cartaMenor(self, cartas):
        #Se houver somente uma carta, retorna ela, caso contrário, é realizada uma
        #busca da menor carta
        if(type(cartas) != "list"):
            return cartas
        else:
            menor = cartas[0]

            for i in cartas:
                if self.menorQueMesa(self.baralhoAux[i.info]):
                    menor = i

            return menor

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
        tree = arvore.Arvore(self.cartaMesa.getFull())
        cartas = []
        #Todos os estados válidos para montar a árvore
        estados = self.todosEstados()
        node = tree

        #Cria o primeiro nível da árvore com as cartas da IA
        for i in self.jogador2.mao:
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

    def alfabeta(self, profundidade, jogadorMax, estado):
        #Condição de parada, se a recursão chegar em uma folha da árvore
        if profundidade == 0:
            return estado

        if jogadorMax:
            valorMax = MIN

            for i in estado.adjacencias:
                #Valor do próximo nó
                valor = self.alfabeta(profundidade - 1, not jogadorMax, i)
                #Maior carta nas adjacencias do nó
                maiorCarta = self.cartaMaior(valor)
                #Maior valor
                valorMax = max(valorMax, maiorCarta.valor)

            return valorMax

        else:
            valorMin = MAX

            for i in estado.adjacencias:
                #Valor do próximo nó
                valor = self.alfabeta(profundidade - 1, not jogadorMax, i)
                #Menor carta nas adjacencias do nó
                menorCarta = self.cartaMenor(valor)
                #Menor valor
                valorMin = max(valorMax, menorCarta.valor)

            return valorMin

    def jogadaIa(self, jogador):
        self.printaMao(jogador)

        if len(jogador.mao) > 1:
            #Criação da árvore para a jogada da IA
            tree = self.montaArvore()
            melhorOpcao = self.alfabeta(3, True, tree)
            carta = self.baralhoAux[melhorOpcao.info]
        else:
            carta = jogador.mao[0]

        jogador.mao.remove(carta)
        print("Computador jogou: " + carta.getFull())
        print("--------------------------")
        return carta

    def jogadaPlayer(self, jogador):
        self.printaMao(jogador)
        escolhendo = True

        while escolhendo:
            try:
                escolha = int(input("selecione entre 0 e " + str(len(jogador.mao) -1) + ":"))
                carta = jogador.mao[escolha]
                escolhendo = False
            except ValueError:
                print("Escolha inválida!")
            except IndexError:
                print("Escolha fora dos limites!")

        jogador.mao.remove(carta)
        print("jogador jogou: " + carta.getFull())
        print("--------------------------")
        return carta

    def rodada(self):
        countP1 = 0
        countP2 = 0
        rodadas = 1
        empate = 0

        self.criaBaralho()
        self.embaralhaBaralho()
        self.limpaMao()
        self.distribuiCartas()
        self.jogador1.prioridade = True
        self.jogador2.prioridade = False

        while (self.acabou(countP1,countP2) == False or empate == 3):
            #define quem vai jogar
            if self.jogador1.prioridade:
                jogada1 = self.jogadaPlayer(self.jogador1)
                jogada2 = self.jogadaIa(self.jogador2)
            else:
                jogada2 = self.jogadaIa(self.jogador2)
                jogada1 = self.jogadaPlayer(self.jogador1)
            # valida se a rodada é 2 ou 3 e se os jogadores jogaram cartas iguais e diferentes de manilhas
            if(jogada1.valor == jogada2.valor and rodadas >= 2 and jogada1.valor != 11):
                if(self.jogador1.primeiraRodada == True):
                    countP1 = countP1 + 1
                    print("============ nova rodada ==============")
                else:
                    countP2 = countP2 + 1
                    print("============ nova rodada ==============")
            # define se os jogadores jogaram cartas iguais diferentes de manilhas
            if(jogada1.valor == jogada2 and jogada1.valor == 11):
                print("entrou no jogadas iguais sem ser manilha")
                if(jogada1.subvalor > jogada2.subvalor):
                    countP1 = countP1 + 1
                    if(rodadas == 1):
                        self.jogador1.primeiraRodada = True

                    self.jogador1.prioridade = True
                    self.jogador2.prioridade = False
                    print("============ nova rodada ==============")
                else:
                    countP2 = countP2 + 1
                    if(rodadas == 1):
                        self.jogador2.primeiraRodada = True
                    self.jogador1.prioridade = False
                    self.jogador2.prioridade = True
                    print("============ nova rodada ==============")
            #se empatar na primeira rodada os dois ganham o ponto, se empatar mais vezes ninguem ganha ponto e se empatar 3 vezes sai do loop e ninguem ganha
            if(jogada1.valor == jogada2.valor):
                #print("entrou no igual")
                if(empate == 0):
                    countP2 = countP2 + 1
                    countP1 = countP1 + 1
                    empate = empate + 1
                    print("============ nova rodada ==============")
                else:
                    empate = empate + 1
            #se uma das cartas for maior que a outra
            if(jogada1.valor > jogada2.valor):
                #print("valores : " + str(jogada1.valor) +" " + str(jogada2.valor))
                countP1 = countP1 + 1
                #print("entrou no maior")
                #print(countP1)
                if(rodadas == 1):
                    self.jogador1.primeiraRodada = True
                self.jogador1.prioridade = True
                self.jogador2.prioridade = False
                print("============ nova rodada ==============")
            else:
                #print("entrou no maior ao contrario")
                countP2 = countP2 + 1
                if(rodadas == 1):
                    self.jogador2.primeiraRodada = True
                self.jogador1.prioridade = False
                self.jogador2.prioridade = True
                print("============ nova rodada ==============")


        if countP1 == 2:
            self.jogador1.pontos += 1
            print("Player Ganhou")
        if countP2 == 2:
            self.jogador2.pontos += 1
            print("Computador Ganhou")
        self.baralho.clear()
        print("==================================")

    def jogo(self):
        self.jogador1.prioridade = True
        self.jogador2.prioridade = False

        while self.fimDeJogo() == True:
            self.fimDeJogo()
            self.rodada()
