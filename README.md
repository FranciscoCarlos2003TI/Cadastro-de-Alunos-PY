# Cadastro de Alunos

Aplicação de linha de comando em Python para cadastrar e administrar alunos
usando SQLite. Não é necessário instalar dependências externas; `sqlite3` faz
parte da biblioteca padrão do Python.

## Requisitos

- Python 3.10 ou superior.

## Como executar

Abra um terminal nesta pasta e execute:

```powershell
python main.py
```

No Windows, se o comando `python` não estiver disponível, tente:

```powershell
py main.py
```

Na primeira execução, o banco `alunos.db` e a tabela de alunos são criados
automaticamente na pasta do projeto. Use o menu para cadastrar, listar,
pesquisar por CPF, atualizar ou excluir alunos.

Os campos do cadastro são nome, CPF, idade e curso. O CPF é validado e
armazenado somente com dígitos; cada CPF pode aparecer uma única vez.

## Executar os testes

```powershell
python -m unittest discover -v
```

## Organização

- `main.py`: ponto de entrada.
- `cadastro_alunos/aluno.py`: modelo de dados `Aluno`.
- `cadastro_alunos/validacoes.py`: validação de nome, CPF, idade e curso.
- `cadastro_alunos/banco_dados.py`: criação do SQLite e operações CRUD.
- `cadastro_alunos/app.py`: menu interativo e tratamento de erros.
- `tests/`: testes automatizados de validação e persistência.
