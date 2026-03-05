import sqlite3
from contextlib import contextmanager
from pathlib import Path

# -------------------------------------------------------------------
# Caminho do arquivo SQLite ao lado deste módulo (portável no projeto).
# -------------------------------------------------------------------
DB_PATH = Path(__file__).with_name("supermercado.db")


@contextmanager
def conectar():
    """
    Abre uma conexão SQLite com commit automático ao final do bloco.

    - row_factory = sqlite3.Row permite acessar colunas por nome (dict-like),
      facilitando a integração com o CRUDManager e a camada de apresentação.
    - Garante fechamento da conexão mesmo em caso de exceção.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _coluna_existe(conn, tabela, coluna):
    """
    Verifica a existência de uma coluna em uma tabela já criada.

    Útil para migrações simples (ex.: adicionar coluna nova sem quebrar
    bancos já existentes).
    """
    cur = conn.execute(f"PRAGMA table_info({tabela});")
    colunas = [row["name"] for row in cur.fetchall()]
    return coluna in colunas


def _tabela_existe(conn, tabela):
    """
    Verifica se a tabela existe no schema do SQLite.
    """
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (tabela,),
    )
    return cur.fetchone() is not None


def _migrar_produtos_removendo_codigo_barras(conn):
    """
    Migração estruturada da tabela 'produtos' para remover a coluna
    'codigo_barras' e garantir o schema alinhado com o projeto atual.

    Estratégia (compatível com SQLite de forma geral):
    1) Renomeia tabela antiga -> produtos_old
    2) Cria tabela nova (schema atualizado)
    3) Copia dados existentes (apenas colunas suportadas)
    4) Remove tabela antiga
    5) Recria índices
    """
    cur = conn.cursor()

    # Renomeia a tabela antiga para preservar dados durante a migração
    cur.execute("ALTER TABLE produtos RENAME TO produtos_old;")

    # Cria a tabela nova sem 'codigo_barras'
    cur.execute(
        """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL CHECK(preco >= 0),
            quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
            data_cadastro TEXT NOT NULL
        );
        """
    )

    # Copia os dados existentes.
    # - Se data_cadastro não existia (banco muito antigo), usa valor padrão.
    col_data = "data_cadastro" if _coluna_existe(conn, "produtos_old", "data_cadastro") else None

    if col_data:
        cur.execute(
            """
            INSERT INTO produtos (id, nome, categoria, preco, quantidade, data_cadastro)
            SELECT id, nome, categoria, preco, quantidade, data_cadastro
            FROM produtos_old;
            """
        )
    else:
        cur.execute(
            """
            INSERT INTO produtos (id, nome, categoria, preco, quantidade, data_cadastro)
            SELECT id, nome, categoria, preco, quantidade, '2000-01-01'
            FROM produtos_old;
            """
        )

    # Remove a tabela antiga
    cur.execute("DROP TABLE produtos_old;")

    # Índices (melhoram performance de busca/consulta)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria);")


def init_db():
    """
    Inicializa o banco do projeto.

    Responsabilidades:
    - Criar a tabela principal 'produtos' caso não exista
    - Garantir integridade via constraints (NOT NULL, UNIQUE, CHECK)
    - Garantir índices para consultas comuns
    - Manter compatibilidade com bancos anteriores (migração)
    """
    with conectar() as conn:
        cur = conn.cursor()

        # Caso a tabela ainda não exista, cria diretamente com o schema atual.
        if not _tabela_existe(conn, "produtos"):
            cur.execute(
                """
                CREATE TABLE produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    categoria TEXT NOT NULL,
                    preco REAL NOT NULL CHECK(preco >= 0),
                    quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                    data_cadastro TEXT NOT NULL
                );
                """
            )

            cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria);")
            return

        # Se a tabela existe, verificamos se ainda tem 'codigo_barras':
        # - Se tiver, migra para o novo schema alinhado ao main.py.
        if _coluna_existe(conn, "produtos", "codigo_barras"):
            _migrar_produtos_removendo_codigo_barras(conn)
            return

        # Se não tem 'codigo_barras', apenas garantimos que data_cadastro exista.
        # (Pode ocorrer em versões intermediárias do projeto.)
        if not _coluna_existe(conn, "produtos", "data_cadastro"):
            cur.execute("ALTER TABLE produtos ADD COLUMN data_cadastro TEXT;")
            cur.execute(
                "UPDATE produtos SET data_cadastro = '2000-01-01' "
                "WHERE data_cadastro IS NULL;"
            )

        # Reforça índices (idempotente)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria);")


def reset_db():
    """
    Reinicia o banco removendo o arquivo físico do SQLite e recriando o schema.
    Útil para testes e demonstrações em apresentação.
    """
    if DB_PATH.exists():
        DB_PATH.unlink()

    init_db()