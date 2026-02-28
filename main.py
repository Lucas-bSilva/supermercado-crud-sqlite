from datetime import datetime

from database import init_db, reset_db
from crud_manager import CRUDManager
from reports import relatorio_estoque
from utils import input_int, input_float, input_optional, pause


produtos_crud = CRUDManager(
    table="produtos",
    columns=["nome", "categoria", "preco", "quantidade", "codigo_barras", "data_cadastro"],
    nome_col="nome",
)


def input_data_cadastro():
    while True:
        data_str = input("Data de cadastro (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except ValueError:
            print("Data inválida. Use o formato YYYY-MM-DD.")


def menu_produtos():
    while True:
        print("\n==============================================")
        print("SUPERMERCADO — PRODUTOS (ESTOQUE)")
        print("==============================================")
        print("[1] Inserir")
        print("[2] Alterar")
        print("[3] Pesquisar por nome")
        print("[4] Remover")
        print("[5] Listar todos")
        print("[6] Exibir um")
        print("[7] Relatório de estoque (resumo)")
        print("[9] Resetar banco (apagar supermercado.db)")
        print("[0] Sair")

        op = input("Escolha: ").strip()

        if op == "1":
            nome = input("Nome: ").strip()
            categoria = input("Categoria: ").strip()
            preco = input_float("Preço (R$): ")
            quantidade = input_int("Quantidade em estoque: ")
            codigo_barras = input_optional("Código de barras (opcional): ")
            data_cadastro = input_data_cadastro()

            try:
                new_id = produtos_crud.inserir(
                    [nome, categoria, preco, quantidade, codigo_barras, data_cadastro]
                )
                print(f"Produto cadastrado! ID={new_id}")
            except Exception as e:
                print(f"Erro ao inserir: {e}")

            pause()

        elif op == "2":
            pid = input_int("ID do produto: ")
            atual = produtos_crud.exibir_um(pid)

            if not atual:
                print("Produto não encontrado.")
                pause()
                continue

            vals = []

            for col in produtos_crud.columns:
                old = atual.get(col)
                novo = input(f"{col} [{old}]: ").strip()

                if novo == "":
                    vals.append(old)
                else:
                    if col == "preco":
                        vals.append(float(novo.replace(",", ".")))
                    elif col == "quantidade":
                        vals.append(int(novo))
                    elif col == "data_cadastro":
                        try:
                            datetime.strptime(novo, "%Y-%m-%d")
                            vals.append(novo)
                        except ValueError:
                            vals.append(old)
                    else:
                        vals.append(novo)

            produtos_crud.alterar(pid, vals)
            print("Produto atualizado!")
            pause()

        elif op == "3":
            termo = input("Digite parte do nome: ").strip()
            res = produtos_crud.pesquisar_por_nome(termo)

            for r in res:
                print(
                    f"{r['id']} | {r['nome']} | estoque={r['quantidade']} | "
                    f"R$ {float(r['preco']):.2f} | {r.get('data_cadastro', '-')}"
                )

            pause()

        elif op == "4":
            pid = input_int("ID para remover: ")
            produtos_crud.remover(pid)
            print("Removido.")
            pause()

        elif op == "5":
            res = produtos_crud.listar_todos()

            for r in res:
                print(
                    f"{r['id']} | {r['nome']} | estoque={r['quantidade']} | "
                    f"R$ {float(r['preco']):.2f} | {r['categoria']} | "
                    f"{r.get('data_cadastro', '-')}"
                )

            pause()

        elif op == "6":
            pid = input_int("ID: ")
            r = produtos_crud.exibir_um(pid)

            if r:
                print(f"ID: {r['id']}")
                print(f"Nome: {r['nome']}")
                print(f"Categoria: {r['categoria']}")
                print(f"Preço: R$ {float(r['preco']):.2f}")
                print(f"Estoque: {r['quantidade']}")
                print(f"Código de barras: {r['codigo_barras']}")
                print(f"Data de cadastro: {r.get('data_cadastro', '-')}")
            else:
                print("Produto não encontrado.")

            pause()

        elif op == "7":
            print("\n" + relatorio_estoque())
            pause()

        elif op == "9":
            c = input("Tem certeza? (s/n): ").strip().lower()
            if c == "s":
                reset_db()
                print("Banco resetado.")
            pause()

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


def main():
    init_db()
    menu_produtos()


if __name__ == "__main__":
    main()