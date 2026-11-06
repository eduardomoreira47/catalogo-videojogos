
import csv
import re
import shutil
import unicodedata
from pathlib import Path

from app.database.database import obter_conexao


# Pastas e ficheiros do projeto
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ORIGEM = PASTA_PROJETO / "capas_importadas"
PASTA_CAPAS = PASTA_PROJETO / "app" / "static" / "capas"
FICHEIRO_CSV = PASTA_PROJETO / "dados" / "jogos.csv"

# Extensões de imagem permitidas
EXTENSOES_PERMITIDAS = {".png", ".jpg", ".jpeg"}


def normalizar_texto(texto):
    """Normaliza texto para comparar títulos."""

    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    return re.sub(r"\s+", " ", texto).strip().casefold()


def obter_jogos_existentes(conexao):
    """Obtém os jogos existentes, organizados pelo título normalizado."""

    jogos = conexao.execute(
        "SELECT id_jogo, titulo, capa FROM JOGO"
    ).fetchall()

    return {
        normalizar_texto(jogo["titulo"]): jogo
        for jogo in jogos
    }


def importar_jogos_csv(conexao):
    """Importa títulos, descrições e anos a partir do CSV."""

    if not FICHEIRO_CSV.is_file():
        print(f"Ficheiro CSV não encontrado: {FICHEIRO_CSV}")
        return

    importados = 0
    duplicados = 0
    invalidos = 0

    jogos_existentes = obter_jogos_existentes(conexao)

    with open(
        FICHEIRO_CSV,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as ficheiro:

        leitor = csv.DictReader(ficheiro)

        campos = {"titulo", "descricao", "ano_lancamento"}

        if not campos.issubset(leitor.fieldnames or []):
            print("O CSV não contém as colunas necessárias.")
            return

        for linha in leitor:
            titulo = (linha["titulo"] or "").strip()
            descricao = (linha["descricao"] or "").strip()

            try:
                ano = int(linha["ano_lancamento"])
            except (ValueError, TypeError):
                invalidos += 1
                continue

            if not titulo or not 1950 <= ano <= 2100:
                invalidos += 1
                continue

            chave = normalizar_texto(titulo)

            if chave in jogos_existentes:
                duplicados += 1
                continue

            cursor = conexao.execute(
                """
                INSERT INTO JOGO (
                    titulo,
                    descricao,
                    ano_lancamento,
                    capa
                )
                VALUES (?, ?, ?, NULL)
                """,
                (titulo, descricao, ano)
            )

            jogos_existentes[chave] = {
                "id_jogo": cursor.lastrowid,
                "titulo": titulo,
                "capa": None
            }

            importados += 1

    print("\n--- Importação do CSV ---")
    print(f"Jogos importados: {importados}")
    print(f"Jogos repetidos ignorados: {duplicados}")
    print(f"Registos inválidos ignorados: {invalidos}")


def extrair_titulo(nome_ficheiro):
    """Extrai o título a partir do nome do ficheiro da capa."""

    titulo = Path(nome_ficheiro).stem

    # Remove a informação da plataforma, por exemplo [Windows].
    titulo = re.sub(r"\s+\[[^\]]+\]", "", titulo)

    # Remove os detalhes técnicos da imagem.
    titulo = re.split(
        r"\s+-\s+box art\b",
        titulo,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    # Remove sufixos conhecidos.
    titulo = re.sub(
        r"\s+-\s+fan-made box$",
        "",
        titulo,
        flags=re.IGNORECASE
    )

    return titulo.strip()


def obter_destino_capa(ficheiro):
    """Escolhe um nome de destino sem substituir capas existentes."""

    destino = PASTA_CAPAS / ficheiro.name

    contador = 1

    while destino.exists():
        nome = (
            f"{ficheiro.stem}_importado_{contador}"
            f"{ficheiro.suffix.lower()}"
        )
        destino = PASTA_CAPAS / nome
        contador += 1

    return destino


def importar_capas(conexao):
    """Importa capas e associa-as aos jogos existentes."""

    if not PASTA_ORIGEM.is_dir():
        print(f"\nPasta de capas não encontrada: {PASTA_ORIGEM}")
        return

    PASTA_CAPAS.mkdir(parents=True, exist_ok=True)

    importados = 0
    atualizados = 0
    ignorados = 0

    jogos_existentes = obter_jogos_existentes(conexao)

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

        chave = normalizar_texto(titulo)

        destino = obter_destino_capa(ficheiro)
        caminho_relativo = f"capas/{destino.name}"

        shutil.copy2(ficheiro, destino)

        jogo_existente = jogos_existentes.get(chave)

        if jogo_existente:

            conexao.execute(
                """
                UPDATE JOGO
                SET capa = ?
                WHERE id_jogo = ?
                """,
                (caminho_relativo, jogo_existente["id_jogo"])
            )

            atualizados += 1
            print(f"Capa associada: {jogo_existente['titulo']}")

        else:

            cursor = conexao.execute(
                """
                INSERT INTO JOGO (
                    titulo,
                    descricao,
                    ano_lancamento,
                    capa
                )
                VALUES (?, NULL, NULL, ?)
                """,
                (titulo, caminho_relativo)
            )

            jogos_existentes[chave] = {
                "id_jogo": cursor.lastrowid,
                "titulo": titulo,
                "capa": caminho_relativo
            }

            importados += 1
            print(f"Jogo criado através da capa: {titulo}")

    print("\n--- Importação das capas ---")
    print(f"Jogos criados: {importados}")
    print(f"Capas associadas: {atualizados}")
    print(f"Ficheiros ignorados: {ignorados}")


def importar_jogos():
    """Executa a importação dos dados e das capas."""

    conexao = obter_conexao()

    try:
        importar_jogos_csv(conexao)
        importar_capas(conexao)

        conexao.commit()

        print("\nImportação concluída com sucesso!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    importar_jogos()
