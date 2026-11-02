
import re
import shutil
import unicodedata
from pathlib import Path

from app.database.database import obter_conexao


# Pastas do projeto
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ORIGEM = PASTA_PROJETO / "capas_importadas"
PASTA_CAPAS = PASTA_PROJETO / "app" / "static" / "capas"

# Extensões de imagem permitidas
EXTENSOES_PERMITIDAS = {".png", ".jpg", ".jpeg"}


def normalizar_texto(texto):
    """Normaliza texto para facilitar a comparação dos títulos."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )
    return re.sub(r"\s+", " ", texto).strip().casefold()


def extrair_titulo(nome_ficheiro):
    """Extrai o título a partir do nome criado pelo fetchart."""
    titulo = Path(nome_ficheiro).stem

    # Remove a informação da plataforma, por exemplo [Windows].
    titulo = re.sub(r"\s*\[[^\]]+\]", "", titulo)

    # Remove os detalhes técnicos da imagem.
    titulo = re.split(
        r"\s+-\s+box art\b",
        titulo,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    # Remove sufixos conhecidos que fazem parte do nome do ficheiro.
    titulo = re.sub(
        r"\s+-\s+fan-made box$",
        "",
        titulo,
        flags=re.IGNORECASE,
    )

    return titulo.strip()


def importar_jogos():
    """Importa os jogos encontrados na pasta de capas."""
    if not PASTA_ORIGEM.is_dir():
        print(f"A pasta de origem não existe: {PASTA_ORIGEM}")
        return

    PASTA_CAPAS.mkdir(parents=True, exist_ok=True)

    conexao = obter_conexao()

    importados = 0
    atualizados = 0
    ignorados = 0

    try:
        ficheiros = sorted(PASTA_ORIGEM.iterdir())

        for ficheiro in ficheiros:
            if not ficheiro.is_file():
                continue

            if ficheiro.suffix.lower() not in EXTENSOES_PERMITIDAS:
                print(f"Ignorado (formato não permitido): {ficheiro.name}")
                ignorados += 1
                continue

            titulo = extrair_titulo(ficheiro.name)

            if not titulo:
                print(f"Ignorado (sem título): {ficheiro.name}")
                ignorados += 1
                continue

            chave_titulo = normalizar_texto(titulo)

            # Procura um título igual na base de dados.
            jogos = conexao.execute(
                """
                SELECT id_jogo, titulo, capa
                FROM JOGO
                """
            ).fetchall()

            jogo_existente = next(
                (
                    jogo
                    for jogo in jogos
                    if normalizar_texto(jogo["titulo"]) == chave_titulo
                ),
                None,
            )

            # Usa o nome original do ficheiro para evitar colisões.
            destino = PASTA_CAPAS / ficheiro.name
            caminho_relativo = f"capas/{ficheiro.name}"

            # Não substitui ficheiros com o mesmo nome.
            if destino.exists():
                destino = PASTA_CAPAS / (
                    f"{ficheiro.stem}_importado{ficheiro.suffix.lower()}"
                )
                caminho_relativo = f"capas/{destino.name}"

            shutil.copy2(ficheiro, destino)

            if jogo_existente:
                # Atualiza a capa sem criar um jogo duplicado.
                conexao.execute(
                    """
                    UPDATE JOGO
                    SET capa = ?
                    WHERE id_jogo = ?
                    """,
                    (caminho_relativo, jogo_existente["id_jogo"]),
                )
                atualizados += 1
                print(f"Capa atualizada: {jogo_existente['titulo']}")

            else:
                # Cria o jogo quando ainda não existe.
                conexao.execute(
                    """
                    INSERT INTO JOGO (titulo, descricao, ano_lancamento, capa)
                    VALUES (?, ?, ?, ?)
                    """,
                    (titulo, None, None, caminho_relativo),
                )
                importados += 1
                print(f"Jogo criado: {titulo}")

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

    print("\n--- Resumo da importação ---")
    print(f"Jogos criados: {importados}")
    print(f"Capas associadas a jogos existentes: {atualizados}")
    print(f"Ficheiros ignorados: {ignorados}")


if __name__ == "__main__":
    importar_jogos()
