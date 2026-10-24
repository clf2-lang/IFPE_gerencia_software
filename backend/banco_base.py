
from backend.conta import Conta

class BancoBase:
    def __init__(self):
        self._contas = {}

    def cadastrar_conta(self, numero):
        numero = str(numero).strip()
        if not numero:
            raise ValueError("O número da conta não pode ficar vazio.")
        if numero in self._contas:
            raise ValueError("Já existe uma conta com esse número.")
        conta = Conta(numero)
        self._contas[numero] = conta
        return conta
