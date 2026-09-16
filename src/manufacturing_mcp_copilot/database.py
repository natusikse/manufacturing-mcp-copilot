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
"""

SEED_MACHINES = [
    ("CNC-001", "CNC Milling Station", "running", 67.4, 42),
    ("ROB-002", "Assembly Robot", "maintenance", 31.8, 0),
    ("PKG-003", "Packaging Line", "idle", 24.2, 0),
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