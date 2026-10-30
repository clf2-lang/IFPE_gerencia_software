
def creditar(banco, numero, valor):
    """Adiciona dinheiro ao saldo de uma conta."""
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    conta = banco.localizar_conta(numero)
    conta.saldo += valor


def debitar(banco, numero, valor):
    """Retira dinheiro do saldo de uma conta."""
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    conta = banco.localizar_conta(numero)
    
    # Verifica se há saldo suficiente antes de debitar o valor
    if conta.saldo >= valor:
        conta.saldo -= valor
    else:
        raise ValueError("Saldo insuficiente para debitar o valor solicitado.")
    


def transferir(banco, origem, destino, valor):
    """Transfere dinheiro entre duas contas."""
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    if str(origem).strip() == str(destino).strip():
        raise ValueError("As contas devem ser diferentes.")

    conta_origem = banco.localizar_conta(origem)
    conta_destino = banco.localizar_conta(destino)

    # Verifica se a conta de origem tem saldo suficiente antes de transferir
    if conta_origem.saldo >= valor:
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
    else:
        raise ValueError("Saldo insuficiente para transferir o valor solicitado.")
