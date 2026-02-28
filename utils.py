from datetime import datetime


def input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Digite um número inteiro válido.")


def input_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("Digite um número válido (ex.: 10.50).")


def input_optional(msg: str):
    v = input(msg).strip()
    return v if v else None


def input_data(msg: str = "Data (YYYY-MM-DD): ") -> str:
    """
    Lê e valida data no formato YYYY-MM-DD.
    """
    while True:
        data_str = input(msg).strip()
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except ValueError:
            print("Data inválida. Use o formato YYYY-MM-DD (ex.: 2026-02-28).")


def pause():
    input("\nPressione ENTER para continuar...")