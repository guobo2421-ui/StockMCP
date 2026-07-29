from .common import (
    success_response,
    error_response,
)

from .financial_ratios import get_financial_ratios
from .valuation_ratios import get_valuation_ratios

from .financial_analysis import (
    PROFITABILITY_RULES,
    LIQUIDITY_RULES,
    LEVERAGE_RULES,
    VALUATION_RULES,
    FINANCIAL_HEALTH_RULES,
)

from .financial_scoring import (
    score_category,
    score_overall,
    get_profile_weights
)

from .screening_utils import analyze_screening_result


def get_screen_company(
    symbol: str,
    profile: str = "default",
) -> dict:
    """
    Screen a single company using financial and valuation metrics.
    """

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required",
        )

    symbol = symbol.strip().upper()

    financial = get_financial_ratios(symbol)

    if not financial["success"]:
        return financial

    valuation = get_valuation_ratios(symbol)

    if not valuation["success"]:
        return valuation

    ratios = financial["ratios"]
    valuation_ratios = valuation["ratios"]

    categories = {
        "profitability": score_category(
            ratios,
            PROFITABILITY_RULES,
        ),

        "liquidity": score_category(
            ratios,
            LIQUIDITY_RULES,
        ),

        "leverage": score_category(
            ratios,
            LEVERAGE_RULES,
        ),

        "valuation": score_category(
            valuation_ratios,
            VALUATION_RULES,
        ),

        "financial_health": score_category(
            ratios,
            FINANCIAL_HEALTH_RULES,
        ),
    }

    overall_result = score_overall(
        categories,
        weights=get_profile_weights(profile),
    )

    category_scores = {
        name: category["score"]
        for name, category in categories.items()
    }

    strengths, risks = analyze_screening_result(
        category_scores
    )

    return success_response(
        symbol=symbol,
        overall_score=overall_result["score"],
        category_scores=category_scores,
        score_breakdown=overall_result["breakdown"],
        categories=categories,
        strengths=strengths,
        risks=risks,
    )