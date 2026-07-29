"""
MCP tools for comparing company stocks from a watchlist.
"""

from mcp_instance import mcp

from services.watchlist_comparison import get_compare_watchlist


@mcp.tool(
    description="""
    Compare multiple companies from a watchlist using financial metrics.

    Use this tool when the user asks for:
    - side-by-side stock comparison
    - compare companies
    - compare financial performance
    - compare valuation, profitability, liquidity, leverage,
      and cash flow metrics

    Returns:
    - company comparison table
    - financial metrics
    - category scores
    - strengths and risks
    """
)
def compare_watchlist(symbols: list[str]):
    return get_compare_watchlist(symbols)