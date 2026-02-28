#  Supermercado — CRUD de Produtos (Parte 1) com SQLite

Sistema desenvolvido em Python utilizando SQLite para gerenciamento de estoque de produtos, atendendo às especificações acadêmicas da Parte 1 do projeto da disciplina de Banco de Dados.

O sistema implementa um CRUD completo para Produtos (Estoque), incluindo geração de relatório resumido.


##  Objetivo do Projeto

Desenvolver um sistema CRUD para cadastro e gerenciamento de produtos de um supermercado, contendo obrigatoriamente as seguintes funcionalidades:

1. Inserir
2. Alterar
3. Pesquisar por nome
4. Remover
5. Listar todos
6. Exibir um

Além disso, o sistema gera relatório resumido de estoque conforme exigido na especificação.


##  Modelagem

### Entidade Principal: Produto

A classe `Produto` possui os seguintes atributos:

- `id`
- `nome`
- `categoria`
- `preco`
- `quantidade`
- `codigo_barras`
- `data_cadastro`

O sistema utiliza uma classe genérica `CRUDManager` para gerenciar as operações de inserção, alteração, remoção, listagem e busca, conforme solicitado na especificação do projeto.


##  Funcionalidades do Sistema

Menu principal:
[1] Inserir
[2] Alterar
[3] Pesquisar por nome
[4] Remover
[5] Listar todos
[6] Exibir um
[7] Relatório de estoque (resumo)
[9] Resetar banco
[0] Sair


---

##  Relatório de Estoque

O relatório apresenta:

- Quantidade total de produtos cadastrados
- Soma total de itens em estoque
- Valor total do estoque (preço × quantidade)
- Listagem organizada dos produtos cadastrados

---

##  Banco de Dados

- Banco utilizado: SQLite
- Arquivo gerado automaticamente: `supermercado.db`
- Criação automática na primeira execução
- Estrutura gerenciada pelo arquivo `database.py`

---

##  Como Executar o Projeto

1. Certifique-se de ter o Python 3 instalado.
2. No terminal, dentro da pasta do projeto, execute:

python main.py


O banco de dados será criado automaticamente na primeira execução.

---

##  Estrutura do Projeto

crud_manager.py → Classe genérica para operações CRUD
database.py → Conexão e criação do banco SQLite
main.py → Interface de menu e interação com o usuário
models.py → Modelagem da entidade Produto
reports.py → Geração de relatório de estoque
utils.py → Funções auxiliares de entrada e validação


---

##  Tecnologias Utilizadas

- Python 3
- SQLite
- Programação Orientada a Objetos (POO)

---

##  Autor

Lucas B. Silva  
Projeto Acadêmico — Banco de Dados
