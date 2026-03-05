from datetime import datetime

from database import init_db, reset_db
from crud_manager import CRUDManager
from reports import relatorio_estoque
from utils import input_int, input_float, pause


# ============================================================
# Configuração do gerenciador CRUD da entidade "Produto"
# ------------------------------------------------------------
# A classe CRUDManager centraliza todas as operações de banco
# de dados (Create, Read, Update e Delete) da tabela definida.
#
# table: nome da tabela no banco SQLite
# columns: atributos persistidos da entidade Produto
# nome_col: campo utilizado nas pesquisas por nome (LIKE)
# ============================================================
produtos_crud = CRUDManager(
    table="produtos",
    columns=["nome", "categoria", "preco", "quantidade", "data_cadastro"],
    nome_col="nome",
)


# ============================================================
# Função: input_data_cadastro()
# ------------------------------------------------------------
# Responsável por solicitar ao usuário uma data válida no
# formato ISO (YYYY-MM-DD).
#
# A função mantém um loop até que o usuário informe uma data
# válida, utilizando datetime.strptime() para validação.
#
# Retorno:
#    str -> data validada no formato YYYY-MM-DD
# ============================================================
def input_data_cadastro(prompt="Data de cadastro (YYYY-MM-DD): "):

    while True:

        data_str = input(prompt).strip()

        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str

        except ValueError:
            print("Data inválida. Use o formato YYYY-MM-DD.")


# ============================================================
# Função: input_non_empty()
# ------------------------------------------------------------
# Garante que o usuário forneça um valor obrigatório.
#
# Essa função evita que campos essenciais como "nome" e
# "categoria" sejam inseridos vazios no banco de dados.
#
# Retorno:
#    str -> texto não vazio informado pelo usuário
# ============================================================
def input_non_empty(prompt):

    while True:

        val = input(prompt).strip()

        if val:
            return val

        print("Este campo é obrigatório.")


# ============================================================
# Função: input_float_br()
# ------------------------------------------------------------
# Lê valores numéricos decimais aceitando separadores
# decimal no formato brasileiro (vírgula) ou padrão (ponto).
#
# Caso um valor padrão (default) seja informado, pressionar
# ENTER mantém o valor atual do campo.
#
# Retorno:
#    float -> número decimal validado
# ============================================================
def input_float_br(prompt, default=None):

    while True:

        s = input(prompt).strip()

        if s == "" and default is not None:
            return default

        try:
            return float(s.replace(",", "."))
        except ValueError:
            print("Digite um número válido (ex: 10.50 ou 10,50)")


# ============================================================
# Função: input_int_optional()
# ------------------------------------------------------------
# Solicita ao usuário um número inteiro opcional.
#
# Se o usuário pressionar ENTER e existir um valor padrão,
# o valor atual é mantido sem alteração.
#
# Retorno:
#    int -> valor inteiro informado ou padrão
# ============================================================
def input_int_optional(prompt, default=None):

    while True:

        s = input(prompt).strip()

        if s == "" and default is not None:
            return default

        try:
            return int(s)

        except ValueError:
            print("Digite um número inteiro válido.")


# ============================================================
# Função: confirmacao()
# ------------------------------------------------------------
# Utilizada para confirmar operações críticas no sistema,
# como exclusão de registros ou reset do banco de dados.
#
# Retorno:
#    bool -> True se usuário confirmar com "s"
# ============================================================
def confirmacao(msg="Tem certeza? (s/n): "):

    return input(msg).strip().lower() == "s"


