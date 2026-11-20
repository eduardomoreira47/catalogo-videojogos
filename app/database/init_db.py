
from app.database.database import obter_conexao


def criar_tabelas():
    conexao = obter_conexao()

    try:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS JOGO (
                id_jogo INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT,
                ano_lancamento INTEGER,
                capa TEXT,
                classificacao INTEGER
                    CHECK (classificacao BETWEEN 1 AND 5)
            );

            CREATE TABLE IF NOT EXISTS GENERO (
                id_genero INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS PLATAFORMA (
                id_plataforma INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS JOGO_GENERO (
                id_jogo INTEGER NOT NULL,
                id_genero INTEGER NOT NULL,
                PRIMARY KEY (id_jogo, id_genero),
                FOREIGN KEY (id_jogo) REFERENCES JOGO(id_jogo)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_genero) REFERENCES GENERO(id_genero)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS JOGO_PLATAFORMA (
                id_jogo INTEGER NOT NULL,
                id_plataforma INTEGER NOT NULL,
                PRIMARY KEY (id_jogo, id_plataforma),
                FOREIGN KEY (id_jogo) REFERENCES JOGO(id_jogo)
                    ON DELETE CASCADE,
                FOREIGN KEY (id_plataforma) REFERENCES PLATAFORMA(id_plataforma)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS JOGO_FAVORITO (
                id_jogo INTEGER PRIMARY KEY,
                FOREIGN KEY (id_jogo) REFERENCES JOGO(id_jogo)
                    ON DELETE CASCADE
            );
        """)

        # Verifica as colunas existentes na tabela JOGO.
        colunas = conexao.execute(
            "PRAGMA table_info(JOGO)"
        ).fetchall()

        nomes_colunas = [coluna["name"] for coluna in colunas]

        # Acrescenta a coluna capa apenas se ainda não existir.
        if "capa" not in nomes_colunas:
            conexao.execute(
                "ALTER TABLE JOGO ADD COLUMN capa TEXT"
            )

        # Acrescenta a classificação apenas se ainda não existir.
        if "classificacao" not in nomes_colunas:
            conexao.execute("""
                ALTER TABLE JOGO
                ADD COLUMN classificacao INTEGER
                CHECK (classificacao BETWEEN 1 AND 5)
            """)

        # Lista de géneros.
        generos = [
            "Ação",
            "Aventura",
            "RPG",
            "Desporto",
            "Corridas",
            "Estratégia",
            "Simulação",
            "Terror",
            "Plataformas",
            "Luta",
            "Puzzle",
            "Mundo Aberto"
        ]

        for genero in generos:
            conexao.execute(
                "INSERT OR IGNORE INTO GENERO (nome) VALUES (?)",
                (genero,)
            )

        # Atualiza o nome da primeira PlayStation, se necessário.
        conexao.execute("""
            UPDATE PLATAFORMA
            SET nome = 'PlayStation (PS1)'
            WHERE nome = 'PlayStation'
              AND NOT EXISTS (
                  SELECT 1 FROM PLATAFORMA
                  WHERE nome = 'PlayStation (PS1)'
              )
        """)

        # Lista de plataformas.
        plataformas = [
            "PC",
            "macOS",
            "Linux",
            "PlayStation (PS1)",
            "PlayStation 2",
            "PlayStation 3",
            "PlayStation 4",
            "PlayStation 5",
            "PSP",
            "PS Vita",
            "Xbox",
            "Xbox 360",
            "Xbox One",
            "Xbox Series X/S",
            "Nintendo Entertainment System (NES)",
            "Super Nintendo (SNES)",
            "Nintendo 64",
            "Nintendo GameCube",
            "Nintendo Wii",
            "Nintendo Wii U",
            "Nintendo Switch",
            "Game Boy",
            "Game Boy Color",
            "Game Boy Advance",
            "Nintendo DS",
            "Nintendo 3DS",
            "Android",
            "iOS",
            "Arcade",
            "Sega Mega Drive (Genesis)",
            "Sega Master System",
            "Sega Game Gear",
            "Sega Saturn",
            "Sega Dreamcast"
        ]

        for plataforma in plataformas:
            conexao.execute(
                "INSERT OR IGNORE INTO PLATAFORMA (nome) VALUES (?)",
                (plataforma,)
            )

        conexao.commit()

        print("Tabelas criadas e verificadas com sucesso!")

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabelas()
