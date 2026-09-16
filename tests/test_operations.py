from pathlib import Path

import pytest

from manufacturing_mcp_copilot.operations import (
    get_inventory_status,
    get_machine_status,
    list_machines,
    list_production_orders,
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

def test_get_inventory_status_marks_low_stock(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    inventory = get_inventory_status(db_path=database)
    low_stock_ids = {
        item["item_id"]
        for item in inventory
        if item["low_stock"]
    }

    assert len(inventory) == 4
    assert low_stock_ids == {"MAT-002", "MAT-004"}


def test_get_inventory_status_filters_low_stock(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    inventory = get_inventory_status(
        low_stock_only=True,
        db_path=database,
    )

    assert {item["item_id"] for item in inventory} == {
        "MAT-002",
        "MAT-004",
    }
    assert all(item["low_stock"] for item in inventory)


def test_list_production_orders_filters_by_status(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    orders = list_production_orders("blocked", db_path=database)

    assert len(orders) == 1
    assert orders[0]["order_id"] == "ORD-1004"
    assert orders[0]["completed_quantity"] == 12