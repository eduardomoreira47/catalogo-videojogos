
from app.database.database import obter_conexao


def guardar_jogo(titulo, descricao, ano_lancamento, capa=None):
    """Guarda um videojogo na base de dados."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO JOGO (titulo, descricao, ano_lancamento, capa)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, ano_lancamento, capa)
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
            SELECT id_jogo, titulo, descricao, ano_lancamento, capa
            FROM JOGO
            ORDER BY titulo ASC
            """
        )

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def pesquisar_jogos(titulo, ano_lancamento=None):
    """Pesquisa videojogos pelo título e, opcionalmente, pelo ano."""

    conexao = obter_conexao()

    try:
        consulta = """
            SELECT id_jogo, titulo, descricao, ano_lancamento, capa
            FROM JOGO
            WHERE titulo LIKE ?
        """

        parametros = [f"%{titulo.strip()}%"]

        if ano_lancamento is not None:
            consulta += " AND ano_lancamento = ?"
            parametros.append(ano_lancamento)

        consulta += " ORDER BY titulo ASC"

        cursor = conexao.execute(consulta, parametros)

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def obter_jogo_por_id(id_jogo):
    """Devolve um videojogo específico através do seu ID."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT id_jogo, titulo, descricao, ano_lancamento, capa
            FROM JOGO
            WHERE id_jogo = ?
            """,
            (id_jogo,)
        )

        linha = cursor.fetchone()

        return dict(linha) if linha else None

    finally:
        conexao.close()


def atualizar_jogo(id_jogo, titulo, descricao, ano_lancamento, capa=None):
    """Atualiza os dados de um videojogo existente."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            UPDATE JOGO
            SET titulo = ?,
                descricao = ?,
                ano_lancamento = ?,
                capa = ?
            WHERE id_jogo = ?
            """,
            (titulo, descricao, ano_lancamento, capa, id_jogo)
        )

        conexao.commit()

        return cursor.rowcount > 0

    finally:
        conexao.close()


def eliminar_jogo(id_jogo):
    """Elimina um videojogo da base de dados."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            DELETE FROM JOGO
            WHERE id_jogo = ?
            """,
            (id_jogo,)
        )

        conexao.commit()

        return cursor.rowcount > 0

    finally:
        conexao.close()
