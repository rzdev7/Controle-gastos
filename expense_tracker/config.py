"""Ferramentas de configuração para o controle de gastos."""

from __future__ import annotations

import os


def get_mongo_uri() -> str:
    """Retorna a string de conexão com o MongoDB, usando localhost por padrão."""
    return os.getenv("MONGODB_URI", "mongodb://localhost:27017")


def get_database_name() -> str:
    """Retorna o nome do banco de dados utilizado pelo controle."""
    return os.getenv("EXPENSE_DB_NAME", "expense_tracker")


def get_collection_name() -> str:
    """Retorna o nome da coleção utilizada para armazenar os gastos."""
    return os.getenv("EXPENSE_COLLECTION_NAME", "expenses")
