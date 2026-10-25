from backend.banco_base import BancoBase
#from backend.transacoes import creditar, debitar, transferir

# Interface principal do sistema bancário
def _ler_numero_conta(mensagem):
    numero = input(mensagem).strip()
    if not numero:
        raise ValueError("O número da conta não pode ficar vazio.")
    return numero


def _ler_valor(mensagem):
    entrada = input(mensagem).strip().replace(",", ".")
    try:
        valor = float(entrada)
    except ValueError as erro:
        raise ValueError("O valor informado não é válido.") from erro
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    return valor


def _cadastrar_conta(banco):
    numero = _ler_numero_conta("Número da conta: ")
    conta = banco.cadastrar_conta(numero)
    print(f"Conta {conta.numero} cadastrada com saldo R$ {conta.saldo:.2f}.")


def _consultar_saldo(banco):
    numero = _ler_numero_conta("Número da conta: ")
    saldo = banco.consultar_saldo(numero)
    print(f"Saldo da conta {numero}: R$ {saldo:.2f}.")


def _realizar_credito(banco):
    numero = _ler_numero_conta("Número da conta: ")
    valor = _ler_valor("Valor do crédito: ")
    creditar(banco, numero, valor)
    print(f"Crédito realizado. Saldo atual: R$ {banco.consultar_saldo(numero):.2f}.")


def _realizar_debito(banco):
    numero = _ler_numero_conta("Número da conta: ")
    valor = _ler_valor("Valor do débito: ")
    debitar(banco, numero, valor)
    print(f"Débito realizado. Saldo atual: R$ {banco.consultar_saldo(numero):.2f}.")


def _realizar_transferencia(banco):
    origem = _ler_numero_conta("Conta de origem: ")
    destino = _ler_numero_conta("Conta de destino: ")
    valor = _ler_valor("Valor da transferência: ")
    transferir(banco, origem, destino, valor)
    print("Transferência realizada com sucesso.")


def _mostrar_menu():
    print("\n=== Sistema Bancário IFPE ===")
    print("1. Cadastrar conta")
    print("2. Consultar saldo")
    print("3. Crédito")
    print("4. Débito")
    print("5. Transferência")
    print("0. Sair")


def executar_menu():
    banco = BancoBase()
    operacoes = {
        "1": _cadastrar_conta,
        "2": _consultar_saldo,
        "3": _realizar_credito,
        "4": _realizar_debito,
        "5": _realizar_transferencia,
    }
    while True:
        _mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Aplicação encerrada.")
            return
        operacao = operacoes.get(opcao)
        if operacao is None:
            print("Opção inválida.")
            continue
        try:
            operacao(banco)
        except ValueError as erro:
            print(f"Operação não realizada: {erro}")
