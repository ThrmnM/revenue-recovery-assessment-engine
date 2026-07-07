"""Shared output contract for Business Intelligence categories."""

from typing import Any, Dict, Iterable, List, Optional


CATEGORY_OUTPUT_FIELDS = (
    "score",
    "confidence",
    "explanation",
    "strengths",
    "weaknesses",
    "recommended_improvements",
    "revenue_opportunities",
    "service_opportunities",
    "missing_inputs",
)


def clamp_score(value: Any) -> int:
    """Return a whole-number score between 0 and 100."""

    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        number = 0

    return max(0, min(100, number))


def list_value(items: Optional[Iterable[Any]]) -> List[Any]:
    """Normalize optional iterable values into a list."""

    if items is None:
        return []

    if isinstance(items, list):
        return items

    return list(items)


def make_category_output(
    score: Any,
    confidence: Any,
    explanation: str,
    strengths: Optional[Iterable[Any]] = None,
    weaknesses: Optional[Iterable[Any]] = None,
    recommended_improvements: Optional[Iterable[Any]] = None,
    revenue_opportunities: Optional[Iterable[Any]] = None,
    service_opportunities: Optional[Iterable[Any]] = None,
    missing_inputs: Optional[Iterable[Any]] = None,
) -> Dict[str, Any]:
    """Create a category output that satisfies the frozen contract."""

    return {
        "score": clamp_score(score),
        "confidence": clamp_score(confidence),
        "explanation": str(explanation).strip(),
        "strengths": list_value(strengths),
        "weaknesses": list_value(weaknesses),
        "recommended_improvements": list_value(recommended_improvements),
        "revenue_opportunities": list_value(revenue_opportunities),
        "service_opportunities": list_value(service_opportunities),
        "missing_inputs": list_value(missing_inputs),
    }


def validate_category_output(output: Dict[str, Any]) -> bool:
    """Return whether a category output includes every required field."""

    return all(field in output for field in CATEGORY_OUTPUT_FIELDS)
