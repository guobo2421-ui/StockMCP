from typing import Annotated, Any

from mcp_instance import mcp
from services.yahoo import (
    get_stock_price,
    get_stock_history,
    get_stock_info,
)


@mcp.tool()
def stock_price(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
) -> dict[str, Any]:
    """Return the closing stock price for the given symbol."""

    return get_stock_price(symbol)


@mcp.tool()
def stock_history(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
    period: Annotated[
        str,
        "Historical period (e.g. 1d, 1mo, 1y, max)",
    ],
) -> list[dict[str, Any]]:
    """Return historical OHLCV data."""

    return get_stock_history(symbol, period)


@mcp.tool()
def stock_info(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
) -> dict[str, Any]:
    """Return company information."""

    return get_stock_info(symbol)