
import sqlite3
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent
BASE_DADOS = PASTA_PROJETO / "catalogo.db"
PASTA_CAPAS = PASTA_PROJETO / "app" / "static" / "capas"


def verificar_capas():
    ligacao = sqlite3.connect(BASE_DADOS)
    cursor = ligacao.cursor()

    cursor.execute("""
        SELECT id_jogo, titulo, capa
        FROM JOGO
        ORDER BY titulo
    """)

    jogos = cursor.fetchall()
    ligacao.close()

    com_capa = []
    sem_capa = []
    capas_em_falta = []

    for jogo_id, titulo, capa in jogos:
        if capa:
            nome_ficheiro = Path(capa).name
            caminho_capa = PASTA_CAPAS / nome_ficheiro

            if caminho_capa.is_file():
                com_capa.append(titulo)
            else:
                capas_em_falta.append((titulo, capa))
        else:
            sem_capa.append(titulo)

    print("\n--- VERIFICAÇÃO DO CATÁLOGO ---")
    print(f"Total de jogos: {len(jogos)}")
    print(f"Jogos com capa existente: {len(com_capa)}")
    print(f"Jogos sem capa: {len(sem_capa)}")
    print(f"Capas associadas mas não encontradas: {len(capas_em_falta)}")

    if sem_capa:
        print("\n--- JOGOS SEM CAPA ---")
        for titulo in sem_capa:
            print(titulo)

    if capas_em_falta:
        print("\n--- CAPAS EM FALTA NO DISCO ---")
        for titulo, caminho in capas_em_falta:
            print(f"{titulo} -> {caminho}")


if __name__ == "__main__":
    verificar_capas()
