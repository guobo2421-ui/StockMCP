from typing import Any

from .company_screening import get_screen_company


def build_best_in_class_summary(
    comparisons: list[dict[str, Any]],
    best: dict[str, Any],
) -> dict[str, str]:

    if not comparisons:
        return {}

    weakest_leverage = min(
        comparisons,
        key=lambda x: x["category_scores"]["leverage"],
    )

    return {
        "overall_winner": (
            f"{best['overall']} ranks highest "
            "based on the financial screening score"
        ),

        "best_value": (
            f"{best['valuation'][0]} has the strongest "
            "valuation score among this watchlist"
        ),

        "main_risk": (
            f"{weakest_leverage['symbol']} has the weakest "
            "leverage score among this watchlist"
        ),
    }

def get_best_in_class(
    comparisons: list[dict[str, Any]]
) -> dict[str, Any]:

    if not comparisons:
        return {}

    best = {}

    # Highest overall score
    best["overall"] = max(
        comparisons,
        key=lambda x: x["overall_score"],
    )["symbol"]

    categories = [
        "profitability",
        "liquidity",
        "leverage",
        "valuation",
        "financial_health",
    ]

    for category in categories:

        highest_score = max(
            item["category_scores"][category]
            for item in comparisons
        )

        best[category] = [
            item["symbol"]
            for item in comparisons
            if item["category_scores"][category]
            == highest_score
        ]

    best["summary"] = build_best_in_class_summary(
        comparisons,
        best,
    )

    return best    

def get_compare_watchlist(
    symbols: list[str],
) -> dict[str, Any]:

    comparisons = []

    for symbol in symbols:

        result = get_screen_company(symbol)

        if not result["success"]:
            continue

        comparisons.append(
            {
                "symbol": result["symbol"],

                "overall_score": result["overall_score"],

                "category_scores": result["category_scores"],

                "strengths": result.get(
                    "strengths",
                    []
                ),

                "risks": result.get(
                    "risks",
                    []
                ),
            }
        )

    # Highest score first
    comparisons.sort(
        key=lambda x: x["overall_score"],
        reverse=True,
    )

    return {
        "success": True,
        "count": len(comparisons),

        "best_in_class": get_best_in_class(
            comparisons
        ),

        "comparison": comparisons,
    }

