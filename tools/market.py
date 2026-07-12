from typing import Annotated, Any

from mcp_instance import mcp
from services.market_data import get_market_status

@mcp.tool()
def market_status(symbol: str) -> dict[str, Any]:
    """
    Return current market status.
    """

    return get_market_status()    