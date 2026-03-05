from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    """
    Modelo de domínio para a entidade Produto (estoque).

    Função do modelo:
    - Representar os dados de forma estruturada dentro do código (camada de domínio)
    - Facilitar validação, testes e clareza do que compõe um "produto"
    - Servir como referência do schema lógico alinhado ao banco SQLite

    Observação:
    - O campo 'id' é opcional porque só existe após inserção no banco (AUTOINCREMENT).
    - 'data_cadastro' segue o padrão ISO (YYYY-MM-DD) e é obrigatório no schema atual.
    """
    id: Optional[int]
    nome: str
    categoria: str
    preco: float
    quantidade: int
    data_cadastro: str  # formato: YYYY-MM-DD