from .company_screening import screen_company
from .screening_utils import analyze_screening_result

def screen_watchlist(
    symbols: list[str],
    profile: str = "default",
    min_score: int | None = None,
    min_valuation_score: int | None = None,
    min_leverage_score: int | None = None,
) -> dict:

    results = []

    for symbol in symbols:

        result = screen_company(symbol, profile=profile,)

        if result["success"]:
            results.append(result)

    # Apply filters first
    if min_score is not None:
        results = [
            r for r in results
            if r["overall_score"] >= min_score
        ]

    if min_valuation_score is not None:
        results = [
            r for r in results
            if r["category_scores"]["valuation"]
            >= min_valuation_score
        ]

    if min_leverage_score is not None:
        results = [
            r for r in results
            if r["category_scores"]["leverage"]
            >= min_leverage_score
        ]

    # Sort after filtering
    results.sort(
        key=lambda x: x["overall_score"],
        reverse=True,
    )

    rankings = []

    for index, result in enumerate(results, start=1):

        rankings.append(
            {
                "rank": index,
                "symbol": result["symbol"],
                "overall_score": result["overall_score"],
                "category_scores": result["category_scores"],
                "score_breakdown": result["score_breakdown"],
                "strengths": result["strengths"],
                "risks": result["risks"],
            }
        )

    return {
        "success": True,
        "count": len(rankings),
        "rankings": rankings,
        "filters": {
            "min_score": min_score,
            "min_valuation_score": min_valuation_score,
            "min_leverage_score": min_leverage_score,
        },        
    }