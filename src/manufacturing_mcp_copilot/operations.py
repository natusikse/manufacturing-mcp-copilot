from typing import Any

MACHINES: list[dict[str, Any]] = [
    {
        "machine_id": "CNC-001",
        "name": "CNC Milling Station",
        "status": "running",
        "temperature_c": 67.4,
        "output_per_hour": 42,
    },
    {
        "machine_id": "ROB-002",
        "name": "Assembly Robot",
        "status": "maintenance",
        "temperature_c": 31.8,
        "output_per_hour": 0,
    },
    {
        "machine_id": "PKG-003",
        "name": "Packaging Line",
        "status": "idle",
        "temperature_c": 24.2,
        "output_per_hour": 0,
    },
]


def list_machines(status: str | None = None) -> list[dict[str, Any]]:
    """Return all machines, optionally filtered by operational status."""
    if status is None:
        return [machine.copy() for machine in MACHINES]

    normalized_status = status.strip().lower()
    return [
        machine.copy() for machine in MACHINES if machine["status"] == normalized_status
    ]


def get_machine_status(machine_id: str) -> dict[str, Any]:
    """Return operational data for a single machine."""
    normalized_id = machine_id.strip().upper()

    for machine in MACHINES:
        if machine["machine_id"] == normalized_id:
            return machine.copy()

    raise ValueError(f"Unknown machine ID: {machine_id}")
