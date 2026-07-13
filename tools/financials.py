"""
MCP tools for financial statements.
"""

from typing import Any

from mcp_instance import mcp
from services.financial_data import get_income_statement


@mcp.tool()
def income_statement(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company income statement.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
        limit: Number of reports to return
    """

    return get_income_statement(symbol, period, limit)