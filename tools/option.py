"""
MCP tools for stock options.
"""

from typing import Any, Annotated

from mcp_instance import mcp

from services.options_data import (
    get_option_expirations,
    get_option_chain,
    get_option_summary,
)


@mcp.tool()
def option_expirations(
    symbol: Annotated[
        str,
        "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)",
    ],
) -> dict[str, Any]:
    """Return available option expiration dates."""

    return get_option_expirations(symbol)


@mcp.tool()
def option_chain(
    symbol: Annotated[
        str,
        "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)",
    ],
    expiration: Annotated[
        str,
        "Option expiration date in YYYY-MM-DD format.",
    ],
) -> dict[str, Any]:
    """Return calls and puts for an option expiration date."""

    return get_option_chain(symbol, expiration)


@mcp.tool()
def option_summary(
    symbol: Annotated[
        str,
        "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)",
    ],
    expiration: Annotated[
        str,
        "Option expiration date in YYYY-MM-DD format.",
    ],
) -> dict[str, Any]:
    """Return a summarized analysis of an option chain."""

    return get_option_summary(symbol, expiration)    