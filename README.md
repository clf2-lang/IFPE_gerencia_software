# IFPE_gerencia_software

Sistema bancário desenvolvido em Python para a disciplina de Gerência e Configuração de Software do IFPE.

## Requisitos

- Python 3.9 ou superior.
- Flask.
- Requests.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/clf2-lang/IFPE_gerencia_software.git
```

Entre na pasta do projeto:

```bash
cd IFPE_gerencia_software
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

O sistema bancário permite realizar operações de cadastro, consulta e movimentação de contas.

## Testes unitários

O projeto utiliza a biblioteca `unittest`, integrada ao Python, para testar as operações bancárias.

Para executar os testes, utilize:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam:

- Cadastro de contas.
- Consulta de contas.
- Consulta de saldo.
- Crédito.
- Débito.
- Transferência.
- Rendimento de juros das contas poupança.

## Integração contínua (CI)

O projeto utiliza GitHub Actions para executar verificações automaticamente.

O fluxo de integração contínua é acionado quando ocorre:

- Um `push` na branch `develop`.
- A abertura ou atualização de um Pull Request destinado à branch `develop`.

O processo executa as seguintes etapas:

1. Baixa o código do repositório.
2. Configura o ambiente Python.
3. Instala as dependências.
4. Verifica a sintaxe dos arquivos Python.
5. Executa os testes unitários.

## Organização

- `main.py`: inicia a aplicação.
- `frontend/menu_principal.py`: apresenta o menu e recebe os dados do usuário.
- `backend/api.py`: disponibiliza a API REST.
- `backend/conta.py`: define as classes de contas.
- `backend/banco_base.py`: cadastra, localiza e consulta contas.
- `backend/transacoes.py`: realiza crédito, débito e transferência.
- `tests/test_banco.py`: contém os testes unitários.
- `requirements.txt`: lista as dependências do projeto.
- `.github/workflows/ci.yml`: configura a integração contínua.