"""Business Intelligence Engine orchestration."""

from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from modules.business_intelligence.category_output import (
    clamp_score,
    validate_category_output,
)
from modules.business_intelligence.categories.automation_readiness import (
    score_automation_readiness,
)
from modules.business_intelligence.categories.competitive_position import (
    score_competitive_position,
)
from modules.business_intelligence.categories.digital_presence import (
    score_digital_presence,
)
from modules.business_intelligence.categories.google_reputation import (
    score_google_reputation,
)
from modules.business_intelligence.categories.revenue_opportunity import (
    score_revenue_opportunity,
)
from modules.business_intelligence.config import get_config
from modules.business_intelligence.service_mapper import (
    collect_service_opportunities,
    map_recommended_services,
)


CATEGORY_SCORERS = {
    "google_reputation": score_google_reputation,
    "competitive_position": score_competitive_position,
    "digital_presence": score_digital_presence,
    "automation_readiness": score_automation_readiness,
    "revenue_opportunity": score_revenue_opportunity,
}


def calculate_business_intelligence(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config_overrides: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Calculate the complete Business Intelligence assessment."""

    config = get_config(dict(config_overrides or {}))
    competitors = list(competitors or [])
    assessment = assessment or {}

    category_outputs = _run_categories(
        company,
        competitors,
        assessment,
        config,
    )

    recommended_services = map_recommended_services(
        category_outputs,
        config,
    )
    business_score = _business_intelligence_score(
        category_outputs,
        config,
    )
    revenue_score = _revenue_opportunity_score(category_outputs)
    confidence = _assessment_confidence(category_outputs)
    priority_score = _priority_score(
        business_score,
        revenue_score,
        confidence,
        config,
    )
    grade = _business_grade(business_score, config)

    strengths = _aggregate_strings(category_outputs, "strengths")
    weaknesses = _aggregate_strings(category_outputs, "weaknesses")
    improvements = _aggregate_strings(
        category_outputs,
        "recommended_improvements",
    )
    revenue_opportunities = _aggregate_opportunities(category_outputs)
    missing_inputs = _aggregate_missing_inputs(category_outputs)
    quick_wins = _quick_wins(category_outputs)
    service_opportunities = collect_service_opportunities(
        recommended_services
    )

    return {
        "business_intelligence_score": business_score,
        "business_grade": grade,
        "revenue_opportunity_score": revenue_score,
        "priority_score": priority_score,
        "assessment_confidence": confidence,
        "category_scores": category_outputs,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommended_improvements": improvements,
        "revenue_opportunities": revenue_opportunities,
        "service_opportunities": service_opportunities,
        "recommended_services": recommended_services,
        "quick_wins": quick_wins,
        "missing_inputs": missing_inputs,
        "score": business_score,
        "grade": grade,
        "confidence": confidence,
    }


def _run_categories(
    company: Mapping[str, Any],
    competitors: Sequence[Mapping[str, Any]],
    assessment: Mapping[str, Any],
    config: Mapping[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """Run enabled category scorers."""

    outputs = {}

    for category_name in config.get("enabled_categories", []):
        scorer = CATEGORY_SCORERS.get(category_name)

        if scorer is None:
            continue

        output = scorer(company, competitors, assessment, config)

        if not validate_category_output(output):
            raise ValueError(
                f"{category_name} did not return the category output contract."
            )

        outputs[category_name] = output

    return outputs


def _business_intelligence_score(
    category_outputs: Mapping[str, Mapping[str, Any]],
    config: Mapping[str, Any],
) -> int:
    """Calculate the configured weighted Business Intelligence Score."""

    weights = config.get("business_intelligence_weights", {})
    weighted_total = 0.0
    total_weight = 0.0

    for category_name, weight in weights.items():
        output = category_outputs.get(category_name)

        if output is None:
            continue

        weighted_total += output["score"] * float(weight)
        total_weight += float(weight)

    if total_weight == 0:
        return 0

    return clamp_score(weighted_total / total_weight)


def _revenue_opportunity_score(
    category_outputs: Mapping[str, Mapping[str, Any]],
) -> int:
    """Calculate the separate Revenue Opportunity Score."""

    revenue_category = category_outputs.get("revenue_opportunity")

    if revenue_category:
        return clamp_score(100 - revenue_category["score"])

    opportunity_count = len(_aggregate_opportunities(category_outputs))
    return clamp_score(opportunity_count * 15)


def _assessment_confidence(
    category_outputs: Mapping[str, Mapping[str, Any]],
) -> int:
    """Calculate data-quality confidence from category confidences."""

    if not category_outputs:
        return 0

    total = sum(
        output["confidence"]
        for output in category_outputs.values()
    )

    return clamp_score(total / len(category_outputs))


def _priority_score(
    business_score: int,
    revenue_score: int,
    confidence: int,
    config: Mapping[str, Any],
) -> int:
    """Calculate internal outreach priority."""

    rules = config.get("priority_rules", {})
    health_gap = 100 - business_score
    confidence_gap = 100 - confidence

    score = (
        health_gap * rules.get("business_health_gap_weight", 0.45)
        + revenue_score * rules.get("revenue_opportunity_weight", 0.45)
        + confidence_gap * rules.get("confidence_gap_weight", 0.10)
    )

    return clamp_score(score)


def _business_grade(score: int, config: Mapping[str, Any]) -> str:
    """Return configured grade for the Business Intelligence Score."""

    boundaries = sorted(
        config.get("grade_boundaries", []),
        key=lambda boundary: boundary["minimum"],
        reverse=True,
    )

    for boundary in boundaries:
        if score >= boundary["minimum"]:
            return boundary["grade"]

    return "F"


def _aggregate_strings(
    category_outputs: Mapping[str, Mapping[str, Any]],
    field: str,
) -> List[str]:
    """Aggregate unique strings from category outputs."""

    values = []

    for output in category_outputs.values():
        for item in output.get(field, []):
            if isinstance(item, str) and item not in values:
                values.append(item)

    return values


def _aggregate_opportunities(
    category_outputs: Mapping[str, Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    """Aggregate unique revenue opportunities."""

    opportunities = []
    seen: set[Tuple[str, str]] = set()

    for output in category_outputs.values():
        for item in output.get("revenue_opportunities", []):
            opportunity = _normalize_opportunity(item)
            key = (
                opportunity.get("condition", ""),
                opportunity.get("opportunity", ""),
            )

            if key in seen:
                continue

            seen.add(key)
            opportunities.append(opportunity)

    return opportunities


def _aggregate_missing_inputs(
    category_outputs: Mapping[str, Mapping[str, Any]],
) -> List[str]:
    """Aggregate unique missing inputs with category context."""

    missing = []

    for category_name, output in category_outputs.items():
        category_label = _label(category_name)

        for item in output.get("missing_inputs", []):
            value = f"{category_label}: {item}"

            if value not in missing:
                missing.append(value)

    return missing


def _quick_wins(
    category_outputs: Mapping[str, Mapping[str, Any]],
) -> List[str]:
    """Return required quick wins from category recommendations."""

    quick_wins = []

    for output in category_outputs.values():
        for item in output.get("recommended_improvements", []):
            if item not in quick_wins:
                quick_wins.append(item)

    defaults = [
        "Claim Google Business Profile.",
        "Post one completed project every week.",
        "Begin requesting Google Reviews.",
        "Add an Online Quote Form.",
        "Respond to recent reviews.",
    ]

    for item in defaults:
        if item not in quick_wins:
            quick_wins.append(item)

    return quick_wins[:6]


def _normalize_opportunity(item: Any) -> Dict[str, Any]:
    """Return a revenue opportunity dictionary."""

    if isinstance(item, Mapping):
        return dict(item)

    return {
        "condition": "",
        "opportunity": str(item),
    }


def _label(value: str) -> str:
    """Return a business-readable label for an internal key."""

    return value.replace("_", " ").title()
