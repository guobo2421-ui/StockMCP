"""
MCP tools for financial statements.
"""

from typing import Any

from mcp_instance import mcp
from services.financial_data import get_income_statement, get_balance_sheet, get_cash_flow
from services.financial_ratios import get_financial_ratios
from services.valuation_ratios import get_valuation_ratios
from services.financial_analysis import (
    get_profitability_analysis,
    get_liquidity_analysis,
    get_leverage_analysis,
    get_valuation_analysis,
    get_financial_health_analysis,
)


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


@mcp.tool()
def balance_sheet(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company balance sheet.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
        limit: Number of reports to return
    """

    return get_balance_sheet(symbol, period, limit)


@mcp.tool()
def cash_flow(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company cash flow.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
        limit: Number of reports to return
    """

    return get_cash_flow(symbol, period, limit)


@mcp.tool()
def financial_ratios(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company ratios.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_financial_ratios(symbol, period)


@mcp.tool()
def valuation_ratios(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company valuation ratios.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_valuation_ratios(symbol, period) 


@mcp.tool()
def profitability_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company profitability analysis.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_profitability_analysis(symbol, period)


@mcp.tool()
def liquidity_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company liquidity analysis.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_liquidity_analysis(symbol, period)


@mcp.tool()
def leverage_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company leverage analysis.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_leverage_analysis(symbol, period)    


@mcp.tool()
def valuation_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company valuation analysis.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_valuation_analysis(symbol, period)


@mcp.tool()
def financial_health_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company financial_health analysis.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_financial_health_analysis(symbol, period)               
