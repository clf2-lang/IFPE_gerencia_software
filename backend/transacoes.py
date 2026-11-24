from backend.banco_base import BancoBase


def creditar(banco, numero, valor):
    if valor <= 0:
        raise ValueError("O valor do crédito deve ser positivo.")

    conta = banco.localizar_conta(numero)
    conta.saldo += valor

    if hasattr(conta, "pontuacao"):
        conta.pontuacao += int(valor / 100)


def debitar(banco, numero, valor):
    if valor <= 0:
        raise ValueError("O valor do débito deve ser positivo.")

    conta = banco.localizar_conta(numero)

    if conta.saldo - valor < getattr(conta, "limite", 0.0):
        raise ValueError("O limite de saldo negativo foi ultrapassado.")

    conta.saldo -= valor


def transferir(banco, origem, destino, valor):
    if valor <= 0:
        raise ValueError("O valor da transferência deve ser positivo.")

    if str(origem).strip() == str(destino).strip():
        raise ValueError("A conta de origem e destino devem ser diferentes.")

    conta_origem = banco.localizar_conta(origem)
    conta_destino = banco.localizar_conta(destino)

    if conta_origem.saldo - valor < getattr(conta_origem, "limite", 0.0):
        raise ValueError("O limite de saldo negativo foi ultrapassado.")

    conta_origem.saldo -= valor
    conta_destino.saldo += valor

    if hasattr(conta_destino, "pontuacao"):
        conta_destino.pontuacao += int(valor / 200)