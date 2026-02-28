from database import conectar


def relatorio_estoque() -> str:
    with conectar() as conn:
        resumo = conn.execute(
            """
            SELECT
                COUNT(*) AS qtd_produtos,
                SUM(quantidade) AS qtd_itens,
                SUM(preco * quantidade) AS valor_total
            FROM produtos
            """
        ).fetchone()

        # 🔹 Ordenação A → Z e inclusão da data de cadastro
        produtos = conn.execute(
            """
            SELECT 
                id,
                nome,
                categoria,
                preco,
                quantidade,
                data_cadastro
            FROM produtos
            ORDER BY nome ASC
            """
        ).fetchall()

    qtd_produtos = int(resumo["qtd_produtos"] or 0)
    qtd_itens = int(resumo["qtd_itens"] or 0)
    valor_total = float(resumo["valor_total"] or 0)

    out = []
    out.append("=== RELATÓRIO DE ESTOQUE ===")
    out.append(f"Produtos cadastrados: {qtd_produtos}")
    out.append(f"Quantidade total em estoque: {qtd_itens}")
    out.append(f"Valor total do estoque: R$ {valor_total:.2f}")
    out.append("")
    out.append("ID | Nome | Preço | Estoque | Categoria | Cadastrado em")
    out.append("-" * 90)

    for p in produtos:
        out.append(
            f"{p['id']} | {p['nome']} | "
            f"R$ {float(p['preco']):.2f} | "
            f"estoque={p['quantidade']} | "
            f"{p['categoria']} | "
            f"{p['data_cadastro']}"
        )

    return "\n".join(out)