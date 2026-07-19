from typing import Any

from .yahoo import (
    get_stock_price,
    get_company_info
)

from .financial_data import (
    get_income_statement,
)

from .financial_ttm import (
    get_ttm_income_statement,
    get_current_balance_sheet,    
    get_ttm_cash_flow,
)

from .common import (
    success_response,
    error_response,
    safe_divide,
)


def format_number_ratio(value):
    if value is None:
        return {
            "value": None,
        }

    return {
        "value": round(value, 2),
    }


def format_percent_ratio(value):
    if value is None:
        return {
            "value": None,
            "percent": None,
        }

    return {
        "value": value,
        "percent": round(value * 100, 2),
    }

def get_valuation_ratios(
    symbol: str,
) -> dict[str, Any]:
    """
    Return company valuation ratios such as P/E, PEG,
    Price/Sales, and Price/Book.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required",
        )

    symbol = symbol.strip().upper()

    price = get_stock_price(symbol)
    if not price["success"]:
        return price

    company = get_company_info(symbol)
    if not company["success"]:
        return company

    income = get_ttm_income_statement(symbol)
    if not income["success"]:
        return income

    balance = get_current_balance_sheet(symbol)
    if not balance["success"]:
        return balance

    current_price = price.get("price")
    market_cap = company.get("market_cap")

    current_ttm = income["current_ttm"]
    previous_ttm = income["previous_ttm"]

    balance_data = balance["current"]

    current_eps = current_ttm.get("diluted_eps")
    previous_eps = previous_ttm.get("diluted_eps")

    # EPS Growth =
    # (Current EPS - Previous EPS) / Previous EPS
    eps_growth = safe_divide(
        current_eps - previous_eps
        if current_eps is not None
        and previous_eps is not None
        else None,
        previous_eps,
    )

    # P/E (TTM) =
    # Current Price / TTM Diluted EPS
    pe_ratio = safe_divide(
        current_price,
        current_eps
        if current_eps is not None
        and current_eps > 0
        else None,
    )

    # PEG =
    # P/E / EPS Growth Rate (%)
    peg = None

    if eps_growth is not None and eps_growth > 0:
        peg = safe_divide(
            pe_ratio,
            eps_growth * 100,
        )

    ratios = {

        # P/E = Current Price / TTM Diluted EPS
        "pe_ratio": format_number_ratio(pe_ratio),

        # P/S = Market Cap / TTM Revenue
        "price_sales": format_number_ratio(
            safe_divide(
                market_cap,
                current_ttm["revenue"],
            )
        ),

        # P/B = Market Cap / Shareholders' Equity
        "price_book": format_number_ratio(
            safe_divide(
                market_cap,
                balance_data["stockholders_equity"],
            )
        ),

        # PEG = P/E / EPS Growth Rate (%)
        "peg": format_number_ratio(peg),

        # EPS Growth
        "eps_growth": format_percent_ratio(
            eps_growth,
        ),
    }

    return success_response(
        symbol=symbol,
        period="TTM",
        ratios=ratios,
    )