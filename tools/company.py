"""
MCP tools for company information.
"""

from typing import Any, Annotated

from mcp_instance import mcp

from services.yahoo import get_company_info

@mcp.tool()
def company_info(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
) -> dict[str, Any]:
    """Return company information."""

    return get_company_info(symbol)