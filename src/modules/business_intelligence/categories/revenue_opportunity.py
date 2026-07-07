"""Revenue opportunity analysis."""

from typing import Any, Dict, Mapping, Optional, Sequence

from modules.business_intelligence.category_output import (
    clamp_score,
    make_category_output,
)


def score_revenue_opportunity(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Score revenue condition while exposing upside opportunities.

    The category score follows the shared category contract: higher score means
    healthier performance. The engine converts this into a separate Revenue
    Opportunity Score where higher means greater upside.
    """

    confidence_penalty = _penalty(config)
    competitors = list(competitors or [])
    assessment = assessment or {}

    opportunity_score = 0
    confidence = 100
    strengths = []
    weaknesses = []
    improvements = []
    revenue_opportunities = []
    service_opportunities = []
    missing_inputs = []
    explanation_parts = []

    estimated_loss = _estimated_loss(company, competitors, assessment)

    if estimated_loss is None:
        confidence -= confidence_penalty
        missing_inputs.append("Estimated Revenue Leakage")
        explanation_parts.append(
            "Estimated revenue leakage was unavailable, so no leakage opportunity was scored."
        )
    elif estimated_loss >= 100000:
        opportunity_score += 35
        weaknesses.append("Estimated revenue leakage is high.")
        improvements.append("Prioritize revenue recovery systems within the next 90 days.")
        revenue_opportunities.append({
            "condition": "low_automation",
            "opportunity": "Recover material annual revenue leakage.",
            "estimated_revenue_improvement": int(estimated_loss),
        })
        service_opportunities.append("low_automation")
        explanation_parts.append(
            f"Estimated revenue leakage is ${estimated_loss:,.0f}, adding 35 opportunity points."
        )
    elif estimated_loss >= 50000:
        opportunity_score += 25
        weaknesses.append("Estimated revenue leakage is meaningful.")
        improvements.append("Address the highest-confidence recovery opportunities first.")
        revenue_opportunities.append({
            "condition": "low_automation",
            "opportunity": "Recover meaningful annual revenue leakage.",
            "estimated_revenue_improvement": int(estimated_loss),
        })
        service_opportunities.append("low_automation")
        explanation_parts.append(
            f"Estimated revenue leakage is ${estimated_loss:,.0f}, adding 25 opportunity points."
        )
    elif estimated_loss > 0:
        opportunity_score += 10
        strengths.append("Revenue leakage appears limited.")
        improvements.append("Monitor leakage indicators and continue improving follow-up.")
        explanation_parts.append(
            f"Estimated revenue leakage is ${estimated_loss:,.0f}, adding 10 opportunity points."
        )
    else:
        strengths.append("No revenue leakage estimate is currently confirmed.")
        explanation_parts.append(
            "No confirmed revenue leakage was identified from available data."
        )

    review_gap = _review_gap(company, competitors, assessment)

    if review_gap is None:
        confidence -= confidence_penalty
        missing_inputs.append("Competitor Review Gap")
    elif review_gap >= 150:
        opportunity_score += 25
        weaknesses.append("Competitors have a large review advantage.")
        improvements.append("Use reputation growth to recover local search demand.")
        revenue_opportunities.append({
            "condition": "competitive_review_gap",
            "opportunity": "Recover demand likely going to better-reviewed competitors.",
            "estimated_revenue_improvement": int(review_gap * 500),
        })
        service_opportunities.append("competitive_review_gap")
        explanation_parts.append(
            f"Competitor review gap is {review_gap:.0f}, adding 25 opportunity points."
        )
    elif review_gap >= 50:
        opportunity_score += 15
        weaknesses.append("Competitors have a measurable review advantage.")
        improvements.append("Increase review requests after completed projects.")
        revenue_opportunities.append({
            "condition": "competitive_review_gap",
            "opportunity": "Improve trust and local conversion by closing the review gap.",
            "estimated_revenue_improvement": int(review_gap * 500),
        })
        service_opportunities.append("competitive_review_gap")
        explanation_parts.append(
            f"Competitor review gap is {review_gap:.0f}, adding 15 opportunity points."
        )

    rating_gap = _rating_gap(company, competitors)

    if rating_gap is None:
        confidence -= confidence_penalty
        missing_inputs.append("Competitor Rating Gap")
    elif rating_gap >= 0.5:
        opportunity_score += 10
        weaknesses.append("Competitors have a clear rating advantage.")
        revenue_opportunities.append({
            "condition": "poor_reviews",
            "opportunity": "Improve trust where competitors currently look stronger.",
        })
        service_opportunities.append("poor_reviews")
        explanation_parts.append(
            f"Competitor rating gap is {rating_gap:.1f}, adding 10 opportunity points."
        )
    elif rating_gap >= 0.2:
        opportunity_score += 5
        weaknesses.append("Competitors have a slight rating advantage.")
        revenue_opportunities.append({
            "condition": "poor_reviews",
            "opportunity": "Close the rating gap before it affects conversion further.",
        })
        service_opportunities.append("poor_reviews")
        explanation_parts.append(
            f"Competitor rating gap is {rating_gap:.1f}, adding 5 opportunity points."
        )

    if company.get("missed_calls"):
        opportunity_score += 10
        revenue_opportunities.append({
            "condition": "missed_calls",
            "opportunity": "Capture leads currently lost when calls are missed.",
            "estimated_revenue_improvement": 35000,
        })
        service_opportunities.append("missed_calls")

    if company.get("quote_delay"):
        opportunity_score += 10
        revenue_opportunities.append({
            "condition": "quote_delay",
            "opportunity": "Improve quote conversion through faster follow-up.",
            "estimated_revenue_improvement": 30000,
        })
        service_opportunities.append("quote_delay")

    if company.get("website_exists") is False:
        opportunity_score += 10
        revenue_opportunities.append({
            "condition": "no_website",
            "opportunity": "Capture search traffic and convert visitors into quote requests.",
        })
        service_opportunities.append("no_website")

    if company.get("facebook_active_within_90_days") is False:
        opportunity_score += 5
        revenue_opportunities.append({
            "condition": "inactive_facebook",
            "opportunity": "Improve trust with visible recent work.",
        })
        service_opportunities.append("inactive_facebook")

    opportunity_score = clamp_score(opportunity_score)
    health_score = 100 - opportunity_score

    if not explanation_parts:
        explanation_parts.append(
            "Revenue opportunity showed no confirmed negative signals."
        )

    return make_category_output(
        score=health_score,
        confidence=confidence,
        explanation=" ".join(explanation_parts),
        strengths=strengths,
        weaknesses=weaknesses,
        recommended_improvements=improvements,
        revenue_opportunities=revenue_opportunities,
        service_opportunities=service_opportunities,
        missing_inputs=missing_inputs,
    )


def _estimated_loss(
    company: Mapping[str, Any],
    competitors: Sequence[Mapping[str, Any]],
    assessment: Mapping[str, Any],
) -> Optional[float]:
    """Return the best available revenue leakage estimate."""

    for key in ("estimated_revenue_leakage", "estimated_loss"):
        if assessment.get(key) is not None:
            return float(assessment[key])
        if company.get(key) is not None:
            return float(company[key])

    gap = _review_gap(company, competitors, assessment)

    if gap is None:
        return None

    return max(0, gap * 500)


def _review_gap(
    company: Mapping[str, Any],
    competitors: Sequence[Mapping[str, Any]],
    assessment: Mapping[str, Any],
) -> Optional[float]:
    """Return average competitor review gap when available."""

    for key in ("competitor_review_gap", "review_gap"):
        if assessment.get(key) is not None:
            return float(assessment[key])
        if company.get(key) is not None:
            return float(company[key])

    review_count = company.get("review_count")
    competitor_reviews = [
        int(competitor["review_count"])
        for competitor in competitors
        if competitor.get("review_count") is not None
    ]

    if review_count is None or not competitor_reviews:
        return None

    return (sum(competitor_reviews) / len(competitor_reviews)) - int(review_count)


def _rating_gap(
    company: Mapping[str, Any],
    competitors: Sequence[Mapping[str, Any]],
) -> Optional[float]:
    """Return average competitor rating gap when available."""

    rating = company.get("rating")
    competitor_ratings = [
        float(competitor["rating"])
        for competitor in competitors
        if competitor.get("rating") is not None
    ]

    if rating is None or not competitor_ratings:
        return None

    return (sum(competitor_ratings) / len(competitor_ratings)) - float(rating)


def _penalty(config: Optional[Mapping[str, Any]]) -> int:
    """Return the configured required-input confidence penalty."""

    if not config:
        return 15

    return int(
        config.get("confidence_penalties", {}).get(
            "missing_required_input",
            15,
        )
    )