# ============================================================
# Função: menu_produtos()
# ------------------------------------------------------------
# Implementa o menu principal de interação do sistema.
#
# Essa função centraliza todas as operações CRUD disponíveis
# para o gerenciamento de produtos do estoque.
#
# As operações disponíveis são:
#   1 - Inserção de novos produtos
#   2 - Atualização de produtos existentes
#   3 - Pesquisa por nome
#   4 - Remoção de registros
#   5 - Listagem completa do estoque
#   6 - Visualização detalhada de um produto
#   7 - Geração de relatório resumido
#   9 - Reset do banco de dados
# ============================================================
def menu_produtos():

    while True:

        print("\n===================================")
        print("SUPERMERCADO — CONTROLE DE ESTOQUE")
        print("===================================")

        print("[1] Inserir produto")
        print("[2] Alterar produto")
        print("[3] Pesquisar por nome")
        print("[4] Remover produto")
        print("[5] Listar todos")
        print("[6] Exibir um produto")
        print("[7] Relatório de estoque")
        print("[9] Resetar banco")
        print("[0] Sair")

        op = input("Escolha: ").strip()

        # -------------------------------------------------
        # Inserção de novo produto no banco de dados
        # -------------------------------------------------
        if op == "1":

            nome = input_non_empty("Nome: ")
            categoria = input_non_empty("Categoria: ")
            preco = input_float("Preço (R$): ")
            quantidade = input_int("Quantidade em estoque: ")
            data_cadastro = input_data_cadastro()

            try:

                new_id = produtos_crud.inserir(
                    [nome, categoria, preco, quantidade, data_cadastro]
                )

                print(f"Produto cadastrado com sucesso! ID={new_id}")

            except Exception as e:
                print(f"Erro ao inserir: {e}")

            pause()

        # -------------------------------------------------
        # Atualização de produto existente
        # -------------------------------------------------
        elif op == "2":

            pid = input_int("ID do produto: ")

            atual = produtos_crud.exibir_um(pid)

            if not atual:
                print("Produto não encontrado.")
                pause()
                continue

            nome = input(f"Nome [{atual['nome']}]: ").strip() or atual["nome"]

            categoria = input(f"Categoria [{atual['categoria']}]: ").strip() or atual["categoria"]

            preco = input_float_br(
                f"Preço [{atual['preco']}]: ",
                default=float(atual["preco"])
            )

            quantidade = input_int_optional(
                f"Quantidade [{atual['quantidade']}]: ",
                default=int(atual["quantidade"])
            )

            data_str = input(f"Data [{atual['data_cadastro']}]: ").strip()

            if data_str == "":
                data_cadastro = atual["data_cadastro"]

            else:
                try:
                    datetime.strptime(data_str, "%Y-%m-%d")
                    data_cadastro = data_str
                except ValueError:
                    print("Data inválida. Mantendo a anterior.")
                    data_cadastro = atual["data_cadastro"]

            try:

                produtos_crud.alterar(
                    pid,
                    [nome, categoria, preco, quantidade, data_cadastro]
                )

                print("Produto atualizado.")

            except Exception as e:
                print(f"Erro ao atualizar: {e}")

            pause()

        # -------------------------------------------------
        # Pesquisa por nome (busca parcial)
        # -------------------------------------------------
        elif op == "3":

            termo = input("Digite parte do nome: ").strip()

            res = produtos_crud.pesquisar_por_nome(termo)

            if not res:
                print("Nenhum produto encontrado.")
                pause()
                continue

            for r in res:

                print(
                    f"{r['id']} | {r['nome']} | "
                    f"estoque={r['quantidade']} | "
                    f"R$ {float(r['preco']):.2f} | "
                    f"{r.get('data_cadastro','-')}"
                )

            pause()

        # -------------------------------------------------
        # Remoção de produto
        # -------------------------------------------------
        elif op == "4":

            pid = input_int("ID para remover: ")

            atual = produtos_crud.exibir_um(pid)

            if not atual:
                print("Produto não encontrado.")
                pause()
                continue

            print(f"Produto: {atual['nome']} (estoque {atual['quantidade']})")

            if confirmacao("Confirmar remoção? (s/n): "):

                try:
                    produtos_crud.remover(pid)
                    print("Produto removido.")

                except Exception as e:
                    print(f"Erro ao remover: {e}")

            else:
                print("Remoção cancelada.")

            pause()

        # -------------------------------------------------
        # Listagem completa do estoque
        # -------------------------------------------------
        elif op == "5":

            res = produtos_crud.listar_todos()

            if not res:
                print("Nenhum produto cadastrado.")
                pause()
                continue

            for r in res:

                print(
                    f"{r['id']} | {r['nome']} | "
                    f"estoque={r['quantidade']} | "
                    f"R$ {float(r['preco']):.2f} | "
                    f"{r['categoria']} | "
                    f"{r.get('data_cadastro','-')}"
                )

            pause()

        # -------------------------------------------------
        # Visualização detalhada de um produto
        # -------------------------------------------------
        elif op == "6":

            pid = input_int("ID: ")

            r = produtos_crud.exibir_um(pid)

            if r:

                print(f"ID: {r['id']}")
                print(f"Nome: {r['nome']}")
                print(f"Categoria: {r['categoria']}")
                print(f"Preço: R$ {float(r['preco']):.2f}")
                print(f"Estoque: {r['quantidade']}")
                print(f"Data cadastro: {r['data_cadastro']}")

            else:
                print("Produto não encontrado.")

            pause()

        # -------------------------------------------------
        # Geração de relatório resumido do estoque
        # -------------------------------------------------
        elif op == "7":

            print("\n" + relatorio_estoque())

            pause()

        # -------------------------------------------------
        # Reset completo do banco de dados
        # -------------------------------------------------
        elif op == "9":

            if confirmacao("Resetar banco e apagar dados? (s/n): "):

                reset_db()
                print("Banco resetado.")

            else:
                print("Operação cancelada.")

            pause()

        elif op == "0":

            print("Saindo...")
            break

        else:
            print("Opção inválida.")


# ============================================================
# Função principal do sistema
# ------------------------------------------------------------
# Responsável por inicializar o banco de dados e iniciar o
# menu de interação do usuário.
# ============================================================
def main():

    init_db()
    menu_produtos()


if __name__ == "__main__":
    main()