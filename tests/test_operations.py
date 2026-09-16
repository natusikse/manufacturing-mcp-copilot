import pytest

from manufacturing_mcp_copilot.operations import (
    get_machine_status,
    list_machines,
)


def test_list_machines_returns_all_machines() -> None:
    machines = list_machines()

    assert len(machines) == 3
    assert {machine["machine_id"] for machine in machines} == {
        "CNC-001",
        "ROB-002",
        "PKG-003",
    }


def test_list_machines_filters_by_status() -> None:
    machines = list_machines("maintenance")

    assert len(machines) == 1
    assert machines[0]["machine_id"] == "ROB-002"


def test_get_machine_status_normalizes_id() -> None:
    machine = get_machine_status(" cnc-001 ")

    assert machine["status"] == "running"


def test_get_machine_status_rejects_unknown_machine() -> None:
    with pytest.raises(ValueError, match="Unknown machine ID"):
        get_machine_status("UNKNOWN-999")