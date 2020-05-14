#encoding: utf-8

from jogo import Jogo
from carta import Carta
from naipe import Naipe
from jogador import Jogador

def setNomeJogador():
    definindo = True

    while definindo:
        try:
            nomeJogador = input("Jogador, digite seu nome: ")

            if " " not in nomeJogador and len(nomeJogador) > 0 and nomeJogador != "cpu":
                definindo = not definindo
            else:
                print("Nome inválido, contém espaços ou é muito curto")
        except:
            print("Nome inválido!")

    return nomeJogador

if __name__ == "__main__":
    #nomeJogador = setNomeJogador()
    nomeJogador = "jogador_eu"
    #Definição dos jogadores
    jogador1 = Jogador(nomeJogador)
    jogador2 = Jogador("CPU")
    #Definições das informações das cartas
    nomesNaipes = ["ouros", "espadas", "copas", "paus"]
    pesosNaipes = [1, 2, 3, 4]
    valorCartas = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    pesosCartas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #Definição das cartas
    naipes = [Naipe(nomesNaipes[i], pesosNaipes[i]) for i in range(len(nomesNaipes))]
    cartas = [Carta(valorCartas[i], j, pesosCartas[i]) for i in range(len(valorCartas)) for j in naipes]
    #Definição do jogo
    truco = Jogo(cartas, naipes, jogador1, jogador2)

    print("O jogador \"" + truco.joga() + "\" ganhou a partida!")
