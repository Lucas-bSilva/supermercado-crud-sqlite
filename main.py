from datetime import datetime

from database import init_db, reset_db
from crud_manager import CRUDManager
from reports import relatorio_estoque
from utils import input_int, input_float, pause


# ============================================================
# Configuração do gerenciador CRUD da entidade Produto
# ------------------------------------------------------------
# A classe CRUDManager centraliza as operações de persistência
# da tabela "produtos", permitindo inserir, alterar, buscar,
# remover, listar e exibir registros individualmente.
#
# table:
#   Nome da tabela no banco de dados.
#
# columns:
#   Lista de colunas persistidas da entidade Produto.
#
# nome_col:
#   Campo utilizado nas pesquisas textuais por nome.
# ============================================================
produtos_crud = CRUDManager(
    table="produtos",
    columns=["nome", "categoria", "preco", "quantidade", "data_cadastro"],
    nome_col="nome",
)


# ============================================================
# Funções auxiliares de entrada e validação
# ============================================================

def input_data_cadastro(prompt: str = "Data de cadastro (YYYY-MM-DD): ") -> str:
    """
    Solicita ao usuário uma data válida no formato ISO (YYYY-MM-DD).

    A função permanece em loop até que uma data válida seja informada.

    Retorno:
        str: Data validada no formato YYYY-MM-DD.
    """
    while True:
        data_str = input(prompt).strip()

        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except ValueError:
            print("Data inválida. Use o formato YYYY-MM-DD.")


def input_non_empty(prompt: str) -> str:
    """
    Garante que o usuário informe um valor obrigatório.

    Essa função é utilizada para evitar inserção de campos
    essenciais vazios, como nome e categoria.

    Retorno:
        str: Texto não vazio informado pelo usuário.
    """
    while True:
        valor = input(prompt).strip()

        if valor:
            return valor

        print("Este campo é obrigatório.")


def input_float_br(prompt: str, default=None) -> float:
    """
    Lê um valor decimal aceitando vírgula ou ponto como separador.

    Se o usuário pressionar ENTER e existir um valor padrão,
    o valor atual é mantido.

    Retorno:
        float: Valor decimal validado.
    """
    while True:
        valor = input(prompt).strip()

        if valor == "" and default is not None:
            return default

        try:
            return float(valor.replace(",", "."))
        except ValueError:
            print("Digite um número válido (ex.: 10.50 ou 10,50).")


def input_int_optional(prompt: str, default=None) -> int:
    """
    Solicita um valor inteiro opcional.

    Se o usuário pressionar ENTER e existir um valor padrão,
    o valor atual é mantido.

    Retorno:
        int: Valor inteiro informado ou valor padrão.
    """
    while True:
        valor = input(prompt).strip()

        if valor == "" and default is not None:
            return default

        try:
            return int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")


def confirmacao(msg: str = "Tem certeza? (s/n): ") -> bool:
    """
    Solicita confirmação do usuário para operações críticas.

    Exemplos de uso:
    - exclusão de produto
    - reset do banco de dados

    Retorno:
        bool: True se o usuário confirmar com 's'.
    """
    return input(msg).strip().lower() == "s"


# ============================================================
# Funções auxiliares de interface textual
# ============================================================

def exibir_cabecalho() -> None:
    """
    Exibe o cabeçalho principal do sistema com aparência textual
    mais organizada para o menu em terminal.
    """
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║         SUPERMERCADO • CONTROLE DE ESTOQUE          ║")
    print("║                  Sistema CRUD - Parte 1             ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║ [1] Inserir produto                                 ║")
    print("║ [2] Alterar produto                                 ║")
    print("║ [3] Pesquisar por nome                              ║")
    print("║ [4] Remover produto                                 ║")
    print("║ [5] Listar todos os produtos                        ║")
    print("║ [6] Exibir um produto                               ║")
    print("║ [7] Relatório de estoque                            ║")
    print("║ [9] Resetar banco                                   ║")
    print("║ [0] Sair                                            ║")
    print("╚══════════════════════════════════════════════════════╝")


def exibir_separador(titulo: str) -> None:
    """
    Exibe um separador visual para destacar operações do sistema.

    Parâmetros:
        titulo (str): Título da operação em execução.
    """
    print(f"\n── {titulo} " + "─" * 50)


