class Conta:
    def __init__(self, numero, saldo_inicial):
        self.numero = numero
        self.saldo = saldo_inicial


class ContaBonus(Conta):
    def __init__(self, numero):
        super().__init__(numero, 0.0)
        self.pontuacao = 10


class ContaPoupanca(Conta):
    def __init__(self, numero):
        super().__init__(numero, 0.0)

    def render_juros(self, taxa):
        juros = self.saldo * (taxa / 100)
        self.saldo += juros