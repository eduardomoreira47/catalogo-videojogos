
from app.database.database import obter_conexao


DADOS_JOGOS = [
    (
        "God of War",
        "Jogo de ação e aventura em que Kratos e o seu filho Atreus "
        "viajam por um mundo inspirado na mitologia nórdica.",
        2018,
    ),
    (
        "Grand Theft Auto V",
        "Jogo de ação em mundo aberto que acompanha três protagonistas "
        "envolvidos em assaltos e outras atividades criminosas.",
        2013,
    ),
    (
        "Halo 3",
        "Jogo de ação na primeira pessoa em que o Master Chief luta "
        "contra forças alienígenas para proteger a humanidade.",
        2007,
    ),
    (
        "Minecraft",
        "Jogo de construção e exploração num mundo de blocos, "
        "onde os jogadores podem recolher recursos e construir estruturas.",
        2011,
    ),
    (
        "Super Mario Odyssey",
        "Jogo de plataformas e aventura em que Mario viaja por vários "
        "reinos para salvar a Princesa Peach.",
        2017,
    ),
    (
        "The Witcher 3",
        "Jogo de RPG de mundo aberto em que Geralt de Rívia procura "
        "a sua filha adotiva num mundo de fantasia.",
        2015,
    ),
]


def atualizar_dados():
    conexao = obter_conexao()

    try:
        for titulo, descricao, ano in DADOS_JOGOS:
            resultado = conexao.execute(
                """
                UPDATE JOGO
                SET descricao = ?, ano_lancamento = ?
                WHERE titulo = ?
                """,
                (descricao, ano, titulo),
            )

            if resultado.rowcount > 0:
                print(f"Dados atualizados: {titulo}")
            else:
                print(f"Jogo não encontrado: {titulo}")

        conexao.commit()
        print("\nAtualização concluída!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    atualizar_dados()
