from app.database.database import obter_conexao


def criar_jogo(titulo, descricao, ano_lancamento):
    """Regista um videojogo na base de dados."""

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