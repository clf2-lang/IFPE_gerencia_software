import requests


API_URL = "http://127.0.0.1:5000"


# Interface principal do sistema bancario
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


def _chamar_api(method, caminho, **kwargs):
    try:
        resposta = requests.request(
            method,
            f"{API_URL}{caminho}",
            timeout=5,
            **kwargs
        )
    except requests.RequestException:
        raise ValueError("Não foi possível conectar ao servidor.")

    dados = resposta.json() if resposta.content else {}
    if resposta.status_code in (400, 404):
        raise ValueError(dados.get("mensagem", "Operação não realizada."))
    if not resposta.ok:
        raise ValueError("Erro ao comunicar com o servidor.")
    return dados


def _cadastrar_conta():
    numero = _ler_numero_conta("Número da conta: ")
    print("1 - Conta Corrente")
    print("2 - Conta Bônus")
    print("3 - Conta Poupança")
    opcao = input("Escolha o tipo de conta: ").strip()
    tipos = {
        "1": "corrente",
        "2": "bonus",
        "3": "poupanca",
    }
    tipo = tipos.get(opcao)
    if tipo is None:
        raise ValueError("Tipo de conta inválido.")

    dados = {"numero": numero, "tipo": tipo}
    if tipo == "poupanca":
        saldo_inicial = _ler_valor("Saldo inicial da conta Poupança: ")
        dados["saldo_inicial"] = saldo_inicial

    conta = _chamar_api("POST", "/banco/conta/", json=dados)
    print(f"Conta {conta['numero']} cadastrada com saldo R$ {conta['saldo']:.2f}.")


def _consultar_saldo():
    numero = _ler_numero_conta("Número da conta: ")
    dados = _chamar_api("GET", f"/banco/conta/{numero}/saldo")
    print(f"Saldo da conta {numero}: R$ {dados['saldo']:.2f}.")


def _consultar_conta():
    numero = _ler_numero_conta("Número da conta: ")
    dados = _chamar_api("GET", "/banco/conta/", params={"numero": numero})
    print(f"Tipo: {dados['tipo']}")
    print(f"Número: {dados['numero']}")
    print(f"Saldo: R$ {dados['saldo']:.2f}")
    if "bonus" in dados:
        print(f"Bônus: {dados['bonus']}")


def _realizar_credito():
    numero = _ler_numero_conta("Número da conta: ")
    valor = _ler_valor("Valor do crédito: ")
    dados = _chamar_api(
        "PUT",
        f"/banco/conta/{numero}/credito",
        json={"valor": valor},
    )
    print(f"Crédito realizado. Saldo atual: R$ {dados['saldo']:.2f}.")


def _realizar_debito():
    numero = _ler_numero_conta("Número da conta: ")
    valor = _ler_valor("Valor do débito: ")
    dados = _chamar_api(
        "PUT",
        f"/banco/conta/{numero}/debito",
        json={"valor": valor},
    )
    print(f"Débito realizado. Saldo atual: R$ {dados['saldo']:.2f}.")


def _realizar_transferencia():
    origem = _ler_numero_conta("Conta de origem: ")
    destino = _ler_numero_conta("Conta de destino: ")
    valor = _ler_valor("Valor da transferência: ")
    _chamar_api(
        "PUT",
        "/banco/conta/transferencia",
        json={"from": origem, "to": destino, "amount": valor},
    )
    print("Transferência realizada com sucesso.")


def _render_juros():
    numero = _ler_numero_conta("Número da conta Poupança: ")
    taxa = _ler_valor("Taxa de juros (%): ")
    dados = _chamar_api(
        "PUT",
        "/banco/conta/rendimento",
        json={"numero": numero, "taxa": taxa},
    )
    print(
        f"Juros aplicados com sucesso. Saldo atual: "
        f"R$ {dados['saldo']:.2f}."
    )


def _mostrar_menu():
    print("\n=== Sistema Bancário IFPE ===")
    print("1. Cadastrar conta")
    print("2. Consultar saldo")
    print("3. Crédito")
    print("4. Débito")
    print("5. Transferência")
    print("6. Render Juros")
    print("7. Consultar conta")
    print("0. Sair")


def executar_menu():
    operacoes = {
        "1": _cadastrar_conta,
        "2": _consultar_saldo,
        "3": _realizar_credito,
        "4": _realizar_debito,
        "5": _realizar_transferencia,
        "6": _render_juros,
        "7": _consultar_conta,
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
            operacao()
        except ValueError as erro:
            print(f"Operação não realizada: {erro}")
