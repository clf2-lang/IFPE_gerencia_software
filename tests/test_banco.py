
import unittest

from backend.banco_base import BancoBase

from backend.transacoes import creditar, debitar, transferir

class TestCadastroConta(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()

    def test_cadastrar_conta_corrente(self):
        conta = self.banco.cadastrar_conta("123", "corrente")

        self.assertEqual(conta.numero, "123")
        self.assertEqual(conta.saldo, 0.0)

    def test_cadastrar_conta_bonus(self):
        conta = self.banco.cadastrar_conta("456", "bonus")

        self.assertEqual(conta.numero, "456")
        self.assertEqual(conta.saldo, 0.0)
        self.assertEqual(conta.pontuacao, 10)

    def test_cadastrar_conta_poupanca(self):
        conta = self.banco.cadastrar_conta(
            "789", "poupanca", 500.0
        )

        self.assertEqual(conta.numero, "789")
        self.assertEqual(conta.saldo, 500.0)

    def test_cadastrar_conta_numero_duplicado(self):
        self.banco.cadastrar_conta("123", "corrente")

        with self.assertRaises(ValueError):
            self.banco.cadastrar_conta("123", "bonus")

    def test_cadastrar_conta_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.banco.cadastrar_conta("999", "invalida")



class TestConsultaConta(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()

    def test_consultar_conta_corrente(self):
        self.banco.cadastrar_conta("123", "corrente")

        dados = self.banco.consultar_conta("123")

        self.assertEqual(dados["tipo"], "corrente")
        self.assertEqual(dados["numero"], "123")
        self.assertEqual(dados["saldo"], 0.0)
        self.assertNotIn("bonus", dados)

    def test_consultar_conta_bonus(self):
        self.banco.cadastrar_conta("456", "bonus")

        dados = self.banco.consultar_conta("456")

        self.assertEqual(dados["tipo"], "bonus")
        self.assertEqual(dados["numero"], "456")
        self.assertEqual(dados["saldo"], 0.0)
        self.assertEqual(dados["bonus"], 10)

    def test_consultar_conta_poupanca(self):
        self.banco.cadastrar_conta("789", "poupanca", 500.0)

        dados = self.banco.consultar_conta("789")

        self.assertEqual(dados["tipo"], "poupanca")
        self.assertEqual(dados["numero"], "789")
        self.assertEqual(dados["saldo"], 500.0)
        self.assertNotIn("bonus", dados)



class TestConsultaSaldo(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()

    def test_consultar_saldo(self):
        self.banco.cadastrar_conta("123", "corrente")

        creditar_saldo = 150.0
        self.banco.localizar_conta("123").saldo = creditar_saldo

        saldo = self.banco.consultar_saldo("123")

        self.assertEqual(saldo, 150.0)

    def test_consultar_saldo_conta_inexistente(self):
        with self.assertRaises(ValueError):
            self.banco.consultar_saldo("999")



class TestCredito(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()

    def test_credito_normal(self):
        self.banco.cadastrar_conta("123", "corrente")

        creditar(self.banco, "123", 100.0)

        self.assertEqual(
            self.banco.consultar_saldo("123"), 100.0
        )

    def test_credito_valor_negativo(self):
        self.banco.cadastrar_conta("123", "corrente")

        with self.assertRaises(ValueError):
            creditar(self.banco, "123", -50.0)

    def test_credito_conta_bonus(self):
        self.banco.cadastrar_conta("456", "bonus")

        creditar(self.banco, "456", 200.0)

        dados = self.banco.consultar_conta("456")

        self.assertEqual(dados["saldo"], 200.0)
        self.assertEqual(dados["bonus"], 12)



class TestDebito(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()

    def test_debito_normal(self):
        self.banco.cadastrar_conta("123", "corrente")
        creditar(self.banco, "123", 500.0)

        debitar(self.banco, "123", 200.0)

        self.assertEqual(
            self.banco.consultar_saldo("123"), 300.0
        )

    def test_debito_valor_negativo(self):
        self.banco.cadastrar_conta("123", "corrente")

        with self.assertRaises(ValueError):
            debitar(self.banco, "123", -50.0)

    def test_debito_saldo_insuficiente(self):
        self.banco.cadastrar_conta("123", "corrente")

        with self.assertRaises(ValueError):
            debitar(self.banco, "123", 1100.0)

        self.assertEqual(
            self.banco.consultar_saldo("123"), 0.0
        )


class TestTransferencia(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()
        self.banco.cadastrar_conta("123", "corrente")
        self.banco.cadastrar_conta("456", "corrente")
        creditar(self.banco, "123", 500.0)

    def test_transferencia_normal(self):
        transferir(self.banco, "123", "456", 200.0)

        self.assertEqual(
            self.banco.consultar_saldo("123"), 300.0
        )
        self.assertEqual(
            self.banco.consultar_saldo("456"), 200.0
        )

    def test_transferencia_valor_negativo(self):
        with self.assertRaises(ValueError):
            transferir(self.banco, "123", "456", -50.0)

    def test_transferencia_limite_excedido(self):
        with self.assertRaises(ValueError):
            transferir(self.banco, "123", "456", 1501.0)

        self.assertEqual(
            self.banco.consultar_saldo("123"), 500.0
        )
        self.assertEqual(
            self.banco.consultar_saldo("456"), 0.0
        )

    def test_transferencia_conta_bonus(self):
        self.banco.cadastrar_conta("789", "bonus")

        transferir(self.banco, "123", "789", 200.0)

        conta = self.banco.localizar_conta("789")

        self.assertEqual(conta.saldo, 200.0)
        self.assertEqual(conta.pontuacao, 11)


class TestRenderJuros(unittest.TestCase):

    def setUp(self):
        self.banco = BancoBase()
        self.banco.cadastrar_conta("123", "poupanca", 1000.0)
        self.banco.cadastrar_conta("456", "poupanca", 2000.0)

    def test_render_juros_conta_poupanca(self):
        self.banco.render_juros("123", 10)

        self.assertAlmostEqual(
            self.banco.consultar_saldo("123"), 1100.0
        )

    def test_render_juros_outra_conta_poupanca(self):
        self.banco.render_juros("456", 5)

        self.assertAlmostEqual(
            self.banco.consultar_saldo("456"), 2100.0
        )


if __name__ == "__main__":
    unittest.main()
