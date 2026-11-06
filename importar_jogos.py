
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from app.database.database import obter_conexao


PASTA_PROJETO = Path(__file__).resolve().parent

PASTAS_ORIGEM = [
    PASTA_PROJETO / "capas_fetchart_pendentes",
    PASTA_PROJETO / "capas_importadas",
]

PASTA_CAPAS = PASTA_PROJETO / "app" / "static" / "capas"

EXTENSOES_PERMITIDAS = {".png", ".jpg", ".jpeg"}


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    return "".join(
        c for c in texto.casefold()
        if c.isalnum()
    )


def extrair_titulo(nome_ficheiro):
    titulo = Path(nome_ficheiro).stem

    # Remove a plataforma, por exemplo [Windows].
    titulo = re.sub(r"\s*\[[^\]]+\]", "", titulo)

    # Remove os detalhes técnicos da imagem.
    titulo = re.split(
        r"\s+-\s+box art\b",
        titulo,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    return titulo.strip()


def obter_imagens():
    imagens = {}

    for pasta in PASTAS_ORIGEM:
        if not pasta.is_dir():
            print(f"[AVISO] Pasta não encontrada: {pasta.name}")
            continue

        for ficheiro in sorted(pasta.iterdir()):
            if not ficheiro.is_file():
                continue

            if ficheiro.suffix.lower() not in EXTENSOES_PERMITIDAS:
                continue

            titulo = extrair_titulo(ficheiro.name)
            chave = normalizar_texto(titulo)

            imagens.setdefault(chave, []).append(ficheiro)

    return imagens


def encontrar_capa(titulo, imagens):
    chave = normalizar_texto(titulo)
    return imagens.get(chave, [])


def preparar_associacoes(conexao, imagens):
    jogos = conexao.execute(
        """
        SELECT id_jogo, titulo, capa
        FROM JOGO
        ORDER BY titulo
        """
    ).fetchall()

    associacoes = []
    sem_capa = []

    for jogo in jogos:
        jogo_id = jogo["id_jogo"]
        titulo = jogo["titulo"]
        capa_atual = jogo["capa"]

        # Nunca alterar jogos que já têm capa.
        if capa_atual:
            continue

        correspondencias = encontrar_capa(titulo, imagens)

        if correspondencias:
            ficheiro = correspondencias[0]
            associacoes.append((jogo_id, titulo, ficheiro))

            if len(correspondencias) > 1:
                print(
                    f"[VÁRIAS IMAGENS] {titulo} "
                    f"({len(correspondencias)} opções)"
                )
        else:
            sem_capa.append(titulo)

    return associacoes, sem_capa


def obter_destino_seguro(ficheiro):
    destino = PASTA_CAPAS / ficheiro.name

    if not destino.exists():
        return destino

    contador = 1

    while True:
        novo_nome = (
            f"{ficheiro.stem}_fetchart_{contador}"
            f"{ficheiro.suffix}"
        )

        destino = PASTA_CAPAS / novo_nome

        if not destino.exists():
            return destino

        contador += 1


def importar():
    aplicar = "--aplicar" in sys.argv

    conexao = obter_conexao()

    try:
        imagens = obter_imagens()

        associacoes, sem_capa = preparar_associacoes(
            conexao,
            imagens
        )

        total_imagens = sum(
            len(lista) for lista in imagens.values()
        )

        print("\n--- SIMULAÇÃO DA IMPORTAÇÃO ---")
        print(f"Imagens disponíveis: {total_imagens}")
        print(f"Capas que podem ser associadas: {len(associacoes)}")

        for jogo_id, titulo, ficheiro in associacoes:
            print(f"[CAPA] {titulo}")
            print(f"       {ficheiro.name}")

        print(f"\nJogos sem correspondência exata: {len(sem_capa)}")

        for titulo in sem_capa:
            print(f"[EM FALTA] {titulo}")

        if not aplicar:
            print("\nSIMULAÇÃO TERMINADA.")
            print("Nada foi copiado nem alterado.")
            print("Se estiver tudo correto, executa:")
            print("python importar_jogos.py --aplicar")
            return

        PASTA_CAPAS.mkdir(parents=True, exist_ok=True)

        total_importadas = 0

        for jogo_id, titulo, ficheiro in associacoes:
            destino = obter_destino_seguro(ficheiro)

            shutil.copy2(ficheiro, destino)

            caminho_relativo = f"capas/{destino.name}"

            conexao.execute(
                """
                UPDATE JOGO
                SET capa = ?
                WHERE id_jogo = ?
                AND (capa IS NULL OR TRIM(capa) = '')
                """,
                (caminho_relativo, jogo_id)
            )

            total_importadas += 1

        conexao.commit()

        print("\n--- IMPORTAÇÃO CONCLUÍDA ---")
        print(f"Capas associadas: {total_importadas}")
        print(f"Jogos ainda sem capa: {len(sem_capa)}")
        print("Nenhum jogo novo foi criado.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    importar()
