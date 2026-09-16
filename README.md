# Manufacturing MCP Copilot

[![CI](https://github.com/natusikse/manufacturing-mcp-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/natusikse/manufacturing-mcp-copilot/actions/workflows/ci.yml)

An MCP-based AI integration layer for simulated manufacturing and logistics operations.

The project demonstrates how AI applications can access operational data, retrieve technical evidence, and generate source-aware answers through standardized Model Context Protocol tools.

## Features

- MCP server built with the official Model Context Protocol Python SDK
- Equipment status monitoring
- Inventory monitoring with low-stock detection
- Production-order tracking and filtering
- SQLite persistence with automatic schema initialization
- SQLite FTS5 retrieval over maintenance and logistics documents
- Evidence-grounded integration with the OpenAI Responses API
- Source-aware answers and safe refusal when evidence is unavailable
- Automated tests with isolated temporary databases
- Continuous integration on Python 3.11 and 3.13
- Static analysis and formatting with Ruff

## MCP Tools

| Tool | Description |
|---|---|
| `list_machines` | Lists manufacturing equipment and optionally filters it by status. |
| `get_machine_status` | Returns operational data for a selected machine. |
| `get_inventory_status` | Returns inventory levels and optionally shows only low-stock materials. |
| `list_production_orders` | Lists production orders and optionally filters them by status. |
| `search_technical_documents` | Searches the technical knowledge base and returns ranked evidence. |
| `answer_technical_question` | Generates an evidence-grounded LLM answer with source identifiers. |

## Example Retrieval Query

```text
CNC overheating coolant
```

The retrieval layer returns the most relevant technical document together with its identifier, category, content, and relevance score.

## Project Structure

```text
src/manufacturing_mcp_copilot/
├── __init__.py
├── assistant.py
├── database.py
├── operations.py
├── retrieval.py
└── server.py

tests/
├── test_assistant.py
├── test_operations.py
└── test_retrieval.py
```

## Installation

Requirements:

- Python 3.11+
- uv

Clone the repository and install the locked dependencies:

```bash
git clone https://github.com/natusikse/manufacturing-mcp-copilot.git
cd manufacturing-mcp-copilot
uv sync
```

## Run the MCP Inspector

```bash
uv run mcp dev src/manufacturing_mcp_copilot/server.py
```

The equipment, inventory, production-order, and retrieval tools work without an external API key.

## LLM Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Add an API key and a model available to your OpenAI API account:

```dotenv
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=your-model
```

The `.env` file is excluded from Git and must never be committed. Automated tests use a fake Responses API client and do not make paid API requests.

## Quality Checks

Run static analysis:

```bash
uv run ruff check .
```

Run formatting:

```bash
uv run ruff format .
```

Run the test suite with coverage:

```bash
uv run pytest \
  -W error::ResourceWarning \
  --cov=manufacturing_mcp_copilot \
  --cov-report=term-missing
```

## Reliability and Safety

- Technical answers are grounded in retrieved documents.
- Retrieved source identifiers are returned with the answer.
- The assistant is instructed not to invent unsupported procedures or thresholds.
- The LLM is not called when retrieval returns no evidence.
- Secrets are loaded from environment variables and excluded from Git.
- API integration tests use a fake client.

## Roadmap

- [x] Create the initial MCP server
- [x] Add equipment status tools
- [x] Add SQLite persistence
- [x] Add inventory and production-order tools
- [x] Add technical-document retrieval
- [x] Add an LLM-powered assistant layer
- [x] Add automated tests and CI
- [ ] Extend hallucination and answer-quality evaluation
- [ ] Add Docker deployment
- [ ] Document the complete system architecture

## Disclaimer

This is an independent educational portfolio project using simulated manufacturing and logistics data. It is not affiliated with or endorsed by any company.