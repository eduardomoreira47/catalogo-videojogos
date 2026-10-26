import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "catalogo.db"


def obter_conexao():
    """Cria uma ligação à base de dados SQLite."""
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao