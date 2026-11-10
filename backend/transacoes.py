
def creditar(banco, numero, valor):
    # Verifica se o valor é positivo antes de creditar
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    conta = banco.localizar_conta(numero)
    conta.saldo += valor

    # Conta Bônus ganha 1 ponto a cada R$ 100 depositados
    if hasattr(conta, "pontuacao"):
        conta.pontuacao += int(valor / 100)


def debitar(banco, numero, valor):
    # Verifica se há saldo suficiente antes de debitar o valor
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    conta = banco.localizar_conta(numero)

    if conta.saldo < valor:
        raise ValueError("Saldo insuficiente para debitar o valor solicitado.")

    conta.saldo -= valor


def transferir(banco, origem, destino, valor):
    # Verifica se o valor é positivo antes de transferir
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    if str(origem).strip() == str(destino).strip():
        raise ValueError("As contas devem ser diferentes.")

    conta_origem = banco.localizar_conta(origem)
    conta_destino = banco.localizar_conta(destino)

    if conta_origem.saldo < valor:
        raise ValueError("Saldo insuficiente para transferir o valor solicitado.")

    conta_origem.saldo -= valor
    conta_destino.saldo += valor

    # Conta Bônus ganha 1 ponto a cada R$ 150 recebidos
    if hasattr(conta_destino, "pontuacao"):
        conta_destino.pontuacao += int(valor / 150)
