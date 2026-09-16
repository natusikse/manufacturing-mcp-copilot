import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path("data/manufacturing.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN ('running', 'idle', 'maintenance')),
    temperature_c REAL NOT NULL,
    output_per_hour INTEGER NOT NULL
        CHECK (output_per_hour >= 0)
);

CREATE TABLE IF NOT EXISTS inventory (
    item_id TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL
        CHECK (quantity >= 0),
    reorder_level INTEGER NOT NULL
        CHECK (reorder_level >= 0),
    unit TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS production_orders (
    order_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    target_quantity INTEGER NOT NULL
        CHECK (target_quantity > 0),
    completed_quantity INTEGER NOT NULL
        CHECK (
            completed_quantity >= 0
            AND completed_quantity <= target_quantity
        ),
    status TEXT NOT NULL
        CHECK (
            status IN (
                'planned',
                'in_progress',
                'completed',
                'blocked'
            )
        ),
    due_date TEXT NOT NULL
);
"""

SEED_MACHINES = [
    ("CNC-001", "CNC Milling Station", "running", 67.4, 42),
    ("ROB-002", "Assembly Robot", "maintenance", 31.8, 0),
    ("PKG-003", "Packaging Line", "idle", 24.2, 0),
]

SEED_INVENTORY = [
    ("MAT-001", "Aluminium Housing", 120, 50, "pieces", "Warehouse A"),
    ("MAT-002", "Control Module", 18, 25, "pieces", "Warehouse B"),
    ("MAT-003", "Industrial Seal", 240, 100, "pieces", "Warehouse A"),
    ("MAT-004", "Lubricant", 12, 15, "litres", "Maintenance Storage"),
]

SEED_PRODUCTION_ORDERS = [
    ("ORD-1001", "Drive Control Unit", 100, 64, "in_progress", "2026-09-20"),
    ("ORD-1002", "Sensor Housing", 250, 0, "planned", "2026-09-24"),
    ("ORD-1003", "Assembly Module", 80, 80, "completed", "2026-09-15"),
    ("ORD-1004", "Packaging Unit", 60, 12, "blocked", "2026-09-18"),
]


@contextmanager
def connect(
    db_path: str | Path = DEFAULT_DB_PATH,
) -> Iterator[sqlite3.Connection]:
    """Create a configured SQLite connection and close it after use."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    """Create the database schema and insert initial simulated data."""
    with connect(db_path) as connection:
        connection.executescript(SCHEMA)
        connection.executemany(
            """
            INSERT OR IGNORE INTO machines (
                machine_id,
                name,
                status,
                temperature_c,
                output_per_hour
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            SEED_MACHINES,
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO inventory (
                item_id,
                item_name,
                quantity,
                reorder_level,
                unit,
                location
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            SEED_INVENTORY,
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO production_orders (
                order_id,
                product_name,
                target_quantity,
                completed_quantity,
                status,
                due_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            SEED_PRODUCTION_ORDERS,
        )


def list_machine_records(
    status: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Read all machines, optionally filtered by operational status."""
    initialize_database(db_path)

    query = """
        SELECT
            machine_id,
            name,
            status,
            temperature_c,
            output_per_hour
        FROM machines
    """
    parameters: tuple[str, ...] = ()

    if status is not None:
        query += " WHERE status = ?"
        parameters = (status.strip().lower(),)

    query += " ORDER BY machine_id"

    with connect(db_path) as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]


def get_machine_record(
    machine_id: str,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> dict[str, Any]:
    """Read one machine by its identifier."""
    initialize_database(db_path)
    normalized_id = machine_id.strip().upper()

    with connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT
                machine_id,
                name,
                status,
                temperature_c,
                output_per_hour
            FROM machines
            WHERE machine_id = ?
            """,
            (normalized_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"Unknown machine ID: {machine_id}")

    return dict(row)


def list_inventory_records(
    low_stock_only: bool = False,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Read inventory records, optionally returning only low-stock items."""
    initialize_database(db_path)

    query = """
        SELECT
            item_id,
            item_name,
            quantity,
            reorder_level,
            unit,
            location,
            quantity <= reorder_level AS low_stock
        FROM inventory
    """

    if low_stock_only:
        query += " WHERE quantity <= reorder_level"

    query += " ORDER BY item_id"

    with connect(db_path) as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            **dict(row),
            "low_stock": bool(row["low_stock"]),
        }
        for row in rows
    ]


def list_production_order_records(
    status: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Read production orders, optionally filtered by status."""
    initialize_database(db_path)

    query = """
        SELECT
            order_id,
            product_name,
            target_quantity,
            completed_quantity,
            status,
            due_date
        FROM production_orders
    """
    parameters: tuple[str, ...] = ()

    if status is not None:
        query += " WHERE status = ?"
        parameters = (status.strip().lower(),)

    query += " ORDER BY due_date, order_id"

    with connect(db_path) as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]