# ============================================================
# Menu principal do sistema
# ------------------------------------------------------------
# Centraliza as operações CRUD da entidade Produto.
#
# Funcionalidades disponíveis:
#   1 - Inserção de novos produtos
#   2 - Atualização de produtos existentes
#   3 - Pesquisa por nome
#   4 - Remoção de registros
#   5 - Listagem completa do estoque
#   6 - Visualização detalhada de um produto
#   7 - Geração de relatório consolidado
#   9 - Reset do banco de dados
#   0 - Encerramento do programa
# ============================================================
def menu_produtos():
    while True:
        exibir_cabecalho()
        op = input("Escolha uma opção: ").strip()

        # ----------------------------------------------------
        # [1] Inserção de novo produto
        # ----------------------------------------------------
        if op == "1":
            exibir_separador("Inserção de produto")

            nome = input_non_empty("Nome: ")
            categoria = input_non_empty("Categoria: ")
            preco = input_float("Preço (R$): ")
            quantidade = input_int("Quantidade em estoque: ")
            data_cadastro = input_data_cadastro()

            try:
                novo_id = produtos_crud.inserir(
                    [nome, categoria, preco, quantidade, data_cadastro]
                )
                print(f"Produto cadastrado com sucesso! ID={novo_id}")
            except Exception as e:
                print(f"Erro ao inserir: {e}")

            pause()

        # ----------------------------------------------------
        # [2] Atualização de produto existente
        # ----------------------------------------------------
        elif op == "2":
            exibir_separador("Alteração de produto")

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
                print("Produto atualizado com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar: {e}")

            pause()

        # ----------------------------------------------------
        # [3] Pesquisa por nome (busca parcial)
        # ----------------------------------------------------
        elif op == "3":
            exibir_separador("Pesquisa por nome")

            termo = input("Digite parte do nome: ").strip()
            resultados = produtos_crud.pesquisar_por_nome(termo)

            if not resultados:
                print("Nenhum produto encontrado.")
                pause()
                continue

            for produto in resultados:
                print(
                    f"{produto['id']} | {produto['nome']} | "
                    f"estoque={produto['quantidade']} | "
                    f"R$ {float(produto['preco']):.2f} | "
                    f"{produto.get('data_cadastro', '-')}"
                )

            pause()

        # ----------------------------------------------------
        # [4] Remoção de produto
        # ----------------------------------------------------
        elif op == "4":
            exibir_separador("Remoção de produto")

            pid = input_int("ID para remover: ")
            atual = produtos_crud.exibir_um(pid)

            if not atual:
                print("Produto não encontrado.")
                pause()
                continue

            print(f"Produto selecionado: {atual['nome']} (estoque {atual['quantidade']})")

            if confirmacao("Confirmar remoção? (s/n): "):
                try:
                    produtos_crud.remover(pid)
                    print("Produto removido com sucesso.")
                except Exception as e:
                    print(f"Erro ao remover: {e}")
            else:
                print("Remoção cancelada.")

            pause()

        # ----------------------------------------------------
        # [5] Listagem completa dos produtos
        # ----------------------------------------------------
        elif op == "5":
            exibir_separador("Listagem completa")

            resultados = produtos_crud.listar_todos()

            if not resultados:
                print("Nenhum produto cadastrado.")
                pause()
                continue

            for produto in resultados:
                print(
                    f"{produto['id']} | {produto['nome']} | "
                    f"estoque={produto['quantidade']} | "
                    f"R$ {float(produto['preco']):.2f} | "
                    f"{produto['categoria']} | "
                    f"{produto.get('data_cadastro', '-')}"
                )

            pause()

        # ----------------------------------------------------
        # [6] Exibição detalhada de um único produto
        # ----------------------------------------------------
        elif op == "6":
            exibir_separador("Exibir produto")

            pid = input_int("ID: ")
            produto = produtos_crud.exibir_um(pid)

            if produto:
                print(f"ID: {produto['id']}")
                print(f"Nome: {produto['nome']}")
                print(f"Categoria: {produto['categoria']}")
                print(f"Preço: R$ {float(produto['preco']):.2f}")
                print(f"Estoque: {produto['quantidade']}")
                print(f"Data de cadastro: {produto['data_cadastro']}")
            else:
                print("Produto não encontrado.")

            pause()

        # ----------------------------------------------------
        # [7] Geração do relatório consolidado do estoque
        # ----------------------------------------------------
        elif op == "7":
            exibir_separador("Relatório de estoque")
            print("\n" + relatorio_estoque())
            pause()

        # ----------------------------------------------------
        # [9] Reset completo do banco de dados
        # ----------------------------------------------------
        elif op == "9":
            exibir_separador("Reset do banco")

            if confirmacao("Resetar banco e apagar todos os dados? (s/n): "):
                reset_db()
                print("Banco resetado com sucesso.")
            else:
                print("Operação cancelada.")

            pause()

        # ----------------------------------------------------
        # [0] Encerramento do sistema
        # ----------------------------------------------------
        elif op == "0":
            print("Encerrando o sistema...")
            break

        # ----------------------------------------------------
        # Opção inválida
        # ----------------------------------------------------
        else:
            print("Opção inválida.")
            pause()


# ============================================================
# Função principal do sistema
# ------------------------------------------------------------
# Responsável por:
#   1. Inicializar o banco de dados
#   2. Iniciar o menu principal de interação
# ============================================================
def main():
    init_db()
    menu_produtos()


if __name__ == "__main__":
    main()