import tempfile
import unittest
from pathlib import Path

from cadastro_alunos.aluno import Aluno
from cadastro_alunos.banco_dados import BancoDeDados
from cadastro_alunos.validacoes import normalizar_cpf, validar_idade, validar_nome


class ValidacoesTest(unittest.TestCase):
    def test_normaliza_cpf_valido(self) -> None:
        self.assertEqual(normalizar_cpf("529.982.247-25"), "52998224725")

    def test_rejeita_cpf_invalido(self) -> None:
        with self.assertRaises(ValueError):
            normalizar_cpf("111.111.111-11")

    def test_valida_nome_e_idade(self) -> None:
        self.assertEqual(validar_nome("  Ana Silva  "), "Ana Silva")
        self.assertEqual(validar_idade("20"), 20)
        with self.assertRaises(ValueError):
            validar_idade("0")


class BancoDeDadosTest(unittest.TestCase):
    def setUp(self) -> None:
        self.diretorio = tempfile.TemporaryDirectory()
        caminho = Path(self.diretorio.name) / "teste.db"
        self.banco = BancoDeDados(caminho)
        self.aluno = Aluno("Ana Silva", "52998224725", 20, "Engenharia")

    def tearDown(self) -> None:
        self.diretorio.cleanup()

    def test_cadastro_pesquisa_atualizacao_e_exclusao(self) -> None:
        self.banco.cadastrar(self.aluno)
        self.assertEqual(self.banco.buscar_por_cpf(self.aluno.cpf), self.aluno)
        self.assertEqual(self.banco.listar(), [self.aluno])

        atualizado = Aluno("Ana Souza", self.aluno.cpf, 21, "Computação")
        self.banco.atualizar(self.aluno.cpf, atualizado)
        self.assertEqual(self.banco.buscar_por_cpf(self.aluno.cpf), atualizado)

        self.assertTrue(self.banco.excluir(self.aluno.cpf))
        self.assertIsNone(self.banco.buscar_por_cpf(self.aluno.cpf))
        self.assertFalse(self.banco.excluir(self.aluno.cpf))

    def test_rejeita_cpf_duplicado(self) -> None:
        self.banco.cadastrar(self.aluno)
        with self.assertRaisesRegex(ValueError, "Já existe"):
            self.banco.cadastrar(self.aluno)


if __name__ == "__main__":
    unittest.main()
