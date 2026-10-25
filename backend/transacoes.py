class Conta:
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 0.0
class Transacoes:
    def __init__(self, contas):
        self.contas = contas

    def credito(self, numero, valor):
        conta = self.contas.get(numero)

        if conta is None:
            print("Conta não encontrada.")
            return False

        if valor <= 0:
            print("O valor deve ser maior que zero.")
            return False

        conta.saldo += valor

        print("Crédito realizado com sucesso!")
        print(f"Novo saldo: R$ {conta.saldo:.2f}")
        return True

    def debito(self, numero, valor):
        conta = self.contas.get(numero)

        if conta is None:
            print("Conta não encontrada.")
            return False

        if valor <= 0:
            print("O valor deve ser maior que zero.")
            return False

        conta.saldo -= valor

        print("Débito realizado com sucesso!")
        print(f"Novo saldo: R$ {conta.saldo:.2f}")
        return True

    def transferir(self, origem_numero, destino_numero, valor):
        origem = self.contas.get(origem_numero)
        destino = self.contas.get(destino_numero)

        if origem is None:
            print("Conta de origem não encontrada.")
            return False

        if destino is None:
            print("Conta de destino não encontrada.")
            return False

        if valor <= 0:
            print("O valor deve ser maior que zero.")
            return False

        origem.saldo -= valor
        destino.saldo += valor

        print("Transferência realizada com sucesso!")
        return True
