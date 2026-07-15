from typing import Any

from .financial_ratio import get_financial_ratios
from .common import (
    success_response,
    error_response,
)


PROFITABILITY_RULES = {

    "gross_margin": [
        (0.50, "Excellent"),
        (0.40, "Good"),
        (0.20, "Average"),
        (0.00, "Weak"),
    ],

    "operating_margin": [
        (0.25, "Excellent"),
        (0.15, "Good"),
        (0.05, "Average"),
        (0.00, "Weak"),
    ],

    "net_margin": [
        (0.20, "Excellent"),
        (0.10, "Good"),
        (0.05, "Average"),
        (0.00, "Weak"),
    ],

    "roe": [
        (0.20, "Excellent"),
        (0.15, "Good"),
        (0.10, "Average"),
        (0.00, "Weak"),
    ],

    "roa": [
        (0.10, "Excellent"),
        (0.05, "Good"),
        (0.02, "Average"),
        (0.00, "Weak"),
    ]
}


def get_rating(
    value: float | None,
    rules: list[tuple[float, str]],
) -> str:

    if value is None:
        return "Unknown"

    for threshold, rating in rules:
        if value >= threshold:
            return rating

    return "Unknown"


def get_profitability_analysis(
    symbol: str,
    period: str = "annual",
) -> dict[str, Any]:
    """
    Return company profitability analysis.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    financial_ratio = get_financial_ratios(symbol, period)
    if not financial_ratio["success"]:
        return financial_ratio

    ratios = financial_ratio["ratios"]

    profitability = {}

    for key, rules in PROFITABILITY_RULES.items():
        ratio = ratios.get(key)
        value = ratio["value"] if ratio else None

        profitability[key] = {
            "value": value,
            "rating": get_rating(
                value,
                rules
            )
        }

    return success_response(
        symbol = symbol,
        period = period,
        profitability = profitability,
    )     