from truco import Truco
import truco

if __name__ == "__main__":
    naipes = ["ouros", "espadas", "copas", "paus"]
    nome = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    valores =[1,2,3,4,5,6,7,8,9,10]


    jogoTruco = Truco(naipes, nome, valores)

    jogoTruco.jogo()
    #jogoTruco.criaBaralho()

    # jogoTruco.printaBaralho()

    #jogoTruco.embaralhaBaralho()

    #jogoTruco.printaBaralho()

    #jogoTruco.distribuiCartas()

    #jogoTruco.printaMao()

    #jogoTruco.limpaMao()

    #jogoTruco.printaMao()

    #truco.jogo()
