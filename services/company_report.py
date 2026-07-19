from typing import Any

from services.yahoo import get_company_info
from .financial_analysis import (
    get_profitability_analysis,
    get_liquidity_analysis,
    get_leverage_analysis,
    get_valuation_analysis,
    get_financial_health_analysis,
)

from .common import (
    success_response,
    error_response,
)


def get_company_report(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return complete company financial report.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()


    company = get_company_info(symbol)

    if not company["success"]:
        return company


    profitability = get_profitability_analysis(
        symbol
    )

    liquidity = get_liquidity_analysis(
        symbol
    )

    leverage = get_leverage_analysis(
        symbol
    )

    valuation = get_valuation_analysis(
        symbol
    )

    health = get_financial_health_analysis(
        symbol
    )

    return success_response(
        symbol = symbol,
        period = "TTM",
        company=company,

        analysis={
            "profitability": profitability,
            "liquidity": liquidity,
            "leverage": leverage,
            "valuation": valuation,
            "financial_health": health,
        }
    )