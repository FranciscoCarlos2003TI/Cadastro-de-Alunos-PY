from contextlib import contextmanager
import sqlite3
from pathlib import Path
from collections.abc import Iterator

from cadastro_alunos.aluno import Aluno
from cadastro_alunos.validacoes import normalizar_cpf


class AlunoNaoEncontradoError(LookupError):
    """Indica que não existe aluno com o CPF informado."""


class BancoDeDados:
    def __init__(self, caminho: str | Path | None = None) -> None:
        self.caminho = Path(caminho) if caminho else (
            Path(__file__).resolve().parent.parent / "alunos.db"
        )
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._criar_tabela()

    @contextmanager
    def _conectar(self) -> Iterator[sqlite3.Connection]:
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        try:
            with conexao:
                yield conexao
        finally:
            conexao.close()

    def _criar_tabela(self) -> None:
        with self._conectar() as conexao:
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS alunos (
                    cpf TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL CHECK (idade BETWEEN 1 AND 120),
                    curso TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _para_aluno(registro: sqlite3.Row) -> Aluno:
        return Aluno(
            nome=registro["nome"],
            cpf=registro["cpf"],
            idade=registro["idade"],
            curso=registro["curso"],
        )

    def cadastrar(self, aluno: Aluno) -> None:
        try:
            with self._conectar() as conexao:
                conexao.execute(
                    "INSERT INTO alunos (cpf, nome, idade, curso) VALUES (?, ?, ?, ?)",
                    (normalizar_cpf(aluno.cpf), aluno.nome, aluno.idade, aluno.curso),
                )
        except sqlite3.IntegrityError as erro:
            raise ValueError("Já existe um aluno cadastrado com esse CPF.") from erro

    def listar(self) -> list[Aluno]:
        with self._conectar() as conexao:
            registros = conexao.execute(
                "SELECT cpf, nome, idade, curso FROM alunos ORDER BY nome"
            ).fetchall()
        return [self._para_aluno(registro) for registro in registros]

    def buscar_por_cpf(self, cpf: str) -> Aluno | None:
        cpf_normalizado = normalizar_cpf(cpf)
        with self._conectar() as conexao:
            registro = conexao.execute(
                "SELECT cpf, nome, idade, curso FROM alunos WHERE cpf = ?",
                (cpf_normalizado,),
            ).fetchone()
        return self._para_aluno(registro) if registro else None

    def atualizar(self, cpf_atual: str, aluno: Aluno) -> None:
        cpf_normalizado = normalizar_cpf(cpf_atual)
        novo_cpf = normalizar_cpf(aluno.cpf)
        try:
            with self._conectar() as conexao:
                cursor = conexao.execute(
                    """
                    UPDATE alunos
                    SET cpf = ?, nome = ?, idade = ?, curso = ?
                    WHERE cpf = ?
                    """,
                    (novo_cpf, aluno.nome, aluno.idade, aluno.curso, cpf_normalizado),
                )
                if cursor.rowcount == 0:
                    raise AlunoNaoEncontradoError("Aluno não encontrado.")
        except sqlite3.IntegrityError as erro:
            raise ValueError("Já existe outro aluno cadastrado com esse CPF.") from erro

    def excluir(self, cpf: str) -> bool:
        cpf_normalizado = normalizar_cpf(cpf)
        with self._conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM alunos WHERE cpf = ?", (cpf_normalizado,)
            )
        return cursor.rowcount > 0
