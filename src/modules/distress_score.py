"""Distress scoring for revenue recovery assessments."""

from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union


CompanyData = Mapping[str, Any]
AssessmentData = Mapping[str, Any]
CompetitorData = Mapping[str, Any]
CompetitorInput = Union[
    Sequence[CompetitorData],
    Mapping[str, Sequence[CompetitorData]],
]


def calculate_distress_score(
    company: CompanyData,
    competitors: CompetitorInput,
    assessment: AssessmentData,
) -> Dict[str, Any]:
    """
    Calculate a company's distress score from reputation and operations data.

    The score measures business risk and revenue recovery urgency. Higher
    scores indicate more severe distress. The final score is capped at 100.
    """

    score = 0
    reasons: List[str] = []

    review_count = int(company.get("review_count", 0))
    rating = float(company.get("rating", 0))

    # Google Reviews
    if review_count < 25:
        score += 30
        reasons.append(
            f"Google review count is below 25 ({review_count}), adding 30 points."
        )
    elif review_count <= 50:
        score += 20
        reasons.append(
            f"Google review count is between 25 and 50 ({review_count}), "
            "adding 20 points."
        )
    elif review_count <= 100:
        score += 10
        reasons.append(
            f"Google review count is between 50 and 100 ({review_count}), "
            "adding 10 points."
        )

    # Google Rating
    if rating < 4.2:
        score += 25
        reasons.append(
            f"Google rating is below 4.2 ({rating:.1f}), adding 25 points."
        )
    elif rating <= 4.5:
        score += 10
        reasons.append(
            f"Google rating is between 4.2 and 4.5 ({rating:.1f}), "
            "adding 10 points."
        )

    # Operational distress indicators can come from company data or from the
    # broader assessment result if they are not stored directly on the company.
    if _is_flagged(company, assessment, "missed_calls"):
        score += 15
        reasons.append(
            "Missed calls are present, adding 15 points."
        )

    if _is_flagged(company, assessment, "quote_delay"):
        score += 10
        reasons.append(
            "Quote delays are present, adding 10 points."
        )

    if _is_flagged(company, assessment, "poor_communication"):
        score += 10
        reasons.append(
            "Poor communication is present, adding 10 points."
        )

    if _is_flagged(company, assessment, "late_technicians"):
        score += 10
        reasons.append(
            "Late technicians are present, adding 10 points."
        )

    competitor_score, competitor_reason = _score_competitor_review_ratio(
        review_count,
        competitors,
    )

    if competitor_score:
        score += competitor_score
        reasons.append(competitor_reason)

    score = min(score, 100)

    return {
        "score": int(score),
        "grade": _get_grade(score),
        "priority": _get_priority(score),
        "reasons": reasons,
    }


def _is_flagged(
    company: CompanyData,
    assessment: AssessmentData,
    key: str,
) -> bool:
    """
    Return whether a distress indicator is active.

    Company data is the primary source. Assessment data is used only as a
    fallback so callers can pass derived assessment fields without duplicating
    them on the company record.
    """

    if key in company:
        return bool(company.get(key))

    return bool(assessment.get(key))


def _score_competitor_review_ratio(
    review_count: int,
    competitors: CompetitorInput,
) -> Tuple[int, str]:
    """Score the largest competitor review multiple."""

    competitor_list = _normalize_competitors(competitors)

    if review_count <= 0 or not competitor_list:
        return 0, ""

    top_competitor = max(
        competitor_list,
        key=lambda competitor: int(competitor.get("review_count", 0)),
    )

    top_reviews = int(top_competitor.get("review_count", 0))
    review_ratio = top_reviews / review_count
    competitor_name = top_competitor.get("name", "A competitor")

    if review_ratio >= 8:
        return (
            20,
            f"{competitor_name} has {review_ratio:.1f}x more Google reviews "
            "than the company, adding 20 points.",
        )

    if review_ratio >= 5:
        return (
            10,
            f"{competitor_name} has {review_ratio:.1f}x more Google reviews "
            "than the company, adding 10 points.",
        )

    return 0, ""


def _normalize_competitors(
    competitors: CompetitorInput,
) -> Sequence[CompetitorData]:
    """Return competitors from either a raw list or a wrapped data structure."""

    if isinstance(competitors, Mapping):
        return competitors.get("competitors", [])

    return competitors


def _get_priority(score: int) -> str:
    """Return the priority label for a distress score."""

    if score >= 90:
        return "CRITICAL"
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"

    return "LOW"


def _get_grade(score: int) -> str:
    """Return the grade label for a distress score."""

    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"

    return "F"
