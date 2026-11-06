import sqlite3

from cadastro_alunos.aluno import Aluno
from cadastro_alunos.banco_dados import AlunoNaoEncontradoError, BancoDeDados
from cadastro_alunos.validacoes import (
    normalizar_cpf,
    validar_curso,
    validar_idade,
    validar_nome,
)


def _ler_aluno() -> Aluno:
    nome = validar_nome(input("Nome: "))
    cpf = normalizar_cpf(input("CPF: "))
    idade = validar_idade(input("Idade: "))
    curso = validar_curso(input("Curso: "))
    return Aluno(nome=nome, cpf=cpf, idade=idade, curso=curso)


def _exibir_aluno(aluno: Aluno) -> None:
    cpf_formatado = (
        f"{aluno.cpf[:3]}.{aluno.cpf[3:6]}.{aluno.cpf[6:9]}-{aluno.cpf[9:]}"
    )
    print(
        f"Nome: {aluno.nome} | CPF: {cpf_formatado} | "
        f"Idade: {aluno.idade} | Curso: {aluno.curso}"
    )


def _cadastrar(banco: BancoDeDados) -> None:
    aluno = _ler_aluno()
    banco.cadastrar(aluno)
    print("Aluno cadastrado com sucesso.")


def _listar(banco: BancoDeDados) -> None:
    alunos = banco.listar()
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for aluno in alunos:
        _exibir_aluno(aluno)


def _pesquisar(banco: BancoDeDados) -> None:
    cpf = normalizar_cpf(input("CPF para pesquisa: "))
    aluno = banco.buscar_por_cpf(cpf)
    if aluno is None:
        print("Aluno não encontrado.")
    else:
        _exibir_aluno(aluno)


def _atualizar(banco: BancoDeDados) -> None:
    cpf_atual = normalizar_cpf(input("CPF do aluno que deseja atualizar: "))
    aluno_atual = banco.buscar_por_cpf(cpf_atual)
    if aluno_atual is None:
        print("Aluno não encontrado.")
        return

    print("Pressione Enter para manter o valor atual.")
    nome = input(f"Nome [{aluno_atual.nome}]: ").strip() or aluno_atual.nome
    cpf = input(f"CPF [{aluno_atual.cpf}]: ").strip() or aluno_atual.cpf
    idade = input(f"Idade [{aluno_atual.idade}]: ").strip() or str(aluno_atual.idade)
    curso = input(f"Curso [{aluno_atual.curso}]: ").strip() or aluno_atual.curso
    aluno_novo = Aluno(
        nome=validar_nome(nome),
        cpf=normalizar_cpf(cpf),
        idade=validar_idade(idade),
        curso=validar_curso(curso),
    )
    banco.atualizar(cpf_atual, aluno_novo)
    print("Cadastro atualizado com sucesso.")


def _excluir(banco: BancoDeDados) -> None:
    cpf = normalizar_cpf(input("CPF do aluno que deseja excluir: "))
    if banco.excluir(cpf):
        print("Aluno excluído com sucesso.")
    else:
        print("Aluno não encontrado.")


def executar() -> None:
    try:
        banco = BancoDeDados()
    except sqlite3.Error as erro:
        print(f"Não foi possível iniciar o banco de dados: {erro}")
        return

    operacoes = {
        "1": ("Cadastrar aluno", _cadastrar),
        "2": ("Listar alunos", _listar),
        "3": ("Pesquisar aluno por CPF", _pesquisar),
        "4": ("Atualizar aluno", _atualizar),
        "5": ("Excluir aluno", _excluir),
    }

    while True:
        print(
            "\n=== Cadastro de Alunos ===\n"
            "1. Cadastrar aluno\n"
            "2. Listar alunos\n"
            "3. Pesquisar aluno por CPF\n"
            "4. Atualizar aluno\n"
            "5. Excluir aluno\n"
            "0. Sair"
        )
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Aplicação encerrada.")
            break
        operacao = operacoes.get(opcao)
        if operacao is None:
            print("Opção inválida. Escolha uma opção de 0 a 5.")
            continue

        try:
            operacao[1](banco)
        except ValueError as erro:
            print(f"Dados inválidos: {erro}")
        except AlunoNaoEncontradoError as erro:
            print(str(erro))
        except sqlite3.Error as erro:
            print(f"Erro ao acessar o banco de dados: {erro}")

