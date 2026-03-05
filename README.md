## ✅ README.md FINAL (SEM conflito e alinhado com seu projeto)

```markdown
# Supermercado — Controle de Estoque (CRUD em Python + SQLite)

## Descrição do Projeto

Este projeto implementa um **Sistema de Controle de Estoque para Supermercado**, desenvolvido em **Python** com persistência de dados em **SQLite**.

O sistema aplica o padrão **CRUD (Create, Read, Update, Delete)** para gerenciamento de produtos do estoque, permitindo cadastro, consulta, atualização e remoção de itens, além da geração de um **relatório consolidado** (quantitativo e financeiro) do estoque.

O projeto foi desenvolvido como atividade prática da disciplina de **Banco de Dados (Parte 1)**, com foco em:
- persistência de dados em banco relacional (SQLite)
- organização modular do código
- separação de responsabilidades (interface, persistência e relatórios)
- geração de relatórios com informações consolidadas

---

## Objetivo do Sistema

Permitir o gerenciamento básico e confiável do estoque de um supermercado, disponibilizando:
- cadastro e manutenção de produtos
- consulta rápida via pesquisa por nome
- geração de relatório de estoque (resumo + detalhes)

---

## Tecnologias Utilizadas

- **Python 3**
- **SQLite3**
- **Dataclasses** (modelagem da entidade)
- **Context Managers** (controle seguro de conexão/commit)
- **Git/GitHub** (versionamento)

---

## Funcionalidades do Sistema

### Operações CRUD (Produtos / Estoque)
O menu do sistema permite:
- **Inserir** produto
- **Alterar** produto por ID
- **Pesquisar por nome** (busca parcial)
- **Remover** produto por ID (com confirmação)
- **Listar todos** os produtos cadastrados
- **Exibir um** produto específico por ID

### Relatório de Estoque
O sistema gera um relatório contendo:
- quantidade de produtos cadastrados
- quantidade total de itens em estoque
- valor total do estoque
- tabela detalhada com valor total por produto (**preço × quantidade**)

---

## Estrutura do Projeto

```

.
├── main.py
├── database.py
├── crud_manager.py
├── models.py
├── reports.py
├── utils.py
├── supermercado.db
└── README.md

```

### Descrição dos Módulos

- **main.py**  
  Interface via terminal (CLI) e controle do fluxo do sistema.

- **database.py**  
  Criação e inicialização do banco SQLite, controle de conexão, índices e reset do banco.

- **crud_manager.py**  
  Classe responsável por centralizar as operações CRUD (inserir, alterar, listar, remover, buscar).

- **models.py**  
  Modelo da entidade `Produto` utilizando `dataclass`.

- **reports.py**  
  Geração do relatório consolidado do estoque (resumo + tabela detalhada).

- **utils.py**  
  Funções utilitárias para validação de entrada (inteiro, float, data) e pausa do terminal.

---

## Modelo de Dados

### Tabela: `produtos`

| Campo         | Tipo    | Descrição                      |
|--------------|---------|--------------------------------|
| id           | INTEGER | Identificador único (PK)       |
| nome         | TEXT    | Nome do produto (único)        |
| categoria    | TEXT    | Categoria do produto           |
| preco        | REAL    | Preço unitário                 |
| quantidade   | INTEGER | Quantidade em estoque          |
| data_cadastro| TEXT    | Data no formato YYYY-MM-DD     |

**Restrições aplicadas (integridade):**
- `nome` é **UNIQUE**
- `preco >= 0`
- `quantidade >= 0`

---

## Diagrama UML (Modelo de Classes)

```

+-----------------------+
|        Produto        |
+-----------------------+
| id : int              |
| nome : str            |
| categoria : str       |
| preco : float         |
| quantidade : int      |
| data_cadastro : str   |
+-----------------------+

```
       ▲
       │
       │ utiliza
       │
```

+-----------------------+
|      CRUDManager      |
+-----------------------+
| table : str           |
| columns : list        |
| nome_col : str        |
+-----------------------+
| inserir()             |
| alterar()             |
| pesquisar_por_nome()  |
| remover()             |
| listar_todos()        |
| exibir_um()           |
+-----------------------+

```
       ▲
       │
       │ usa
       │
```

+-----------------------+
|       database.py     |
+-----------------------+
| conectar()            |
| init_db()             |
| reset_db()            |
+-----------------------+

```

---

## Fluxo de Funcionamento do Sistema

```

Usuário
│
▼
main.py  (menu/CLI)
│
▼
CRUDManager (operações CRUD)
│
▼
database.py (conexão/SQLite)
│
▼
SQLite (supermercado.db)

````

---

## Como Executar o Projeto

### 1) Executar o sistema
No terminal, dentro da pasta do projeto:

```bash
python main.py
````

O arquivo `supermercado.db` será criado automaticamente na primeira execução (caso ainda não exista).

---

## Exemplo de Menu

```
SUPERMERCADO — CONTROLE DE ESTOQUE

[1] Inserir produto
[2] Alterar produto
[3] Pesquisar por nome
[4] Remover produto
[5] Listar todos
[6] Exibir um produto
[7] Relatório de estoque
[9] Resetar banco
[0] Sair
```

---

## Exemplo de Relatório

```
========== RELATÓRIO DE ESTOQUE ==========

Produtos cadastrados: 4
Quantidade total em estoque: 68
Valor total do estoque: R$ 482.50

ID | Nome | Categoria | Preço | Qtd | Valor Total
-------------------------------------------------
1  | Arroz | Alimentos | 6.50 | 10 | 65.00
2  | Feijão | Alimentos | 7.80 | 8 | 62.40
3  | Refrigerante | Bebidas | 5.00 | 20 | 100.00
4  | Cerveja | Bebidas | 4.50 | 30 | 135.00
```

---

## Requisitos Atendidos (Parte 1)

Este projeto atende aos requisitos acadêmicos da Parte 1:

* Implementação de um sistema **CRUD** em Python
* Utilização de **classe gerenciadora** para operações CRUD (`CRUDManager`)
* Persistência de dados utilizando **SQLite**
* Entidade principal com múltiplos atributos (>= 4)
* Implementação das operações: inserir, alterar, pesquisar por nome, remover, listar todos, exibir um
* Geração de **relatório resumido** do estoque com informações consolidadas

---