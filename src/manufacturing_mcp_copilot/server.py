from typing import Any

from mcp.server import MCPServer

from manufacturing_mcp_copilot import operations

mcp = MCPServer(
    "Manufacturing Operations",
    instructions=(
        "Provides operational information about manufacturing equipment. "
        "Use list_machines for an overview and get_machine_status for details."
    ),
)


@mcp.tool()
def list_machines(status: str | None = None) -> list[dict[str, Any]]:
    """List manufacturing machines, optionally filtered by status."""
    return operations.list_machines(status)


@mcp.tool()
def get_machine_status(machine_id: str) -> dict[str, Any]:
    """Get the current operational status of a manufacturing machine."""
    return operations.get_machine_status(machine_id)


def main() -> None:
    """Run the MCP server using the default stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
