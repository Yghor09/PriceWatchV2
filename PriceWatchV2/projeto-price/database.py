import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "precos.db")


CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        url TEXT NOT NULL,
        site TEXT NOT NULL,
        preco_alvo REAL,
        ativo INTEGER NOT NULL DEFAULT 0,
        data_cadastro TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        preco REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """,
]


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return any(row[1] == column_name for row in cursor.fetchall())


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)

        if not _column_exists(cursor, "produtos", "ativo"):
            cursor.execute(
                "ALTER TABLE produtos ADD COLUMN ativo INTEGER NOT NULL DEFAULT 0"
            )

        if not _column_exists(cursor, "produtos", "data_cadastro"):
            cursor.execute(
                "ALTER TABLE produtos ADD COLUMN data_cadastro TEXT"
            )

        conn.commit()


def listar_produtos():
    """Produtos ativados pelo cadastro e exibidos na home."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM produtos
            WHERE ativo = 1
            ORDER BY data_cadastro DESC, id DESC
            """
        )
        return cursor.fetchall()


def listar_produtos_disponiveis():
    """Produtos guardados no banco, mas ainda não ativados na home."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM produtos
            WHERE ativo = 0
            ORDER BY nome
            """
        )
        return cursor.fetchall()


def listar_todos_produtos():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos ORDER BY nome")
        return cursor.fetchall()


def buscar_produto(produto_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        return cursor.fetchone()


def ativar_produto(produto_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE produtos
            SET ativo = 1,
                data_cadastro = COALESCE(data_cadastro, ?)
            WHERE id = ?
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), produto_id),
        )
        conn.commit()


def desativar_produto(produto_id):
    """Remove da home sem apagar o produto nem o histórico do banco."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE produtos
            SET ativo = 0,
                data_cadastro = NULL
            WHERE id = ?
            """,
            (produto_id,),
        )
        conn.commit()


def buscar_historico_produto(produto_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT preco, data
            FROM historico
            WHERE produto_id = ?
            ORDER BY data ASC, id ASC
            """,
            (produto_id,),
        )
        return cursor.fetchall()


def buscar_ultimo_preco(produto_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT preco, data
            FROM historico
            WHERE produto_id = ?
            ORDER BY data DESC, id DESC
            LIMIT 1
            """,
            (produto_id,),
        )
        return cursor.fetchone()


init_db()
