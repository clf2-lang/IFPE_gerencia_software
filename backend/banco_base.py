from backend.conta import Conta, ContaBonus, ContaPoupanca

class BancoBase:
    def __init__(self):
        self.contas = []

    def cadastrar_conta(self, numero, tipo):
        numero = str(numero).strip()
        if not numero:
            raise ValueError("O número da conta não pode ficar vazio.")
        if any(conta.numero == numero for conta in self.contas):
            raise ValueError("Já existe uma conta com esse número.")

        if tipo == "corrente":
            conta = Conta(numero)
        elif tipo == "bonus":
            conta = ContaBonus(numero)
        elif tipo == "poupanca":
            conta = ContaPoupanca(numero)
        else:
            raise ValueError("Tipo de conta inválido.")

        self.contas.append(conta)
        return conta
    
    def localizar_conta(self, numero):
        numero = str(numero).strip()
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        raise ValueError(f"A conta {numero} não existe.")

    def consultar_saldo(self, numero):
        return self.localizar_conta(numero).saldo

    def render_juros(self, numero, taxa):
        conta = self.localizar_conta(numero)
        if isinstance(conta, ContaPoupanca):
            conta.render_juros(taxa)
