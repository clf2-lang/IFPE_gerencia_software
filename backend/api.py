from flask import Flask, jsonify, request

from backend.banco_base import BancoBase
from backend.transacoes import creditar, debitar, transferir


app = Flask(__name__)
banco = BancoBase()


@app.post("/banco/conta/")
def cadastrar_conta():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "JSON inválido."}), 400

    try:
        numero = dados.get("numero")
        tipo = dados.get("tipo")
        saldo_inicial = dados.get("saldo_inicial", 0.0)

        if numero is None:
            raise ValueError("O número da conta não pode ficar vazio.")
        if tipo is None:
            raise ValueError("Tipo de conta inválido.")

        try:
            saldo_inicial = float(saldo_inicial)
        except (ValueError, TypeError):
            raise ValueError("O saldo inicial informado não é válido.")
        conta = banco.cadastrar_conta(numero, tipo, saldo_inicial)
        resultado = banco.consultar_conta(conta.numero)
        return jsonify(resultado), 201
    except (ValueError, TypeError) as erro:
        return jsonify({"mensagem": str(erro)}), 400


@app.get("/banco/conta/")
def consultar_conta():
    numero = request.args.get("numero")
    if numero is None or not numero.strip():
        return jsonify({"mensagem": "O número da conta é obrigatório."}), 404

    try:
        resultado = banco.consultar_conta(numero)
        return jsonify(resultado), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404


@app.get("/banco/conta/<id>/saldo")
def consultar_saldo(id):
    try:
        saldo = banco.consultar_saldo(id)
        return jsonify({"saldo": saldo}), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404


@app.put("/banco/conta/<id>/credito")
def realizar_credito(id):
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "JSON inválido."}), 400

    valor = dados.get("valor", dados.get("amount"))
    if valor is None:
        return jsonify({"mensagem": "O valor informado não é válido."}), 400

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return jsonify({"mensagem": "O valor informado não é válido."}), 400

    try:
        banco.localizar_conta(id)
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404

    try:
        creditar(banco, id, valor)
        saldo = banco.consultar_saldo(id)
        return jsonify({"saldo": saldo}), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 400


@app.put("/banco/conta/<id>/debito")
def realizar_debito(id):
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "JSON inválido."}), 400

    valor = dados.get("valor", dados.get("amount"))
    if valor is None:
        return jsonify({"mensagem": "O valor informado não é válido."}), 400

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return jsonify({"mensagem": "O valor informado não é válido."}), 400

    try:
        banco.localizar_conta(id)
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404

    try:
        debitar(banco, id, valor)
        saldo = banco.consultar_saldo(id)
        return jsonify({"saldo": saldo}), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 400


@app.put("/banco/conta/transferencia")
def realizar_transferencia():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "JSON inválido."}), 400

    origem = dados.get("from")
    destino = dados.get("to")
    valor = dados.get("amount")
    if origem is None or destino is None or valor is None:
        return jsonify({"mensagem": "Dados da transferência inválidos."}), 400

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return jsonify({"mensagem": "O valor informado não é válido."}), 400

    try:
        banco.localizar_conta(origem)
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404

    try:
        banco.localizar_conta(destino)
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404

    try:
        transferir(banco, origem, destino, valor)
        return jsonify({"mensagem": "Transferência realizada com sucesso."}), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 400


@app.put("/banco/conta/rendimento")
def realizar_rendimento():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "JSON inválido."}), 400

    numero = dados.get("numero", dados.get("conta"))
    taxa = dados.get("taxa")
    if numero is None or taxa is None:
        return jsonify({"mensagem": "Dados do rendimento inválidos."}), 400

    try:
        taxa = float(taxa)
    except (ValueError, TypeError):
        return jsonify({"mensagem": "A taxa informada não é válida."}), 400

    try:
        banco.localizar_conta(numero)
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 404

    try:
        banco.render_juros(numero, taxa)
        resultado = banco.consultar_conta(numero)
        return jsonify(resultado), 200
    except ValueError as erro:
        return jsonify({"mensagem": str(erro)}), 400
