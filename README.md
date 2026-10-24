# IFPE_gerencia_software

Sistema bancário simples executado pelo terminal para a disciplina de
Gerência e Configuração de Software do IFPE.

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Execução

Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

O menu oferece somente as cinco operações bancárias previstas:

1. Cadastrar conta
2. Consultar saldo
3. Crédito
4. Débito
5. Transferência
0. Sair

As contas são mantidas em memória e começam com saldo `0.00`. O sistema
permite saldo negativo e encerra os dados ao finalizar a execução.

## Organização

- `main.py`: inicia a aplicação.
- `frontend/menu_principal.py`: apresenta o menu, recebe dados e exibe os
  resultados.
- `backend/conta.py`: define a classe `Conta`.
- `backend/banco_base.py`: cadastra, localiza e consulta contas.
- `backend/transacoes.py`: realiza crédito, débito e transferência.
