from pathlib import Path

import pytest

from manufacturing_mcp_copilot.operations import (
    get_machine_status,
    list_machines,
)


def test_list_machines_returns_all_machines(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    machines = list_machines(db_path=database)

    assert database.exists()
    assert len(machines) == 3
    assert {machine["machine_id"] for machine in machines} == {
        "CNC-001",
        "ROB-002",
        "PKG-003",
    }


def test_list_machines_filters_by_status(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    machines = list_machines("maintenance", db_path=database)

    assert len(machines) == 1
    assert machines[0]["machine_id"] == "ROB-002"


def test_get_machine_status_normalizes_id(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    machine = get_machine_status(" cnc-001 ", db_path=database)

    assert machine["status"] == "running"


def test_get_machine_status_rejects_unknown_machine(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    with pytest.raises(ValueError, match="Unknown machine ID"):
        get_machine_status("UNKNOWN-999", db_path=database)