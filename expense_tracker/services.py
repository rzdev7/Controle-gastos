"""Regras de negócio para o controle de gastos."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from bson import ObjectId
from pymongo.collection import Collection

FORMATO_DATA = "%Y-%m-%d"


def _normalizar_data(data_bruta: Optional[str]) -> datetime:
    """Converte a string de data ou utiliza o horário atual quando vazio."""
    if not data_bruta:
        return datetime.now(timezone.utc)
    data = datetime.strptime(data_bruta, FORMATO_DATA)
    return data.replace(tzinfo=timezone.utc)


def adicionar_gasto(
    colecao: Collection[Any],
    descricao: str,
    valor: float,
    categoria: str,
    data_gasto: Optional[str] = None,
) -> ObjectId:
    """Insere um novo gasto e retorna o identificador gerado."""
    documento = {
        "descricao": descricao.strip(),
        "valor": round(float(valor), 2),
        "categoria": categoria.strip().lower(),
        "data_gasto": _normalizar_data(data_gasto),
        "criado_em": datetime.now(timezone.utc),
    }
    resultado = colecao.insert_one(documento)
    return resultado.inserted_id


def listar_gastos(colecao: Collection[Any], limite: int = 20) -> Iterable[dict[str, Any]]:
    """Retorna os gastos mais recentes."""
    cursor = colecao.find().sort("data_gasto", -1).limit(limite)
    for documento in cursor:
        documento["id"] = str(documento.pop("_id"))
        yield documento


def remover_gasto(colecao: Collection[Any], gasto_id: str) -> bool:
    """Remove um gasto pelo identificador."""
    try:
        objeto_id = ObjectId(gasto_id)
    except Exception:
        return False
    resultado = colecao.delete_one({"_id": objeto_id})
    return resultado.deleted_count == 1


def resumo_por_categoria(colecao: Collection[Any]) -> list[dict[str, Any]]:
    """Retorna totais agregados por categoria."""
    pipeline = [
        {
            "$group": {
                "_id": "$categoria",
                "total": {"$sum": "$valor"},
                "quantidade": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1}},
    ]
    resumo = []
    for linha in colecao.aggregate(pipeline):
        resumo.append(
            {
                "categoria": linha.get("_id", "desconhecida"),
                "total": round(linha.get("total", 0.0), 2),
                "quantidade": linha.get("quantidade", 0),
            }
        )
    return resumo


def gastos_mensais(colecao: Collection[Any], ano: int) -> list[dict[str, Any]]:
    """Retorna totais por mês para um ano informado."""
    pipeline = [
        {
            "$match": {
                "$expr": {"$eq": [{"$year": "$data_gasto"}, ano]},
            }
        },
        {
            "$group": {
                "_id": {"mes": {"$month": "$data_gasto"}},
                "total": {"$sum": "$valor"},
                "quantidade": {"$sum": 1},
            }
        },
        {"$sort": {"_id.mes": 1}},
    ]
    relatorio = []
    for linha in colecao.aggregate(pipeline):
        mes = linha.get("_id", {}).get("mes")
        relatorio.append(
            {
                "mes": mes,
                "total": round(linha.get("total", 0.0), 2),
                "quantidade": linha.get("quantidade", 0),
            }
        )
    return relatorio
