from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from manufacturing_mcp_copilot.assistant import answer_question


class FakeResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        return SimpleNamespace(
            output_text=("Stop the spindle and inspect the coolant level [DOC-001].")
        )


class FakeClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


def test_answer_question_uses_retrieved_evidence(
    tmp_path: Path,
) -> None:
    database = tmp_path / "test.db"
    client = FakeClient()

    result = answer_question(
        question="What should I do if the CNC station overheats?",
        db_path=database,
        client=client,
        model="test-model",
    )

    assert result["grounded"] is True
    assert result["model"] == "test-model"
    assert result["sources"][0]["document_id"] == "DOC-001"
    assert "[DOC-001]" in result["answer"]

    assert len(client.responses.calls) == 1
    request = client.responses.calls[0]
    assert request["model"] == "test-model"
    assert request["store"] is False
    assert "[DOC-001]" in request["input"]
    assert "coolant level" in request["input"]


def test_answer_question_does_not_call_llm_without_evidence(
    tmp_path: Path,
) -> None:
    database = tmp_path / "test.db"
    client = FakeClient()

    result = answer_question(
        question="What is the employee holiday policy?",
        db_path=database,
        client=client,
        model="test-model",
    )

    assert result["grounded"] is False
    assert result["sources"] == []
    assert result["model"] is None
    assert client.responses.calls == []


def test_answer_question_rejects_empty_question(
    tmp_path: Path,
) -> None:
    database = tmp_path / "test.db"

    with pytest.raises(ValueError, match="Question must not be empty"):
        answer_question(
            question="   ",
            db_path=database,
            model="test-model",
        )


def test_answer_question_requires_model_configuration(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "test.db"
    client = FakeClient()
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Set OPENAI_MODEL",
    ):
        answer_question(
            question="How should robot maintenance be performed?",
            db_path=database,
            client=client,
        )
