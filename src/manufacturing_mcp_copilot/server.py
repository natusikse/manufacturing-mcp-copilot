from typing import Any

from mcp.server import MCPServer

from manufacturing_mcp_copilot import operations

mcp = MCPServer(
    "Manufacturing Operations",
    instructions=(
        "Provides tools for manufacturing equipment, inventory, "
        "and production-order monitoring."
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


@mcp.tool()
def get_inventory_status(
    low_stock_only: bool = False,
) -> list[dict[str, Any]]:
    """List inventory items and identify materials requiring replenishment."""
    return operations.get_inventory_status(low_stock_only)


@mcp.tool()
def list_production_orders(
    status: str | None = None,
) -> list[dict[str, Any]]:
    """List production orders, optionally filtered by order status."""
    return operations.list_production_orders(status)


def main() -> None:
    """Run the MCP server using the default stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()