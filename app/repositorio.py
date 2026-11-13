
from app.database.database import obter_conexao


def obter_generos():
    """Devolve todos os géneros disponíveis."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT id_genero, nome
            FROM GENERO
            ORDER BY nome ASC
            """
        )

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def guardar_jogo(
    titulo,
    descricao,
    ano_lancamento,
    capa=None,
    genero_id=None,
):
    """Guarda um videojogo e associa-lhe um género."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO JOGO (titulo, descricao, ano_lancamento, capa)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, ano_lancamento, capa)
        )

        id_jogo = cursor.lastrowid

        if genero_id is not None:
            conexao.execute(
                """
                INSERT INTO JOGO_GENERO (id_jogo, id_genero)
                VALUES (?, ?)
                """,
                (id_jogo, genero_id)
            )

        conexao.commit()
        return id_jogo

    finally:
        conexao.close()


def listar_jogos(ordenar_por="titulo_az"):
    """Devolve os videojogos ordenados, com géneros e estado de favorito."""

    conexao = obter_conexao()

    try:
        ordenacoes = {
            "titulo_az": "JOGO.titulo ASC",
            "titulo_za": "JOGO.titulo DESC",
            "ano_antigo": "JOGO.ano_lancamento ASC, JOGO.titulo ASC",
            "ano_recente": "JOGO.ano_lancamento DESC, JOGO.titulo ASC",
        }

        # Se receber uma opção inválida, utiliza título A-Z.
        ordem = ordenacoes.get(ordenar_por, "JOGO.titulo ASC")

        consulta = f"""
            SELECT
                JOGO.id_jogo,
                JOGO.titulo,
                JOGO.descricao,
                JOGO.ano_lancamento,
                JOGO.capa,
                (
                    SELECT GROUP_CONCAT(GENERO.nome, ', ')
                    FROM JOGO_GENERO
                    INNER JOIN GENERO
                        ON JOGO_GENERO.id_genero = GENERO.id_genero
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS generos,
                (
                    SELECT MIN(id_genero)
                    FROM JOGO_GENERO
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS genero_id,
                EXISTS (
                    SELECT 1
                    FROM JOGO_FAVORITO
                    WHERE JOGO_FAVORITO.id_jogo = JOGO.id_jogo
                ) AS favorito
            FROM JOGO
            ORDER BY {ordem}
        """

        cursor = conexao.execute(consulta)

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def pesquisar_jogos(
    titulo,
    ano_lancamento=None,
    genero_id=None,
):
    """Pesquisa videojogos por título, ano e género."""

    conexao = obter_conexao()

    try:
        consulta = """
            SELECT
                JOGO.id_jogo,
                JOGO.titulo,
                JOGO.descricao,
                JOGO.ano_lancamento,
                JOGO.capa,
                (
                    SELECT GROUP_CONCAT(GENERO.nome, ', ')
                    FROM JOGO_GENERO
                    INNER JOIN GENERO
                        ON JOGO_GENERO.id_genero = GENERO.id_genero
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS generos,
                (
                    SELECT MIN(id_genero)
                    FROM JOGO_GENERO
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS genero_id,
                EXISTS (
                    SELECT 1
                    FROM JOGO_FAVORITO
                    WHERE JOGO_FAVORITO.id_jogo = JOGO.id_jogo
                ) AS favorito
            FROM JOGO
            WHERE JOGO.titulo LIKE ?
        """

        parametros = [f"%{titulo.strip()}%"]

        if ano_lancamento is not None:
            consulta += " AND JOGO.ano_lancamento = ?"
            parametros.append(ano_lancamento)

        if genero_id is not None:
            consulta += """
                AND EXISTS (
                    SELECT 1
                    FROM JOGO_GENERO
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                    AND JOGO_GENERO.id_genero = ?
                )
            """
            parametros.append(genero_id)

        consulta += " ORDER BY JOGO.titulo ASC"

        cursor = conexao.execute(consulta, parametros)

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def obter_jogo_por_id(id_jogo):
    """Devolve um videojogo específico e o seu género."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT
                JOGO.id_jogo,
                JOGO.titulo,
                JOGO.descricao,
                JOGO.ano_lancamento,
                JOGO.capa,
                (
                    SELECT GROUP_CONCAT(GENERO.nome, ', ')
                    FROM JOGO_GENERO
                    INNER JOIN GENERO
                        ON JOGO_GENERO.id_genero = GENERO.id_genero
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS generos,
                (
                    SELECT MIN(id_genero)
                    FROM JOGO_GENERO
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS genero_id,
                EXISTS (
                    SELECT 1
                    FROM JOGO_FAVORITO
                    WHERE JOGO_FAVORITO.id_jogo = JOGO.id_jogo
                ) AS favorito
            FROM JOGO
            WHERE JOGO.id_jogo = ?
            """,
            (id_jogo,)
        )

        linha = cursor.fetchone()

        return dict(linha) if linha else None

    finally:
        conexao.close()


def atualizar_jogo(
    id_jogo,
    titulo,
    descricao,
    ano_lancamento,
    capa=None,
    genero_id=None,
):
    """Atualiza os dados de um videojogo e o seu género."""

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

        if cursor.rowcount > 0:
            conexao.execute(
                """
                DELETE FROM JOGO_GENERO
                WHERE id_jogo = ?
                """,
                (id_jogo,)
            )

            if genero_id is not None:
                conexao.execute(
                    """
                    INSERT INTO JOGO_GENERO (id_jogo, id_genero)
                    VALUES (?, ?)
                    """,
                    (id_jogo, genero_id)
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


def adicionar_favorito(id_jogo):
    """Marca um videojogo como favorito."""

    conexao = obter_conexao()

    try:
        conexao.execute(
            """
            INSERT OR IGNORE INTO JOGO_FAVORITO (id_jogo)
            VALUES (?)
            """,
            (id_jogo,)
        )

        conexao.commit()

    finally:
        conexao.close()


def remover_favorito(id_jogo):
    """Retira um videojogo dos favoritos."""

    conexao = obter_conexao()

    try:
        conexao.execute(
            """
            DELETE FROM JOGO_FAVORITO
            WHERE id_jogo = ?
            """,
            (id_jogo,)
        )

        conexao.commit()

    finally:
        conexao.close()


def verificar_favorito(id_jogo):
    """Verifica se um videojogo está marcado como favorito."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT 1
            FROM JOGO_FAVORITO
            WHERE id_jogo = ?
            """,
            (id_jogo,)
        )

        return cursor.fetchone() is not None

    finally:
        conexao.close()


def listar_favoritos():
    """Devolve todos os videojogos marcados como favoritos."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT
                JOGO.id_jogo,
                JOGO.titulo,
                JOGO.descricao,
                JOGO.ano_lancamento,
                JOGO.capa,
                (
                    SELECT GROUP_CONCAT(GENERO.nome, ', ')
                    FROM JOGO_GENERO
                    INNER JOIN GENERO
                        ON JOGO_GENERO.id_genero = GENERO.id_genero
                    WHERE JOGO_GENERO.id_jogo = JOGO.id_jogo
                ) AS generos,
                1 AS favorito
            FROM JOGO
            INNER JOIN JOGO_FAVORITO
                ON JOGO.id_jogo = JOGO_FAVORITO.id_jogo
            ORDER BY JOGO.titulo ASC
            """
        )

        return [dict(linha) for linha in cursor.fetchall()]

    finally:
        conexao.close()


def obter_estatisticas_jogos():
    """Calcula estatísticas gerais dos videojogos."""

    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            SELECT
                COUNT(*) AS total,
                MIN(ano_lancamento) AS ano_mais_antigo,
                MAX(ano_lancamento) AS ano_mais_recente
            FROM JOGO
            """
        )

        estatisticas = dict(cursor.fetchone())

        cursor = conexao.execute(
            """
            SELECT
                (ano_lancamento / 10) * 10 AS decada,
                COUNT(*) AS quantidade
            FROM JOGO
            GROUP BY decada
            ORDER BY decada ASC
            """
        )

        estatisticas["jogos_por_decada"] = [
            dict(linha) for linha in cursor.fetchall()
        ]

        return estatisticas

    finally:
        conexao.close()
