from typing import Any

from .financial_data import (
    get_income_statement,
    get_balance_sheet,
    get_cash_flow,
)

from .common import (
    success_response,
    error_response,
    safe_divide,
)


def format_percent_ratio(value: float | None) -> dict[str, Any]:
    if value is None:
        return {
            "value": None,
            "percent": None,
        }

    return {
        "value": value,
        "percent": round(value * 100, 2),
    }


def format_number_ratio(value: float | None) -> dict[str, Any]:
    if value is None:
        return {
            "value": None,
        }

    return {
        "value": value,
    }


def get_financial_ratios(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company ratios.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    #Ratios only need the latest report. keep limit=1
    income = get_income_statement(symbol, period, 1)
    if not income["success"]:
        return income

    balance = get_balance_sheet(symbol, period, 1)
    if not balance["success"]:
        return balance

    cash = get_cash_flow(symbol, period, 1)
    if not cash["success"]:
        return cash

    income_data = income["financials"][0]
    balance_data = balance["financials"][0]
    cash_data = cash["financials"][0]

    ratios = {

        # Percentage ratios
        # Profitability
        "gross_margin": format_percent_ratio(
            safe_divide(
                income_data["gross_profit"],
                income_data["revenue"],
            )
        ),

        "operating_margin": format_percent_ratio(
            safe_divide(
                income_data["operating_income"],
                income_data["revenue"],
            )
        ),

        "net_margin": format_percent_ratio(
            safe_divide(
                income_data["net_income"],
                income_data["revenue"],
            )
        ),

        # Returns
        "roe": format_percent_ratio(
            safe_divide(
                income_data["net_income"],
                balance_data["stockholders_equity"],
            )
        ),

        "roa": format_percent_ratio(
            safe_divide(
                income_data["net_income"],
                balance_data["total_assets"],
            )
        ),

        # Number ratios
        # Liquidity
        "current_ratio": format_number_ratio(
            safe_divide(
                balance_data["current_assets"],
                balance_data["current_liabilities"],
            )
        ),

        # Leverage
        "debt_to_equity": format_number_ratio(
            safe_divide(
                balance_data["total_debt"],
                balance_data["stockholders_equity"],
            )
        ),


        # Percentage ratios
        # Cash Flow
        "operating_cash_flow_margin": format_percent_ratio(
            safe_divide(
                cash_data["operating_cash_flow"],
                income_data["revenue"],
            )
        ),

        "free_cash_flow_margin": format_percent_ratio(
            safe_divide(
                cash_data["free_cash_flow"],
                income_data["revenue"],
            )
        ),
    }

    return success_response(
        symbol = symbol,
        period = period,
        date = income_data["date"],
        count = len(ratios),
        ratios = ratios,
    )