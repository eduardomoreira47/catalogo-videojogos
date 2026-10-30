from app.database.database import obter_conexao


def guardar_jogo(titulo, descricao, ano_lancamento):
    """Guarda um videojogo na base de dados."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO JOGO (titulo, descricao, ano_lancamento)
            VALUES (?, ?, ?)
            """,
            (titulo, descricao, ano_lancamento)
        )

        conexao.commit()

        return cursor.lastrowid

    finally:
        conexao.close()


def listar_jogos():
    """Devolve os videojogos guardados, ordenados pelo título."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT id_jogo, titulo, descricao, ano_lancamento
            FROM JOGO
            ORDER BY titulo ASC
            """
        )

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def limpar_jogos_de_teste():
    """Remove os registos de teste identificados no catálogo."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            DELETE FROM JOGO
            WHERE titulo IN (?, ?, ?)
            """,
            (
                "coloca apenas três espaços.",
                "teste",
                "três espaços"
            )
        )

        conexao.commit()

        return cursor.rowcount

    finally:
        conexao.close()