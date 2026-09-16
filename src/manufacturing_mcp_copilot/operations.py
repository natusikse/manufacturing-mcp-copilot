from pathlib import Path
from typing import Any

from manufacturing_mcp_copilot.database import (
    DEFAULT_DB_PATH,
    get_machine_record,
    list_machine_records,
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