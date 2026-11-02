
from pathlib import Path
import shutil

from app.database.database import obter_conexao


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ORIGEM = PASTA_PROJETO / "capas_importadas"
PASTA_CAPAS = PASTA_PROJETO / "app" / "static" / "capas"


def procurar_capa(parte_do_nome):
    """Procura uma imagem cujo nome contenha o texto indicado."""
    for ficheiro in PASTA_ORIGEM.iterdir():
        if ficheiro.is_file() and parte_do_nome.casefold() in ficheiro.name.casefold():
            return ficheiro

    return None


def corrigir_jogos():
    PASTA_CAPAS.mkdir(parents=True, exist_ok=True)
    conexao = obter_conexao()

    try:
        # Os títulos que queremos manter e as imagens correspondentes.
        correcoes = [
            {
                "titulo": "Minecraft",
                "id_manter": 3,
                "titulo_duplicado": "Minecraft - Java Edition",
                "parte_capa": "Minecraft - Java Edition",
            },
            {
                "titulo": "The Witcher 3",
                "id_manter": 2,
                "titulo_duplicado": "The Witcher 3 - Wild Hunt",
                "parte_capa": "The Witcher 3 - Wild Hunt",
            },
        ]

        for correcao in correcoes:
            capa = procurar_capa(correcao["parte_capa"])

            if capa is None:
                print(f"Capa não encontrada: {correcao['titulo']}")
                continue

            # Copia a imagem para a pasta utilizada pela aplicação.
            destino = PASTA_CAPAS / capa.name

            if not destino.exists():
                shutil.copy2(capa, destino)

            caminho_relativo = f"capas/{destino.name}"

            # Atualiza o jogo original, preservando o seu ano.
            conexao.execute(
                """
                UPDATE JOGO
                SET capa = ?
                WHERE id_jogo = ?
                """,
                (caminho_relativo, correcao["id_manter"]),
            )

            # Remove apenas o duplicado identificado.
            conexao.execute(
                """
                DELETE FROM JOGO
                WHERE titulo = ?
                """,
                (correcao["titulo_duplicado"],),
            )

            print(f"Corrigido: {correcao['titulo']}")

        conexao.commit()
        print("\nCorreções guardadas com sucesso!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    corrigir_jogos()
