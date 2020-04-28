from carta import Carta
from jogador import Jogador
import random

class Truco:

    def __init__(self, naipes, nome, valores):
        self.naipes = naipes
        self.valores = valores
        self.baralho = []
        self.jogador1 = Jogador()
        self.jogador2 = Jogador()
        self.cartaMesa = Carta("","","","")
        self.nome = nome

    def criaBaralho(self):
        baralho = []
        subvalor = 1
        for i in self.naipes:
            for j in range(10):
                baralho.append(Carta(i,self.nome[j],self.valores[j],subvalor))
            subvalor = subvalor + 1

        self.baralho = baralho

    def printaBaralho(self):
        for i in self.baralho:
            print(i.nome + " " + i.naipe + "\n")

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
            print(jogador.mao[i].nome + " " + jogador.mao[i].naipe + " " + str(jogador.mao[i].valor) + " " +str(jogador.mao[i].subvalor) + "\n")


    def limpaMao(self):
        self.jogador1.mao.clear()
        self.jogador2.mao.clear()

    def fimDeJogo(self):
        if(self.jogador1.pontos >= 2 or self.jogador2.pontos >= 2):
            print("ACABOU!")
            return False
        else:
            return True
    def jogadaComp(self, jogador):
        escolha = random.randint(0,len(jogador.mao) -1)
        carta = jogador.mao[escolha]
        jogador.mao.remove(carta)
        print("Computador jogou: " + carta.nome + " - " + str(carta.valor))
        print("--------------------------")
        return carta
    def jogadaPlayer(self, jogador):
        self.printaMao(jogador)
        escolha = int(input("selecione entre 0 e " + str(len(jogador.mao) -1) + ":"))
        carta = jogador.mao[escolha]
        jogador.mao.remove(carta)
        print("jogador jogou: " + carta.nome + " - " +  str(carta.valor))
        print("--------------------------")
        return carta

    def acabou(self, c1, c2):
        if c1 == 2 or c2 == 2:
            return True
        else:
            return False
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
                jogada2 = self.jogadaComp(self.jogador2)
            else:
                jogada2 = self.jogadaComp(self.jogador2)
                jogada1 = self.jogadaPlayer(self.jogador1)
            # valida se a rodada é 2 ou 3 e se os jogadores jogaram cartas iguais e diferentes de manilhas
            if(jogada1.valor == jogada2.valor and rodadas >= 2 and jogada1.valor != 11):
                print("entrou no criterio")
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


