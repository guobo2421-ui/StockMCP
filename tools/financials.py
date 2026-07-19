"""
MCP tools for financial statements.
"""

from typing import Any

from mcp_instance import mcp
from services.financial_data import get_income_statement, get_balance_sheet, get_cash_flow
from services.financial_ratios import get_financial_ratios
from services.valuation_ratios import get_valuation_ratios
from services.company_report import get_company_report 
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
) -> dict[str, Any]:
    """
    Return company financial ratios based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
    """

    return get_financial_ratios(symbol)


@mcp.tool()
def valuation_ratios(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company valuation ratios based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
    """

    return get_valuation_ratios(symbol) 


@mcp.tool()
def profitability_analysis(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company profitability analysis based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_profitability_analysis(symbol)


@mcp.tool()
def liquidity_analysis(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company liquidity analysis based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_liquidity_analysis(symbol)


@mcp.tool()
def leverage_analysis(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company leverage analysis based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_leverage_analysis(symbol)    


@mcp.tool()
def valuation_analysis(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company valuation analysis based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_valuation_analysis(symbol)


@mcp.tool()
def financial_health_analysis(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company financial_health analysis based on TTM data.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL)
        period: annual or quarterly
    """

    return get_financial_health_analysis(symbol)    


@mcp.tool()
def company_report(
    symbol: str,
):
    """
    Return complete financial analysis report based on TTM data.
    """

    return get_company_report(symbol) 


