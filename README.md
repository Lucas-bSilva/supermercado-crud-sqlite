
---

# Supermercado — Sistema de Controle de Estoque

### CRUD em Python com SQLite

## Descrição do Projeto

Este projeto implementa um **Sistema de Controle de Estoque para Supermercado**, desenvolvido em **Python** com persistência de dados utilizando **SQLite**.

O sistema aplica o padrão **CRUD (Create, Read, Update, Delete)** para o gerenciamento de produtos do estoque, permitindo cadastrar, consultar, atualizar e remover itens armazenados no banco de dados, além de gerar um **relatório consolidado do estoque** contendo informações quantitativas e financeiras.

O projeto foi desenvolvido como atividade prática da disciplina de **Banco de Dados – Parte 1**, com foco nos seguintes conceitos:

* utilização de **banco de dados relacional**
* persistência de dados com **SQLite**
* **organização modular do código**
* separação de responsabilidades entre camadas do sistema
* implementação de operações **CRUD**
* geração de **relatórios consolidados**

---

# Objetivo do Sistema

O sistema tem como objetivo permitir o gerenciamento básico e confiável do estoque de um supermercado, oferecendo funcionalidades essenciais como:

* cadastro de novos produtos
* atualização de dados de produtos existentes
* busca rápida por nome
* remoção de produtos
* listagem completa do estoque
* geração de relatórios consolidados

Esse conjunto de funcionalidades permite simular um ambiente simples de gestão de estoque utilizando banco de dados relacional.

---

# Tecnologias Utilizadas

As seguintes tecnologias e recursos da linguagem foram utilizados no desenvolvimento do sistema:

* **Python 3**
* **SQLite3** (banco de dados relacional embarcado)
* **Dataclasses** (modelagem da entidade Produto)
* **Context Managers** (`with`) para controle seguro de conexão e commit
* **Git e GitHub** para controle de versão do projeto

---

# Funcionalidades do Sistema

## Operações CRUD (Produtos / Estoque)

O sistema disponibiliza as seguintes operações para manipulação de produtos:

* **Inserir produto**
  Permite cadastrar um novo item no estoque.

* **Alterar produto por ID**
  Atualiza informações de um produto existente.

* **Pesquisar por nome**
  Realiza busca parcial por nome do produto.

* **Remover produto por ID**
  Remove um item do banco de dados com confirmação do usuário.

* **Listar todos os produtos**
  Exibe todos os itens cadastrados no estoque.

* **Exibir um produto específico**
  Permite consultar um produto específico através do seu ID.

---

# Relatório de Estoque

O sistema gera um **relatório consolidado** contendo:

* número total de produtos cadastrados
* quantidade total de itens em estoque
* valor financeiro total do estoque
* tabela detalhada com valor total por produto
  (**preço × quantidade**)

Esse relatório permite visualizar rapidamente o estado atual do estoque.

---

# Estrutura do Projeto

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

---

# Descrição dos Módulos

### main.py

Responsável pela **interface de interação com o usuário via terminal (CLI)**.
Controla o fluxo principal do sistema, exibindo o menu e direcionando as operações solicitadas pelo usuário.

---

### database.py

Responsável pelo gerenciamento do banco de dados:

* criação da base SQLite
* inicialização da tabela
* criação de índices
* controle de conexão
* função de **reset do banco de dados**

---

### crud_manager.py

Classe responsável por centralizar as operações **CRUD** da aplicação.

Principais métodos:

* `inserir()`
* `alterar()`
* `pesquisar_por_nome()`
* `remover()`
* `listar_todos()`
* `exibir_um()`

Essa classe encapsula a lógica de acesso ao banco de dados para manipulação da tabela de produtos.

---

### models.py

Define o **modelo da entidade Produto**, utilizando `dataclass`.

A classe representa a estrutura de dados utilizada pela aplicação.

---

### reports.py

Responsável pela geração do **relatório consolidado do estoque**, incluindo:

* resumo estatístico
* tabela detalhada de produtos
* cálculo de valores totais

---

### utils.py

Contém funções auxiliares utilizadas em várias partes do sistema, como:

* validação de entrada numérica
* leitura segura de valores
* validação de datas
* pausa do terminal

---

# Modelo de Dados

## Tabela: `produtos`

| Campo         | Tipo    | Descrição                                    |
| ------------- | ------- | -------------------------------------------- |
| id            | INTEGER | Identificador único do produto (Primary Key) |
| nome          | TEXT    | Nome do produto                              |
| categoria     | TEXT    | Categoria do produto                         |
| preco         | REAL    | Preço unitário                               |
| quantidade    | INTEGER | Quantidade disponível em estoque             |
| data_cadastro | TEXT    | Data de cadastro no formato YYYY-MM-DD       |

---

## Restrições de Integridade

O banco de dados possui as seguintes restrições:

* `nome` possui restrição **UNIQUE**
* `preco >= 0`
* `quantidade >= 0`

Essas restrições garantem a **integridade dos dados armazenados**.

---

# Diagrama UML — Modelo de Classes

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

# Arquitetura do Sistema

O fluxo de funcionamento da aplicação segue a seguinte arquitetura:

```
Usuário
   │
   ▼
main.py  (Interface CLI / Menu)
   │
   ▼
CRUDManager (Lógica de operações)
   │
   ▼
database.py (Gerenciamento de conexão)
   │
   ▼
SQLite (arquivo supermercado.db)
```

Essa estrutura separa claramente as responsabilidades entre:

* interface do usuário
* lógica de aplicação
* persistência de dados

---

# Como Executar o Projeto

## 1) Executar o sistema

No terminal, dentro da pasta do projeto:

```bash
python main.py
```

Na primeira execução, o arquivo **`supermercado.db`** será criado automaticamente caso ainda não exista.

---

# Exemplo de Menu do Sistema

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

# Exemplo de Relatório Gerado

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

# Requisitos Atendidos — Parte 1

Este projeto atende aos requisitos acadêmicos estabelecidos para a **Parte 1 da disciplina de Banco de Dados**, incluindo:

* implementação de um sistema **CRUD completo em Python**
* utilização de **classe gerenciadora para operações CRUD**
* persistência de dados utilizando **SQLite**
* modelagem de entidade com múltiplos atributos
* operações obrigatórias:

  * inserir
  * alterar
  * pesquisar por nome
  * remover
  * listar todos
  * exibir um registro
* geração de **relatório consolidado do estoque**

---

