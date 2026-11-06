from dataclasses import dataclass


@dataclass(frozen=True)
class Aluno:
    nome: str
    cpf: str
    idade: int
    curso: str

