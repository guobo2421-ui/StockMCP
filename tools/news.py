from typing import Annotated, Any

from mcp_instance import mcp
from services.yahoo import get_stock_news


@mcp.tool()
def stock_news(
    symbol: Annotated[
        str,
        "Stock ticker symbol (e.g. AAPL, TSLA, NVDA)"
    ],
) -> dict[str, Any]:
    """Return the latest news for the given stock symbol."""

    return get_stock_news(symbol)