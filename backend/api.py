from flask import Flask, jsonify, request

from backend.banco_base import BancoBase


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
