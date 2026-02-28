from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    id: Optional[int]
    nome: str
    categoria: str
    preco: float
    quantidade: int
    codigo_barras: Optional[str] = None
    data_cadastro: Optional[str] = None  # formato: YYYY-MM-DD