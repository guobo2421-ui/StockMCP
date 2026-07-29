"""
MCP tools for screening and ranking company stocks from a watchlist.
"""

from mcp_instance import mcp

from services.watchlist_screening import get_screen_watchlist


@mcp.tool(
    description="""
    Screen and rank a watchlist of stocks using financial quality scores.

    Supports screening profiles:
    - default: balanced weighting
    - value: emphasizes valuation
    - safe: emphasizes liquidity and leverage

    Returns:
    - ranking results
    - overall scores
    - category scores
    - score breakdown
    - strengths and risks
    - applied filters
    """
)
def screen_watchlist(
    symbols: list[str],
    profile: str = "default",
):
    return get_screen_watchlist(
        symbols,
        profile=profile,
    )