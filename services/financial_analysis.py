from typing import Any, Callable, TypedDict, Literal

from .financial_ratios import get_financial_ratios
from .valuation_ratios import get_valuation_ratios
from .common import (
    success_response,
    error_response,
)


RatingRule = tuple[float, str]
class MetricRule(TypedDict):
    direction: Literal["higher", "lower"]
    rules: list[RatingRule]


RuleTable = dict[str, MetricRule]

PROFITABILITY_RULES: RuleTable = {

    "gross_margin": {
        "direction": "higher",
        "rules": [         
            (0.50, "Excellent"),
            (0.40, "Good"),
            (0.20, "Average"),
            (0.00, "Weak"),
        ]
    },

    "operating_margin": {
        "direction": "higher",
        "rules": [         
            (0.25, "Excellent"),
            (0.15, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ]
    },

    "net_margin": {
        "direction": "higher",
        "rules": [ 
            (0.20, "Excellent"),
            (0.10, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ]
    },

    "roe": {
        "direction": "higher",
        "rules": [         
            (0.20, "Excellent"),
            (0.15, "Good"),
            (0.10, "Average"),
            (0.00, "Weak"),
        ]
    },

    "roa": {
        "direction": "higher",
        "rules": [         
            (0.10, "Excellent"),
            (0.05, "Good"),
            (0.02, "Average"),
            (0.00, "Weak"),
        ]
    }
}    

LIQUIDITY_RULES: RuleTable = {
    "current_ratio": {
        "direction": "higher",
        "rules": [         
            (2.00, "Excellent"),
            (1.50, "Good"),
            (1.00, "Average"),
            (0.00, "Weak"),
        ]
    }
}

LEVERAGE_RULES: RuleTable = {

    "debt_to_equity": {
        "direction": "lower",
        "rules": [        
            (0.50, "Excellent"),
            (1.00, "Good"),
            (2.00, "Average"),
            (999, "Weak"),
        ]
    },
}    

# Lower is better
VALUATION_RULES: RuleTable = {

    "pe_ratio": {
        "direction": "lower",
        "rules": [
            (10, "Excellent"),
            (20, "Good"),
            (30, "Fair"),
            (999, "Expensive"),
        ]
    },

    "peg": {
        "direction": "lower",
        "rules": [
            (1.0, "Excellent"),
            (1.5, "Good"),
            (2.0, "Fair"),
            (999, "Expensive"),
        ]
    },

    "price_sales": {
        "direction": "lower",        
        "rules": [       
            (2, "Excellent"),
            (5, "Good"),
            (10, "Fair"),
            (999, "Expensive"),
        ]
    },

    "price_book": {
        "direction": "lower",
        "rules": [
            (1, "Excellent"),
            (3, "Good"),
            (5, "Fair"),
            (999, "Expensive"),
        ]
    },
}

FINANCIAL_HEALTH_RULES: RuleTable = {
    "operating_cash_flow_margin": {
        "direction": "higher",
        "rules": [ 
            (0.25, "Excellent"),
            (0.15, "Good"),
            (0.08, "Average"),
            (0.00, "Weak"),
        ]
    },

    "free_cash_flow_margin": {
        "direction": "higher",
        "rules": [         
            (0.20, "Excellent"),
            (0.10, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ]
    }
}


def get_higher_better_rating(
    value: float | None,
    rules: list[tuple[float, str]],
) -> str:

    if value is None:
        return "Unknown"

    for threshold, rating in rules:
        if value >= threshold:
            return rating

    return "Unknown"

def get_lower_better_rating(
    value: float | None,
    rules: list[tuple[float, str]],
) -> str:

    if value is None:
        return "Unknown"

    for threshold, rating in rules:
        if value <= threshold:
            return rating

    return "Unknown"

def get_analysis(
    symbol: str,
    period: str = "annual",
    get_data: Callable[[str, str], dict[str, Any]] = get_financial_ratios,
    rules: RuleTable = PROFITABILITY_RULES, 
    category: str = "profitability",
) -> dict[str, Any]:
    """
    Return company analysis.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    financial_ratio = get_data(symbol, period)

    if not financial_ratio["success"]:
        return financial_ratio

    ratios = financial_ratio["ratios"]

    analysis = {}

    for key, rules in rules.items():
        ratio = ratios.get(key)
        value = ratio["value"] if ratio else None

        rule = rules["rules"]
        direction = rules["direction"]

        if direction == "higher":
            rating = get_higher_better_rating(value, rule)
        else:
            rating = get_lower_better_rating(value, rule)

        analysis[key] = {
            "value": value,
            "rating": rating
        }

    return success_response(
        symbol = symbol,
        period = period,
        category = category,
        analysis = analysis,
    )  


def get_profitability_analysis(symbol, period="annual"):
    """
    Return company profitability analysis.
    """

    return get_analysis(
        symbol,
        period,
        get_financial_ratios,
        PROFITABILITY_RULES,
        "profitability",
    )

def get_liquidity_analysis(symbol, period="annual"):
    """
    Return company liquidity analysis.
    """

    return get_analysis(
        symbol,
        period,
        get_financial_ratios,
        LIQUIDITY_RULES,
        "liquidity",
    )

def get_leverage_analysis(symbol, period="annual"):
    """
    Return company leverage analysis.
    """

    return get_analysis(
        symbol,
        period,
        get_financial_ratios,
        LEVERAGE_RULES,
        "leverage",
    )

def get_valuation_analysis(symbol, period="annual"):
    """
    Return company valuation analysis.
    """

    return get_analysis(
        symbol,
        period,
        get_valuation_ratios,
        VALUATION_RULES,
        "valuation",
    )

def get_financial_health_analysis(symbol, period="annual"): 
    """
    Return company health analysis.
    """

    return get_analysis(
        symbol,
        period,
        get_financial_ratios,
        FINANCIAL_HEALTH_RULES,
        "financial_health",
    )      