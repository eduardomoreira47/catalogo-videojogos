from app.database.database import obter_conexao


def criar_tabelas():
    conexao = obter_conexao()

    try:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS JOGO (
                id_jogo INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT,
                ano_lancamento INTEGER
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
        """)

        # Verifica se a coluna "capa" já existe.
        colunas = conexao.execute(
            "PRAGMA table_info(JOGO)"
        ).fetchall()

        nomes_colunas = [coluna["name"] for coluna in colunas]

        # Só acrescenta a coluna se ainda não existir.
        if "capa" not in nomes_colunas:
            conexao.execute(
                "ALTER TABLE JOGO ADD COLUMN capa TEXT"
            )

        conexao.commit()
        print("Tabelas criadas e verificadas com sucesso!")

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabelas()