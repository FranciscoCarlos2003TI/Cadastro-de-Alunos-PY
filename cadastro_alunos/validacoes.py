import re


def validar_nome(nome: str) -> str:
    nome = nome.strip()
    if len(nome) < 2:
        raise ValueError("O nome deve ter pelo menos 2 caracteres.")
    return nome


def normalizar_cpf(cpf: str) -> str:
    digitos = re.sub(r"\D", "", cpf)
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        raise ValueError("CPF inválido. Informe os 11 dígitos corretamente.")

    soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
    primeiro = (soma * 10 % 11) % 10
    soma = sum(int(digitos[i]) * (11 - i) for i in range(10))
    segundo = (soma * 10 % 11) % 10

    if digitos[-2:] != f"{primeiro}{segundo}":
        raise ValueError("CPF inválido. Confira os dígitos verificadores.")
    return digitos


def validar_idade(idade: int | str) -> int:
    try:
        idade_numero = int(idade)
    except (TypeError, ValueError) as erro:
        raise ValueError("A idade deve ser um número inteiro.") from erro

    if not 1 <= idade_numero <= 120:
        raise ValueError("A idade deve estar entre 1 e 120 anos.")
    return idade_numero


def validar_curso(curso: str) -> str:
    curso = curso.strip()
    if not curso:
        raise ValueError("O curso não pode ficar vazio.")
    return curso
