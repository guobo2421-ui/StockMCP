from typing import Any

from .yahoo import get_company_info
from .financial_data import (
    get_income_statement,
    get_balance_sheet,
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
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company valuation ratios such as P/E, PEG, Price/Sales, and Price/Book. 
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

    income = get_income_statement(symbol, period, limit=2)
    if not income["success"]:
        return income
        
    if len(income["financials"]) < 2:
        return error_response(
            "INSUFFICIENT_DATA",
            "At least two financial reports are required to calculate PEG."
        )

    balance = get_balance_sheet(symbol, period, limit=1)
    if not balance["success"]:
        return balance

    market_cap = company.get("market_cap")

    income_data = income["financials"][0]
    previous_income_data = income["financials"][1]

    balance_data = balance["financials"][0]

    # EPS Growth = (Current EPS - Previous EPS) / Previous EPS
    # EPS source: Diluted EPS 
    eps_growth = safe_divide(
        income_data["diluted_eps"] - previous_income_data["diluted_eps"], 
        previous_income_data["diluted_eps"]
    )

    pe_ratio = safe_divide(
        market_cap,
        income_data["net_income"]
    ) 

    # Valuation ratios
    ratios = {

        # P/E = Market Cap / Net Income
        "pe_ratio": format_number_ratio(pe_ratio),

        # P/S = Market Cap / Revenue
        "price_sales": format_number_ratio(safe_divide(
            market_cap,
            income_data["revenue"]
        )),

        # P/B = Market Cap / Shareholders Equity
        "price_book": format_number_ratio(safe_divide(
            market_cap,
            balance_data["stockholders_equity"]
        )),

        # PEG = P/E / Earnings Growth Rate 
        "peg": format_number_ratio(safe_divide(
            pe_ratio,
            eps_growth * 100
        )),

        # EPS growth
        "eps_growth": format_percent_ratio(eps_growth),
    }


    return success_response(
        symbol=symbol,
        period = period,        
        ratios=ratios
    )