class Conta:
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 0.0


class ContaBonus(Conta):
    def __init__(self, numero):
        super().__init__(numero)
        self.pontuacao = 10


class ContaPoupanca(Conta):
    def __init__(self, numero, saldo_inicial=0.0):
        super().__init__(numero)
        self.saldo = saldo_inicial

    def render_juros(self, taxa):
        juros = self.saldo * (taxa / 100)
        self.saldo += juros