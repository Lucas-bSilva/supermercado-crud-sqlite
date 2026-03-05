from database import conectar


def relatorio_estoque() -> str:
    """
    Gera um relatório textual do estoque.

    O relatório possui duas partes:
    1) Resumo agregado: quantidade de produtos, total de itens e valor total do estoque.
    2) Tabela detalhada: lista de produtos ordenada por nome, incluindo o valor total
       por produto (preço * quantidade), facilitando análise e apresentação.

    Retorno:
        str -> relatório formatado em múltiplas linhas para exibição no terminal.
    """
    with conectar() as conn:
        # ------------------------------------------------------------------
        # Estatísticas gerais do estoque (útil para visão executiva do estado)
        # ------------------------------------------------------------------
        resumo = conn.execute(
            """
            SELECT
                COUNT(*) AS qtd_produtos,
                SUM(quantidade) AS qtd_itens,
                SUM(preco * quantidade) AS valor_total
            FROM produtos
            """
        ).fetchone()

        # ------------------------------------------------------------------
        # Detalhamento do estoque:
        # - ordenado por nome para leitura mais fácil
        # - inclui valor_total_produto calculado diretamente no SQL
        # ------------------------------------------------------------------
        produtos = conn.execute(
            """
            SELECT
                id,
                nome,
                categoria,
                preco,
                quantidade,
                (preco * quantidade) AS valor_total_produto,
                data_cadastro
            FROM produtos
            ORDER BY nome ASC
            """
        ).fetchall()

    # ----------------------------------------------------------------------
    # Normalização de nulos (caso o banco esteja vazio, SUM pode retornar NULL)
    # ----------------------------------------------------------------------
    qtd_produtos = int(resumo["qtd_produtos"] or 0)
    qtd_itens = int(resumo["qtd_itens"] or 0)
    valor_total = float(resumo["valor_total"] or 0.0)

    # ----------------------------------------------------------------------
    # Construção do relatório:
    # - Cabeçalho + resumo
    # - Tabela com colunas alinhadas (mais profissional para apresentação)
    # ----------------------------------------------------------------------
    out = []
    out.append("========== RELATÓRIO DE ESTOQUE ==========")
    out.append(f"Produtos cadastrados: {qtd_produtos}")
    out.append(f"Quantidade total em estoque: {qtd_itens}")
    out.append(f"Valor total do estoque: R$ {valor_total:.2f}")
    out.append("")

    # Definição de larguras para alinhamento (estética/legibilidade)
    # Ajuste se você tiver nomes muito longos
    w_id = 4
    w_nome = 22
    w_cat = 14
    w_preco = 10
    w_qtd = 5
    w_vtotal = 13

    header = (
        f"{'ID':<{w_id}} | "
        f"{'Nome':<{w_nome}} | "
        f"{'Categoria':<{w_cat}} | "
        f"{'Preço':>{w_preco}} | "
        f"{'Qtd':>{w_qtd}} | "
        f"{'Valor Total':>{w_vtotal}}"
    )
    out.append(header)
    out.append("-" * len(header))

    for p in produtos:
        # Proteções simples para manter o relatório consistente mesmo com dados inesperados
        pid = p["id"]
        nome = str(p["nome"])
        categoria = str(p["categoria"])
        preco = float(p["preco"])
        qtd = int(p["quantidade"])
        vtotal = float(p["valor_total_produto"] or 0.0)

        # Trunca strings para não quebrar o alinhamento visual
        if len(nome) > w_nome:
            nome = nome[: w_nome - 1] + "…"
        if len(categoria) > w_cat:
            categoria = categoria[: w_cat - 1] + "…"

        out.append(
            f"{pid:<{w_id}} | "
            f"{nome:<{w_nome}} | "
            f"{categoria:<{w_cat}} | "
            f"R$ {preco:>{w_preco - 3}.2f} | "
            f"{qtd:>{w_qtd}} | "
            f"R$ {vtotal:>{w_vtotal - 3}.2f}"
        )

    return "\n".join(out)