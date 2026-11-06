
import sqlite3
import pytest

from app import repositorio
from app.services import jogos as servico_jogos


@pytest.fixture
def preparar_base_dados(tmp_path, monkeypatch):
    """Cria uma base de dados temporária para os testes."""

    caminho_bd = tmp_path / "catalogo_teste.db"

    def obter_conexao_teste():
        conexao = sqlite3.connect(caminho_bd)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    monkeypatch.setattr(
        repositorio,
        "obter_conexao",
        obter_conexao_teste
    )

    conexao = obter_conexao_teste()

    conexao.execute("""
        CREATE TABLE JOGO (
            id_jogo INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            descricao TEXT,
            ano_lancamento INTEGER,
            capa TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def test_registar_jogo(preparar_base_dados):
    """Verifica se é possível registar um videojogo."""

    id_jogo = servico_jogos.criar_jogo(
        "Minecraft",
        "Jogo de construção.",
        2011
    )

    assert id_jogo is not None

    jogo = servico_jogos.obter_jogo(id_jogo)

    assert jogo["titulo"] == "Minecraft"
    assert jogo["ano_lancamento"] == 2011


def test_listar_jogos(preparar_base_dados):
    """Verifica se os videojogos são apresentados."""

    servico_jogos.criar_jogo("Minecraft", "Construção.", 2011)
    servico_jogos.criar_jogo("FIFA", "Futebol.", 2023)

    jogos = servico_jogos.obter_jogos()

    assert len(jogos) == 2


def test_pesquisar_jogos_por_titulo(preparar_base_dados):
    """Verifica a pesquisa pelo título."""

    servico_jogos.criar_jogo("Minecraft", "Construção.", 2011)
    servico_jogos.criar_jogo("FIFA", "Futebol.", 2023)

    resultados = servico_jogos.pesquisar_jogos("Mine")

    assert len(resultados) == 1
    assert resultados[0]["titulo"] == "Minecraft"


def test_filtrar_jogos_por_ano(preparar_base_dados):
    """Verifica o filtro pelo ano de lançamento."""

    servico_jogos.criar_jogo("Minecraft", "Construção.", 2011)
    servico_jogos.criar_jogo("FIFA", "Futebol.", 2023)

    resultados = servico_jogos.pesquisar_jogos("", 2023)

    assert len(resultados) == 1
    assert resultados[0]["titulo"] == "FIFA"


def test_editar_jogo(preparar_base_dados):
    """Verifica se é possível editar um videojogo."""

    id_jogo = servico_jogos.criar_jogo(
        "FIFA",
        "Futebol.",
        2023
    )

    servico_jogos.editar_jogo(
        id_jogo,
        "EA Sports FC",
        "Futebol atualizado.",
        2024
    )

    jogo = servico_jogos.obter_jogo(id_jogo)

    assert jogo["titulo"] == "EA Sports FC"
    assert jogo["ano_lancamento"] == 2024


def test_eliminar_jogo(preparar_base_dados):
    """Verifica se é possível eliminar um videojogo."""

    id_jogo = servico_jogos.criar_jogo(
        "Minecraft",
        "Construção.",
        2011
    )

    servico_jogos.remover_jogo(id_jogo)

    jogo = servico_jogos.obter_jogo(id_jogo)

    assert jogo is None
