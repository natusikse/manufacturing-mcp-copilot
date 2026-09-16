import re
from pathlib import Path
from typing import Any

from manufacturing_mcp_copilot.database import DEFAULT_DB_PATH, connect

DOCUMENT_SCHEMA = """
CREATE TABLE IF NOT EXISTS technical_documents (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS technical_documents_fts
USING fts5(
    document_id UNINDEXED,
    title,
    content,
    tokenize = 'porter unicode61'
);
"""

SEED_DOCUMENTS = [
    (
        "DOC-001",
        "CNC Milling Station Overheating",
        "maintenance",
        (
            "If the CNC milling station temperature exceeds 75 degrees Celsius, "
            "stop the spindle and inspect the coolant level. Clean the air filter "
            "and verify that the cooling pump is operating before restarting."
        ),
    ),
    (
        "DOC-002",
        "Assembly Robot Preventive Maintenance",
        "maintenance",
        (
            "The assembly robot requires joint inspection every 500 operating "
            "hours. Check lubrication, cable wear, emergency stops, and position "
            "calibration. Record all completed maintenance actions."
        ),
    ),
    (
        "DOC-003",
        "Packaging Line Jam Recovery",
        "operations",
        (
            "For a packaging line jam, stop the conveyor, isolate the energy "
            "source, remove obstructing material, inspect the optical sensor, "
            "and perform a controlled restart."
        ),
    ),
    (
        "DOC-004",
        "Inventory Replenishment Procedure",
        "logistics",
        (
            "Create a replenishment request when material quantity reaches or "
            "falls below its reorder level. Confirm the warehouse location, "
            "required quantity, supplier lead time, and affected production orders."
        ),
    ),
    (
        "DOC-005",
        "Blocked Production Order Escalation",
        "logistics",
        (
            "A blocked production order must include a documented blocking reason. "
            "Check material availability, equipment status, and quality holds, "
            "then notify the responsible production planner."
        ),
    ),
]

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "do",
    "for",
    "from",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}


def initialize_retrieval(
    db_path: str | Path = DEFAULT_DB_PATH,
) -> None:
    """Create and populate the technical-document search index."""
    with connect(db_path) as connection:
        connection.executescript(DOCUMENT_SCHEMA)
        connection.executemany(
            """
            INSERT OR IGNORE INTO technical_documents (
                document_id,
                title,
                category,
                content
            )
            VALUES (?, ?, ?, ?)
            """,
            SEED_DOCUMENTS,
        )

        connection.execute("DELETE FROM technical_documents_fts")
        connection.execute(
            """
            INSERT INTO technical_documents_fts (
                document_id,
                title,
                content
            )
            SELECT
                document_id,
                title,
                content
            FROM technical_documents
            """
        )


def search_technical_documents(
    query: str,
    limit: int = 3,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Search technical documents using SQLite full-text search."""
    tokens = [
        token
        for token in re.findall(r"[A-Za-z0-9]+", query.lower())
        if token not in STOP_WORDS
    ]

    if not tokens:
        raise ValueError("Search query must contain at least one word")

    if not 1 <= limit <= 10:
        raise ValueError("Search limit must be between 1 and 10")

    initialize_retrieval(db_path)
    match_query = " OR ".join(f'"{token}"' for token in tokens)

    with connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT
                documents.document_id,
                documents.title,
                documents.category,
                documents.content,
                bm25(technical_documents_fts) AS search_rank
            FROM technical_documents_fts
            JOIN technical_documents AS documents
                ON documents.document_id =
                    technical_documents_fts.document_id
            WHERE technical_documents_fts MATCH ?
            ORDER BY search_rank
            LIMIT ?
            """,
            (match_query, limit),
        ).fetchall()

    return [
        {
            "document_id": row["document_id"],
            "title": row["title"],
            "category": row["category"],
            "content": row["content"],
            "relevance_score": round(-float(row["search_rank"]), 6),
        }
        for row in rows
    ]
