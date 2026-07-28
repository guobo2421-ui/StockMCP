CATEGORY_LABELS = {
    "financial_health": "financial health",
}


def analyze_screening_result(
    category_scores: dict[str, int]
) -> tuple[list[str], list[str]]:

    strengths = []
    risks = []

    for category, score in category_scores.items():

        label = CATEGORY_LABELS.get(
            category,
            category,
        )

        if score >= 90:
            strengths.append(
                f"Excellent {label}"
            )

        elif score < 60:
            risks.append(
                f"Weak {label}"
            )

        elif score < 70:
            risks.append(
                f"Moderate {label}"
            )

    return strengths, risks