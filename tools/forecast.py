"""
MCP tools for company financial forecasts and analyst expectations.
"""

from typing import Any

from mcp_instance import mcp

from services.forecast_data import (
    get_company_forecast,
)


@mcp.tool()
def get_forecast(
    symbol: str,
) -> dict[str, Any]:
    """
    Get a comprehensive financial forecast for a publicly traded company.

    Returns:
        - Historical financial trends for revenue, gross margin,
          operating margin, net income, and free cash flow.
        - Analyst EPS estimates and 90-day EPS revision trends.
        - Analyst price targets, including current price, low,
          high, mean, median, and calculated upside/downside.

    Args:
        symbol:
            Stock ticker symbol, such as AAPL or MSFT.
    """

    return get_company_forecast(symbol)