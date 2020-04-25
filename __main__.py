from truco import Truco
import truco

if __name__ == "__main__":
    naipes = ["ouros", "espadas", "copas", "paus"]
    valores = ["A", "2", "3", "4", "5", "6", "7", "Q", "J", "K"]

    jogoTruco = Truco(naipes, valores)

    jogoTruco.criaBaralho()

    # jogoTruco.printaBaralho()

    jogoTruco.embaralhaBaralho()

    jogoTruco.printaBaralho()

    jogoTruco.limpaMao()

    jogoTruco.printaMao()

    truco.jogo()
