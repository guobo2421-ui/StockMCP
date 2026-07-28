from typing import Any

from .financial_analysis import (
    MetricRule,
    RuleTable,
    get_higher_better_rating,
    get_lower_better_rating,
)


# Rating -> numeric score
RATING_SCORES = {
    "Excellent": 100,
    "Good": 80,
    "Average": 60,
    "Fair": 60,
    "Weak": 40,
    "Expensive": 40,
    "Unknown": 0,
}

PROFILE_WEIGHTS = {
    # Balanced scoring
    "default": {
        "profitability": 0.20,
        "liquidity": 0.20,
        "leverage": 0.20,
        "valuation": 0.20,
        "financial_health": 0.20,
    },

    # Emphasize valuation
    "value": {
        "profitability": 0.15,
        "liquidity": 0.15,
        "leverage": 0.15,
        "valuation": 0.40,
        "financial_health": 0.15,
    },

    # Emphasize balance-sheet safety
    "safe": {
        "profitability": 0.20,
        "liquidity": 0.25,
        "leverage": 0.25,
        "valuation": 0.10,
        "financial_health": 0.20,
    },
}


def score_metric(
    value: float | None,
    rule: MetricRule,
) -> int:
    """
    Convert a metric value into a numeric score (0-100).

    This uses the same rules as financial_analysis.py so there is
    only one source of truth for thresholds.

    Returns
    -------
    int
        Score from 0 to 100.
    """

    if value is None:
        return 0

    rating_function = (
        get_higher_better_rating
        if rule["direction"] == "higher"
        else get_lower_better_rating
    )

    rating = rating_function(
        value,
        rule["rules"],
    )

    return RATING_SCORES.get(rating, 0)


def score_category(
    ratios: dict[str, Any],
    rules: RuleTable,
) -> dict[str, Any]:
    """
    Score all metrics in a category.

    Parameters
    ----------
    ratios
        Dictionary returned by get_financial_ratios()["ratios"]
        or get_valuation_ratios()["ratios"].

    rules
        One of:
            PROFITABILITY_RULES
            LIQUIDITY_RULES
            LEVERAGE_RULES
            VALUATION_RULES
            FINANCIAL_HEALTH_RULES

    Returns
    -------
    {
        "score": 86,
        "metrics": {
            "gross_margin": {
                "value": 0.47,
                "score": 80
            },
            ...
        }
    }
    """

    metrics: dict[str, Any] = {}

    total_score = 0
    metric_count = 0

    for metric_name, rule in rules.items():

        ratio = ratios.get(metric_name)

        value = ratio["value"] if ratio else None

        score = score_metric(
            value,
            rule,
        )

        metrics[metric_name] = {
            "value": value,
            "score": score,
        }

        if value is not None:
            total_score += score
            metric_count += 1

    category_score = (
        round(total_score / metric_count)
        if metric_count
        else 0
    )

    return {
        "score": category_score,
        "metrics": metrics,
    }


def score_overall(
    categories: dict[str, dict[str, Any]],
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Calculate overall score from category scores.

    Parameters
    ----------
    categories
        Dictionary containing category results.

    Example
    -------
    {
        "profitability": {
            "score": 96,
            "metrics": {...}
        },
        "valuation": {
            "score": 50,
            "metrics": {...}
        }
    }

    Returns
    -------
    {
        "score": 77,
        "breakdown": {
            "profitability": {
                "score": 96,
                "weight": 0.2,
                "contribution": 19.2
            }
        }
    }
    """

    if not categories:
        return {
            "score": 0,
            "breakdown": {},
        }

    if weights is None:
        weights = DEFAULT_WEIGHTS["default"]

    weight_total = sum(weights.values())

    if round(weight_total, 2) != 1.0:
        raise ValueError(
            "Weights must sum to 1.0"
        )

    total = 0
    breakdown = {}

    for name, category in categories.items():

        score = category["score"]

        weight = weights.get(name, 0)

        contribution = score * weight

        total += contribution

        breakdown[name] = {
            "score": score,
            "weight": weight,
            "contribution": round(contribution, 2),
        }


    return {
        "score": round(total),
        "breakdown": breakdown,
    }

def get_profile_weights(profile: str) -> dict[str, float]:
    return PROFILE_WEIGHTS.get(
        profile,
        PROFILE_WEIGHTS["default"],
    )    