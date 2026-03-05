from __future__ import annotations

from typing import Any, Optional, Sequence

from database import conectar


class CRUDManager:
    """
    Camada de acesso a dados (DAO simplificado) responsável por executar operações
    CRUD genéricas em uma tabela do SQLite.

    Objetivo:
    - Centralizar SQL (Create/Read/Update/Delete) em um único ponto
    - Evitar repetição de código e manter o main.py focado na interface/menu
    - Trabalhar com tabelas cuja chave primária seja 'id' (INTEGER)

    Observação:
    - Esta classe não valida regras de negócio complexas; seu foco é persistência.
    """

    def __init__(self, table: str, columns: list[str], nome_col: str = "nome"):
        """
        Configura o gerenciador para uma entidade/tabela.

        Parâmetros:
        - table: nome da tabela no banco (ex.: 'produtos')
        - columns: lista de colunas manipuladas em INSERT/UPDATE
                   (não inclui 'id', pois é autoincrement)
        - nome_col: coluna textual usada para pesquisa por nome (LIKE)
        """
        self.table = table
        self.columns = columns
        self.nome_col = nome_col

    def inserir(self, values: Sequence[Any]) -> int:
        """
        Insere um novo registro na tabela configurada.

        Contrato:
        - 'values' deve ter a mesma quantidade e ordem de 'self.columns'
        - Retorna o ID gerado (lastrowid), permitindo ao chamador referenciar o registro

        Exemplo (produtos):
        columns = [nome, categoria, preco, quantidade, data_cadastro]
        values  = ["Arroz", "Alimentos", 6.50, 10, "2026-03-05"]
        """
        if len(values) != len(self.columns):
            raise ValueError(
                f"Quantidade de valores ({len(values)}) diferente de columns ({len(self.columns)})."
            )

        placeholders = ", ".join(["?"] * len(self.columns))
        cols = ", ".join(self.columns)

        # SQL parametrizado evita SQL Injection e problemas de escaping.
        sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"

        with conectar() as conn:
            cur = conn.execute(sql, tuple(values))
            return int(cur.lastrowid)

    def alterar(self, entity_id: int, values: Sequence[Any]) -> None:
        """
        Atualiza um registro existente identificado por 'id'.

        Contrato:
        - 'values' deve ter a mesma quantidade e ordem de 'self.columns'
        - Caso o 'id' não exista, levanta ValueError (evita "atualizei" sem atualizar nada)

        Observação:
        - O método sobrescreve todos os campos definidos em self.columns.
        """
        if len(values) != len(self.columns):
            raise ValueError(
                f"Quantidade de valores ({len(values)}) diferente de columns ({len(self.columns)})."
            )

        sets = ", ".join([f"{c}=?" for c in self.columns])
        sql = f"UPDATE {self.table} SET {sets} WHERE id=?"

        with conectar() as conn:
            cur = conn.execute(sql, tuple(values) + (entity_id,))
            if cur.rowcount == 0:
                raise ValueError("Registro não encontrado para atualização (id inexistente).")

    def pesquisar_por_nome(self, termo: str) -> list[dict]:
        """
        Realiza busca textual parcial (LIKE) no campo configurado em 'nome_col'.

        Regras:
        - Busca por qualquer ocorrência do termo (%%termo%%)
        - Retorna lista de dicionários (cada item representa uma linha)

        Observação:
        - Se termo vier vazio, retorna lista vazia para evitar listagem "acidental".
        """
        termo = (termo or "").strip()
        if termo == "":
            return []

        sql = (
            f"SELECT * FROM {self.table} "
            f"WHERE {self.nome_col} LIKE ? "
            f"ORDER BY {self.nome_col}"
        )

        with conectar() as conn:
            rows = conn.execute(sql, (f"%{termo}%",)).fetchall()
            return [dict(r) for r in rows]

    def remover(self, entity_id: int) -> None:
        """
        Remove um registro pelo ID.

        Comportamento:
        - Caso o 'id' não exista, levanta ValueError (facilita feedback no menu).
        """
        sql = f"DELETE FROM {self.table} WHERE id=?"

        with conectar() as conn:
            cur = conn.execute(sql, (entity_id,))
            if cur.rowcount == 0:
                raise ValueError("Registro não encontrado para remoção (id inexistente).")

    def listar_todos(self) -> list[dict]:
        """
        Recupera todos os registros da tabela.

        Observação:
        - Ordenação por id DESC prioriza itens mais recentes no topo (útil para conferência).
        """
        sql = f"SELECT * FROM {self.table} ORDER BY id DESC"

        with conectar() as conn:
            rows = conn.execute(sql).fetchall()
            return [dict(r) for r in rows]

    def exibir_um(self, entity_id: int) -> Optional[dict]:
        """
        Recupera um único registro pelo ID.

        Retorno:
        - dict se encontrado
        - None caso não exista
        """
        sql = f"SELECT * FROM {self.table} WHERE id=?"

        with conectar() as conn:
            row = conn.execute(sql, (entity_id,)).fetchone()
            return dict(row) if row else None