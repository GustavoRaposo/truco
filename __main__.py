from truco import Truco

if __name__ == "__main__":
    naipes = ["ouros", "espadas", "copas", "paus"]
    valores = ["A", "2", "3", "4", "5", "6", "7", "Q", "J", "K"]

    jogoTruco = Truco(naipes, valores)

    jogoTruco.criaBaralho()

    jogoTruco.embaralhaBaralho()

    jogoTruco.printaBaralho()

    jogoTruco.distribuiCartas()

    jogoTruco.printaMao()

    jogoTruco.jogo()
