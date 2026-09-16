from pathlib import Path

import pytest

from manufacturing_mcp_copilot.retrieval import (
    search_technical_documents,
)


@pytest.mark.parametrize(
    ("query", "expected_document_id"),
    [
        ("robot maintenance lubrication", "DOC-002"),
        ("packaging conveyor jam", "DOC-003"),
        ("inventory reorder level", "DOC-004"),
        ("blocked production order", "DOC-005"),
    ],
)
def test_retrieval_returns_expected_top_document(
    query: str,
    expected_document_id: str,
    tmp_path: Path,
) -> None:
    database = tmp_path / "test.db"

    results = search_technical_documents(
        query=query,
        db_path=database,
    )

    assert results
    assert results[0]["document_id"] == expected_document_id
    assert results[0]["relevance_score"] > 0


def test_retrieval_rejects_empty_query(tmp_path: Path) -> None:
    database = tmp_path / "test.db"

    with pytest.raises(
        ValueError,
        match="Search query must contain at least one word",
    ):
        search_technical_documents("   ", db_path=database)


@pytest.mark.parametrize("limit", [0, 11])
def test_retrieval_rejects_invalid_limit(
    limit: int,
    tmp_path: Path,
) -> None:
    database = tmp_path / "test.db"

    with pytest.raises(
        ValueError,
        match="Search limit must be between 1 and 10",
    ):
        search_technical_documents(
            "maintenance",
            limit=limit,
            db_path=database,
        )
