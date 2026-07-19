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
    description: str
    rules: list[RatingRule]
    explanations: dict[str, str]


RuleTable = dict[str, MetricRule]

PROFITABILITY_RULES: RuleTable = {

    "gross_margin": {
        "direction": "higher",
        "description": (
            "Measures the percentage of revenue remaining after deducting "
            "the cost of goods sold. Higher margins indicate stronger pricing "
            "power and production efficiency."
        ),
        "rules": [
            (0.50, "Excellent"),
            (0.40, "Good"),
            (0.20, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Exceptional pricing power and cost efficiency.",
            "Good": "Healthy product margins with solid profitability.",
            "Average": "Acceptable margins but room for operational improvement.",
            "Weak": "Low margins may indicate pricing pressure or high production costs.",
        },
    },

    "operating_margin": {
        "direction": "higher",
        "description": (
            "Measures the percentage of revenue remaining after operating "
            "expenses. Indicates how efficiently the core business is managed."
        ),
        "rules": [
            (0.25, "Excellent"),
            (0.15, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Core operations are highly efficient and profitable.",
            "Good": "Strong operating performance with good cost control.",
            "Average": "Business is profitable but operating efficiency can improve.",
            "Weak": "High operating costs are reducing profitability.",
        },
    },

    "net_margin": {
        "direction": "higher",
        "description": (
            "Measures the percentage of revenue that becomes net income after "
            "all expenses, interest, and taxes."
        ),
        "rules": [
            (0.20, "Excellent"),
            (0.10, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Excellent overall profitability and expense management.",
            "Good": "Healthy bottom-line profitability.",
            "Average": "Moderate profitability with room for improvement.",
            "Weak": "Low earnings relative to revenue.",
        },
    },

    "roe": {
        "direction": "higher",
        "description": (
            "Measures how effectively management generates profit from "
            "shareholders' equity."
        ),
        "rules": [
            (0.20, "Excellent"),
            (0.15, "Good"),
            (0.10, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Generating outstanding returns for shareholders.",
            "Good": "Strong shareholder returns.",
            "Average": "Reasonable use of shareholders' capital.",
            "Weak": "Limited profitability relative to shareholders' investment.",
        },
    },

    "roa": {
        "direction": "higher",
        "description": (
            "Measures how efficiently the company generates profit from "
            "its total assets."
        ),
        "rules": [
            (0.10, "Excellent"),
            (0.05, "Good"),
            (0.02, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Assets are being used very efficiently to generate profit.",
            "Good": "Good utilization of company assets.",
            "Average": "Average efficiency in converting assets into earnings.",
            "Weak": "Assets are generating relatively low returns.",
        },
    },
}    

LIQUIDITY_RULES: RuleTable = {

    "current_ratio": {
        "direction": "higher",
        "description": (
            "Measures a company's ability to meet its short-term obligations "
            "using its current assets. A higher ratio generally indicates "
            "stronger short-term financial flexibility."
        ),
        "rules": [
            (2.00, "Excellent"),
            (1.50, "Good"),
            (1.00, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Excellent short-term liquidity with a strong ability to cover current liabilities.",
            "Good": "Healthy liquidity position with sufficient current assets.",
            "Average": "Adequate liquidity, but financial flexibility may be limited.",
            "Weak": "Current assets are lower than current liabilities, increasing short-term liquidity risk.",
        },
    },
}

LEVERAGE_RULES: RuleTable = {

    "debt_to_equity": {
        "direction": "lower",
        "description": (
            "Measures the proportion of debt used to finance the business "
            "relative to shareholders' equity. Lower values generally indicate "
            "lower financial risk."
        ),
        "rules": [
            (0.50, "Excellent"),
            (1.00, "Good"),
            (2.00, "Average"),
            (999, "Weak"),
        ],
        "explanations": {
            "Excellent": "Low financial leverage with a conservative capital structure.",
            "Good": "Debt is well managed and financial risk remains moderate.",
            "Average": "Debt is meaningful but generally manageable.",
            "Weak": "High reliance on debt may increase financial risk and borrowing costs.",
        },
    },
}   

# Lower is better
VALUATION_RULES: RuleTable = {

    "pe_ratio": {
        "direction": "lower",
        "description": (
            "Measures how much investors are willing to pay for each dollar "
            "of the company's earnings. Lower values generally indicate a "
            "more attractive valuation."
        ),
        "rules": [
            (10, "Excellent"),
            (20, "Good"),
            (30, "Fair"),
            (999, "Expensive"),
        ],
        "explanations": {
            "Excellent": "The stock appears attractively valued relative to its earnings.",
            "Good": "Reasonable valuation based on current earnings.",
            "Fair": "Valuation is acceptable but not particularly cheap.",
            "Expensive": "Investors are paying a high price for each dollar of earnings.",
        },
    },

    "peg": {
        "direction": "lower",
        "description": (
            "Compares the P/E ratio with earnings growth. It helps determine "
            "whether a company's valuation is justified by its expected growth."
        ),
        "rules": [
            (1.0, "Excellent"),
            (1.5, "Good"),
            (2.0, "Fair"),
            (999, "Expensive"),
        ],
        "explanations": {
            "Excellent": "Valuation appears attractive relative to earnings growth.",
            "Good": "Growth reasonably supports the current valuation.",
            "Fair": "Valuation is somewhat high compared with growth expectations.",
            "Expensive": "The stock may be overpriced relative to its earnings growth.",
        },
    },

    "price_sales": {
        "direction": "lower",
        "description": (
            "Measures how much investors pay for each dollar of revenue. "
            "Useful when comparing companies with different profit margins "
            "or those with limited earnings."
        ),
        "rules": [
            (2, "Excellent"),
            (5, "Good"),
            (10, "Fair"),
            (999, "Expensive"),
        ],
        "explanations": {
            "Excellent": "Revenue is priced attractively by the market.",
            "Good": "Reasonable valuation relative to revenue.",
            "Fair": "Revenue is priced at a moderate premium.",
            "Expensive": "Investors are paying a high price for each dollar of revenue.",
        },
    },

    "price_book": {
        "direction": "lower",
        "description": (
            "Compares the company's market value with its book value "
            "(shareholders' equity). Often used to evaluate asset-intensive "
            "businesses."
        ),
        "rules": [
            (1, "Excellent"),
            (3, "Good"),
            (5, "Fair"),
            (999, "Expensive"),
        ],
        "explanations": {
            "Excellent": "Market value is close to the company's book value.",
            "Good": "Reasonable valuation relative to shareholders' equity.",
            "Fair": "Trading at a noticeable premium to book value.",
            "Expensive": "The market values the company far above its accounting book value.",
        },
    },
}

FINANCIAL_HEALTH_RULES: RuleTable = {

    "operating_cash_flow_margin": {
        "direction": "higher",
        "description": (
            "Measures the percentage of revenue converted into cash from "
            "core business operations. Higher margins indicate stronger "
            "cash generation and higher earnings quality."
        ),
        "rules": [
            (0.25, "Excellent"),
            (0.15, "Good"),
            (0.08, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Core operations generate substantial cash with excellent earnings quality.",
            "Good": "Healthy operating cash flow supports the business well.",
            "Average": "Operating cash generation is adequate but could be stronger.",
            "Weak": "Limited cash generation from operations may indicate weaker earnings quality.",
        },
    },

    "free_cash_flow_margin": {
        "direction": "higher",
        "description": (
            "Measures the percentage of revenue remaining as free cash flow "
            "after capital expenditures. Higher margins provide greater "
            "financial flexibility for dividends, share buybacks, debt "
            "repayment, and future investments."
        ),
        "rules": [
            (0.20, "Excellent"),
            (0.10, "Good"),
            (0.05, "Average"),
            (0.00, "Weak"),
        ],
        "explanations": {
            "Excellent": "Excellent free cash flow provides strong financial flexibility.",
            "Good": "Healthy free cash flow supports future growth and shareholder returns.",
            "Average": "Positive free cash flow, but financial flexibility is moderate.",
            "Weak": "Limited free cash flow may constrain future investments or capital returns.",
        },
    },
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

    financial_ratio = get_data(symbol)

    if not financial_ratio["success"]:
        return financial_ratio

    ratios = financial_ratio["ratios"]

    analysis = {}

    for key, metric in rules.items():
        ratio = ratios.get(key)
        value = ratio["value"] if ratio else None

        rating_function = (
            get_higher_better_rating
            if metric["direction"] == "higher"
            else get_lower_better_rating
        )

        rating = rating_function(
            value,
            metric["rules"],
        )

        analysis[key] = {
            "value": value,
            "percent": ratio.get("percent") if ratio else None,
            "rating": rating,
            "description": metric["description"],
            "explanation": metric["explanations"].get(
                rating,
                "Insufficient data to evaluate.",
            ),
        }

    return success_response(
        symbol = symbol,
        category = category,
        analysis = analysis,
    )  


def get_profitability_analysis(symbol):
    """
    Return company profitability analysis.
    """

    return get_analysis(
        symbol,
        get_financial_ratios,
        PROFITABILITY_RULES,
        "profitability",
    )

def get_liquidity_analysis(symbol):
    """
    Return company liquidity analysis.
    """

    return get_analysis(
        symbol,
        get_financial_ratios,
        LIQUIDITY_RULES,
        "liquidity",
    )

def get_leverage_analysis(symbol):
    """
    Return company leverage analysis.
    """

    return get_analysis(
        symbol,
        get_financial_ratios,
        LEVERAGE_RULES,
        "leverage",
    )

def get_valuation_analysis(symbol):
    """
    Return company valuation analysis.
    """

    return get_analysis(
        symbol,
        get_valuation_ratios,
        VALUATION_RULES,
        "valuation",
    )

def get_financial_health_analysis(symbol): 
    """
    Return company health analysis.
    """

    return get_analysis(
        symbol,
        get_financial_ratios,
        FINANCIAL_HEALTH_RULES,
        "financial_health",
    )      