from datetime import datetime
from typing import Optional


def input_int(msg: str) -> int:
    """
    Lê um inteiro do terminal com validação.
    Mantém o usuário em loop até receber uma entrada válida.

    Parâmetros:
        msg (str): mensagem exibida ao usuário.

    Retorno:
        int: valor inteiro validado.
    """
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro (ex.: 0, 1, 2...).")


def input_float(msg: str) -> float:
    """
    Lê um número decimal do terminal com validação, aceitando separador
    decimal por ponto ou vírgula (compatível com padrão pt-BR).

    Parâmetros:
        msg (str): mensagem exibida ao usuário.

    Retorno:
        float: valor decimal validado.
    """
    while True:
        try:
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("Entrada inválida. Digite um número (ex.: 10.50 ou 10,50).")


def input_optional(msg: str) -> Optional[str]:
    """
    Lê uma entrada opcional do terminal.

    Regras:
    - Se o usuário pressionar ENTER sem digitar, retorna None.
    - Caso contrário, retorna a string informada.

    Parâmetros:
        msg (str): mensagem exibida ao usuário.

    Retorno:
        Optional[str]: valor digitado ou None.
    """
    v = input(msg).strip()
    return v if v else None


def input_data(msg: str = "Data (YYYY-MM-DD): ") -> str:
    """
    Lê e valida uma data no formato ISO (YYYY-MM-DD).

    Finalidade:
    - Padronizar entrada de datas no sistema e impedir formatos inválidos.
    - Evitar persistência de dados inconsistentes no banco de dados.

    Parâmetros:
        msg (str): mensagem exibida ao usuário.

    Retorno:
        str: data validada no formato YYYY-MM-DD.
    """
    while True:
        data_str = input(msg).strip()
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except ValueError:
            print("Data inválida. Use YYYY-MM-DD (ex.: 2026-03-05).")


def pause() -> None:
    """
    Pausa a execução até o usuário pressionar ENTER.
    Utilizado para melhorar a experiência no terminal, permitindo leitura
    das mensagens antes de retornar ao menu.
    """
    input("\nPressione ENTER para continuar...")