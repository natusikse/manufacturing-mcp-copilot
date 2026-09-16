import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from manufacturing_mcp_copilot.database import DEFAULT_DB_PATH
from manufacturing_mcp_copilot.retrieval import (
    search_technical_documents,
)

load_dotenv()

SYSTEM_INSTRUCTIONS = """
You are a manufacturing and logistics support assistant.

Answer only from the technical evidence provided in the user message.
Do not add facts, procedures, thresholds, or recommendations that are
not explicitly supported by the evidence.

Cite supporting documents using their identifiers, for example [DOC-001].
Every factual claim must include a citation.

If the evidence is insufficient, say that the available documents do not
contain enough information to answer safely.
""".strip()


def answer_question(
    question: str,
    limit: int = 3,
    db_path: str | Path = DEFAULT_DB_PATH,
    client: Any | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Answer a question using retrieved technical evidence."""
    normalized_question = question.strip()

    if not normalized_question:
        raise ValueError("Question must not be empty")

    documents = search_technical_documents(
        query=normalized_question,
        limit=limit,
        db_path=db_path,
    )

    if not documents:
        return {
            "answer": (
                "The available technical documents do not contain "
                "enough information to answer safely."
            ),
            "sources": [],
            "grounded": False,
            "model": None,
        }

    selected_model = model or os.getenv("OPENAI_MODEL")

    if not selected_model:
        raise RuntimeError("Set OPENAI_MODEL or pass a model explicitly")

    evidence = "\n\n".join(
        (
            f"[{document['document_id']}] {document['title']}\n"
            f"Category: {document['category']}\n"
            f"Content: {document['content']}"
        )
        for document in documents
    )

    prompt = f"Question:\n{normalized_question}\n\nTechnical evidence:\n{evidence}"

    llm_client = client or OpenAI()
    response = llm_client.responses.create(
        model=selected_model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        store=False,
    )

    return {
        "answer": response.output_text,
        "sources": [
            {
                "document_id": document["document_id"],
                "title": document["title"],
                "category": document["category"],
                "relevance_score": document["relevance_score"],
            }
            for document in documents
        ],
        "grounded": True,
        "model": selected_model,
    }
