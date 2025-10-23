"""Interface de linha de comando para o controle de gastos."""

from __future__ import annotations

from datetime import datetime, timezone

from .db import get_collection
from .services import (
    FORMATO_DATA,
    adicionar_gasto,
    gastos_mensais,
    listar_gastos,
    remover_gasto,
    resumo_por_categoria,
)

MENU = """
Expense tracker
===============
1. Adicionar gasto
2. Listar gastos recentes
3. Resumo por categoria
4. Resumo mensal por ano
5. Remover gasto
0. Sair
Digite uma opção: """


def _pedir_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).strip())
        except ValueError:
            print("Valor inválido. Tente novamente.")


def _pedir_data(mensagem: str) -> str | None:
    data_digitada = input(mensagem).strip()
    if not data_digitada:
        return None
    try:
        datetime.strptime(data_digitada, FORMATO_DATA)
        return data_digitada
    except ValueError:
        print(f"Data inválida. Use o formato {FORMATO_DATA}.")
        return _pedir_data(mensagem)


def add_expense_flow() -> None:
    colecao = get_collection()
    descricao = input("Descrição: ").strip()
    valor = _pedir_float("Valor: ")
    categoria = input("Categoria: ").strip()
    data_gasto = _pedir_data(f"Data ({FORMATO_DATA}) [enter para hoje]: ")
    gasto_id = adicionar_gasto(colecao, descricao, valor, categoria, data_gasto)
    print(f"Gasto criado com id {gasto_id}")


def list_expenses_flow() -> None:
    colecao = get_collection()
    limite = max(1, int(_pedir_float("Quantos registros deseja ver? ")))
    for item in listar_gastos(colecao, limite=limite):
        data_gasto = item["data_gasto"].astimezone(timezone.utc).strftime(FORMATO_DATA)
        print(
            f"[{item['id']}] {data_gasto} | {item['categoria']} | {item['descricao']} | R$ {item['valor']:.2f}"
        )


def summarize_flow() -> None:
    colecao = get_collection()
    resumo = resumo_por_categoria(colecao)
    if not resumo:
        print("Nenhum gasto encontrado.")
        return
    for linha in resumo:
        print(f"{linha['categoria']}: R$ {linha['total']:.2f} ({linha['quantidade']} itens)")


def monthly_flow() -> None:
    colecao = get_collection()
    ano = int(_pedir_float("Ano (ex.: 2025): "))
    relatorio = gastos_mensais(colecao, ano)
    if not relatorio:
        print("Nenhum gasto encontrado para o ano informado.")
        return
    for linha in relatorio:
        print(f"Mês {linha['mes']:02d}: R$ {linha['total']:.2f} ({linha['quantidade']} itens)")


def delete_flow() -> None:
    colecao = get_collection()
    gasto_id = input("ID do gasto a remover: ").strip()
    sucesso = remover_gasto(colecao, gasto_id)
    if sucesso:
        print("Gasto removido com sucesso.")
    else:
        print("Não foi possível remover o gasto. Verifique o ID informado.")


def run() -> None:
    while True:
        option = input(MENU).strip()
        if option == "1":
            add_expense_flow()
        elif option == "2":
            list_expenses_flow()
        elif option == "3":
            summarize_flow()
        elif option == "4":
            monthly_flow()
        elif option == "5":
            delete_flow()
        elif option == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
