from __future__ import annotations
from typing import Any, Sequence, Optional
from database import conectar

class CRUDManager:

    def __init__(self, table: str, columns: list[str], nome_col: str = "nome"):
        self.table = table
        self.columns = columns
        self.nome_col = nome_col

    def inserir(self, values: Sequence[Any]) -> int:
        placeholders = ", ".join(["?"] * len(self.columns))
        cols = ", ".join(self.columns)
        sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
        with conectar() as conn:
            cur = conn.execute(sql, tuple(values))
            return int(cur.lastrowid)

    def alterar(self, entity_id: int, values: Sequence[Any]) -> None:
        sets = ", ".join([f"{c}=?" for c in self.columns])
        sql = f"UPDATE {self.table} SET {sets} WHERE id=?"
        with conectar() as conn:
            conn.execute(sql, tuple(values) + (entity_id,))

    def pesquisar_por_nome(self, termo: str) -> list[dict]:
        sql = f"SELECT * FROM {self.table} WHERE {self.nome_col} LIKE ? ORDER BY {self.nome_col}"
        with conectar() as conn:
            rows = conn.execute(sql, (f"%{termo}%",)).fetchall()
            return [dict(r) for r in rows]

    def remover(self, entity_id: int) -> None:
        with conectar() as conn:
            conn.execute(f"DELETE FROM {self.table} WHERE id=?", (entity_id,))

    def listar_todos(self) -> list[dict]:
        with conectar() as conn:
            rows = conn.execute(f"SELECT * FROM {self.table} ORDER BY id DESC").fetchall()
            return [dict(r) for r in rows]

    def exibir_um(self, entity_id: int) -> Optional[dict]:
        with conectar() as conn:
            row = conn.execute(f"SELECT * FROM {self.table} WHERE id=?", (entity_id,)).fetchone()
            return dict(row) if row else None
