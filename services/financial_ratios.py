from typing import Any

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

    income = get_ttm_income_statement(symbol)
    if not income["success"]:
        return income

    balance = get_current_balance_sheet(symbol)
    if not balance["success"]:
        return balance

    cash = get_ttm_cash_flow(symbol)
    if not cash["success"]:
        return cash


    current_income = income["current_ttm"]
    current_balance  = balance["current"]

    current_cash = cash["current_ttm"]

    total_debt = (
        current_balance["current_debt"]
        + current_balance["noncurrent_debt"]
    )

    # FCF=Operating Cash Flow−Capital Expenditures
    free_cash_flow = (
        current_cash["operating_cash_flow"]
        - abs(current_cash["capital_expenditures"])
    )

    ratios = {

        # Percentage ratios
        # Profitability
        "gross_margin": format_percent_ratio(
            safe_divide(
                current_income["gross_profit"],
                current_income["revenue"],
            )
        ),

        "operating_margin": format_percent_ratio(
            safe_divide(
                current_income["operating_income"],
                current_income["revenue"],
            )
        ),

        "net_margin": format_percent_ratio(
            safe_divide(
                current_income["net_income"],
                current_income["revenue"],
            )
        ),

        # Returns
        "roe": format_percent_ratio(
            safe_divide(
                current_income["net_income"],
                current_balance["stockholders_equity"],
            )
        ),

        "roa": format_percent_ratio(
            safe_divide(
                current_income["net_income"],
                current_balance["assets"],
            )
        ),

        # Number ratios
        # Liquidity
        "current_ratio": format_number_ratio(
            safe_divide(
                current_balance["assets"],
                current_balance["liabilities"],
            )
        ),

        # Leverage
        "debt_to_equity": format_number_ratio(
            safe_divide(
                total_debt,
                current_balance["stockholders_equity"],
            )
        ),


        # Percentage ratios
        # Cash Flow
        "operating_cash_flow_margin": format_percent_ratio(
            safe_divide(
                current_cash["operating_cash_flow"],
                current_income["revenue"],
            )
        ),

        "free_cash_flow_margin": format_percent_ratio(
            safe_divide(
                free_cash_flow,
                current_income["revenue"],
            )
        ),

        "cash_conversion": format_percent_ratio(
            safe_divide(
                current_cash["operating_cash_flow"],
                current_income["net_income"],
            )
        ),
        
    }

    return success_response(
        symbol = symbol,
        period = "TTM",
        date = income["current_ttm"]["latest_date"],
        count = len(ratios),
        ratios = ratios,
    )