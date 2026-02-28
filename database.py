import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).with_name("supermercado.db")


@contextmanager
def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _coluna_existe(conn, tabela, coluna):
    cur = conn.execute(f"PRAGMA table_info({tabela});")
    colunas = [row["name"] for row in cur.fetchall()]
    return coluna in colunas


def init_db():
    with conectar() as conn:
        cur = conn.cursor()

        # Cria tabela já com data_cadastro (para banco novo)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK(preco >= 0),
                quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                codigo_barras TEXT,
                data_cadastro TEXT NOT NULL
            );
        """)

        # Se banco já existia sem data_cadastro, adiciona
        if not _coluna_existe(conn, "produtos", "data_cadastro"):
            cur.execute("ALTER TABLE produtos ADD COLUMN data_cadastro TEXT;")
            cur.execute(
                "UPDATE produtos SET data_cadastro = '2000-01-01' "
                "WHERE data_cadastro IS NULL;"
            )

        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria);"
        )


def reset_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()