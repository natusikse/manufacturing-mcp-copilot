from pathlib import Path
from typing import Any

from manufacturing_mcp_copilot.assistant import (
    answer_question as generate_grounded_answer,
)
from manufacturing_mcp_copilot.database import (
    DEFAULT_DB_PATH,
    get_machine_record,
    list_inventory_records,
    list_machine_records,
    list_production_order_records,
)
from manufacturing_mcp_copilot.retrieval import (
    search_technical_documents as retrieve_documents,
)


def list_machines(
    status: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return all machines, optionally filtered by operational status."""
    return list_machine_records(status=status, db_path=db_path)


def get_machine_status(
    machine_id: str,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> dict[str, Any]:
    """Return operational data for a single machine."""
    return get_machine_record(machine_id=machine_id, db_path=db_path)


def get_inventory_status(
    low_stock_only: bool = False,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return inventory records and low-stock indicators."""
    return list_inventory_records(
        low_stock_only=low_stock_only,
        db_path=db_path,
    )


def list_production_orders(
    status: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return production orders, optionally filtered by status."""
    return list_production_order_records(status=status, db_path=db_path)


def search_technical_documents(
    query: str,
    limit: int = 3,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return technical documents relevant to a search query."""
    return retrieve_documents(
        query=query,
        limit=limit,
        db_path=db_path,
    )


def answer_technical_question(
    question: str,
    limit: int = 3,
) -> dict[str, Any]:
    """Generate an evidence-grounded answer to a technical question."""
    return generate_grounded_answer(
        question=question,
        limit=limit,
    )
