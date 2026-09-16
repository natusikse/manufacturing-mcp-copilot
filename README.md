# Manufacturing MCP Copilot

An MCP-based integration layer that exposes manufacturing operations data to AI applications through standardized tools.

This portfolio project demonstrates how the Model Context Protocol can connect AI systems with manufacturing and logistics workflows. The current version provides a tested SQLite-backed equipment service; logistics tools and a retrieval layer are planned as subsequent milestones.

## Current Features

* MCP server built with the official Model Context Protocol Python SDK
* Tool for listing manufacturing equipment
* Optional filtering by operational status
* Tool for retrieving the status of a specific machine
* Normalization and validation of machine identifiers
* Automated tests for the operations layer
* Static analysis and formatting with Ruff
* SQLite-backed persistence with automatic schema initialization
* Isolated temporary databases for automated tests

## MCP Tools

### `list_machines`

Returns all available machines. An optional `status` argument filters the results by operational state.

Example statuses:

* `running`
* `idle`
* `maintenance`

### `get_machine_status`

Returns operational data for one machine, including:

* machine identifier and name
* current status
* temperature
* hourly output

## Project Structure

```text
src/manufacturing_mcp_copilot/
├── __init__.py
├── operations.py
└── server.py

tests/
└── test_operations.py
```

src/manufacturing_mcp_copilot/
├── __init__.py
├── database.py
├── operations.py
└── server.py

## Installation

This project uses Python 3.11+ and [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/natusikse/manufacturing-mcp-copilot.git
cd manufacturing-mcp-copilot
uv sync
```

## Quality Checks

Run the test suite:

```bash
uv run pytest --cov=manufacturing_mcp_copilot --cov-report=term-missing
```

Run static analysis:

```bash
uv run ruff check .
```

Run formatting:

```bash
uv run ruff format .
```

## Roadmap

* [x] Create the initial MCP server
* [x] Add equipment status tools
* [x] Add automated tests
* [x] Replace in-memory data with SQLite
* [ ] Add production-order and inventory tools
* [ ] Add technical-document retrieval
* [ ] Add an LLM-powered assistant layer
* [ ] Evaluate answer quality and hallucinations
* [ ] Add Docker deployment
* [ ] Document the complete system architecture

## Disclaimer

This is an independent educational portfolio project using simulated manufacturing data. It is not affiliated with or endorsed by any company.
