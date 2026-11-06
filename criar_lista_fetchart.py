
import csv
import re
import unicodedata
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent
FICHEIRO_CSV = PASTA_PROJETO / "dados" / "jogos.csv"
PASTA_CAPAS = PASTA_PROJETO / "capas_importadas"
FICHEIRO_LISTA = PASTA_PROJETO / "dados" / "jogos_fetchart_pendentes.txt"


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    return re.sub(r"\s+", " ", texto).strip().casefold()


def extrair_titulo(nome_ficheiro):
    titulo = Path(nome_ficheiro).stem

    titulo = re.sub(r"\s+\[[^\]]+\]", "", titulo)

    titulo = re.split(
        r"\s+-\s+box art\b",
        titulo,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    titulo = re.sub(
        r"\s+-\s+fan-made box$",
        "",
        titulo,
        flags=re.IGNORECASE
    )

    return titulo.strip()


def criar_lista():
    capas_existentes = set()

    if PASTA_CAPAS.is_dir():
        for ficheiro in PASTA_CAPAS.iterdir():
            if ficheiro.is_file():
                titulo = extrair_titulo(ficheiro.name)
                capas_existentes.add(normalizar_texto(titulo))

    jogos_pendentes = []

    with open(
        FICHEIRO_CSV,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as ficheiro:

        leitor = csv.DictReader(ficheiro)

        for linha in leitor:
            titulo = (linha["titulo"] or "").strip()

            if not titulo:
                continue

            if normalizar_texto(titulo) not in capas_existentes:
                jogos_pendentes.append(titulo)

    FICHEIRO_LISTA.write_text(
        "\n".join(jogos_pendentes),
        encoding="utf-8"
    )

    print("\n--- Lista de capas pendentes ---")
    print(f"Jogos no CSV: 500")
    print(f"Jogos sem capa encontrada: {len(jogos_pendentes)}")
    print(f"Ficheiro criado: {FICHEIRO_LISTA}")


if __name__ == "__main__":
    criar_lista()
