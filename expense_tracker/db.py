"""Utilidades de banco de dados para conexão com MongoDB."""

from __future__ import annotations

from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection

from .config import get_collection_name, get_database_name, get_mongo_uri

_cliente: MongoClient | None = None


def get_client() -> MongoClient:
    """Retorna uma instância única de MongoClient."""
    global _cliente
    if _cliente is None:
        _cliente = MongoClient(get_mongo_uri(), tz_aware=True)
    return _cliente


def get_collection() -> Collection[Any]:
    """Retorna a coleção MongoDB onde os gastos são armazenados."""
    cliente = get_client()
    banco_dados = cliente[get_database_name()]
    return banco_dados[get_collection_name()]
