"""Google reputation scoring."""

from typing import Any, Dict, Mapping, Optional, Sequence

from modules.business_intelligence.category_output import (
    clamp_score,
    make_category_output,
)


def score_google_reputation(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Score Google reputation from rating and review count."""

    del competitors, assessment

    confidence_penalty = _penalty(config)
    score = 100
    confidence = 100
    strengths = []
    weaknesses = []
    improvements = []
    revenue_opportunities = []
    service_opportunities = []
    missing_inputs = []
    explanation_parts = []

    rating = company.get("rating")
    review_count = company.get("review_count")

    if rating is None:
        confidence -= confidence_penalty
        missing_inputs.append("Google Rating")
        explanation_parts.append(
            "Google rating was unavailable, so no rating penalty was applied."
        )
    else:
        rating = float(rating)

        if rating >= 4.7:
            strengths.append("Excellent Google Rating")
            explanation_parts.append(
                f"Google rating is strong at {rating:.1f}."
            )
        elif rating >= 4.2:
            score -= 10
            weaknesses.append("Google rating has room to improve.")
            improvements.append("Request reviews from satisfied customers.")
            revenue_opportunities.append({
                "condition": "poor_reviews",
                "opportunity": "Increase trust and conversion from local search.",
            })
            service_opportunities.append("poor_reviews")
            explanation_parts.append(
                f"Google rating is moderate at {rating:.1f}, reducing score by 10."
            )
        else:
            score -= 25
            weaknesses.append("Google rating is below the preferred trust range.")
            improvements.append("Launch a structured Google review growth process.")
            revenue_opportunities.append({
                "condition": "poor_reviews",
                "opportunity": "Increase conversion by improving visible customer trust.",
            })
            service_opportunities.append("poor_reviews")
            explanation_parts.append(
                f"Google rating is weak at {rating:.1f}, reducing score by 25."
            )

    if review_count is None:
        confidence -= confidence_penalty
        missing_inputs.append("Google Review Count")
        explanation_parts.append(
            "Google review count was unavailable, so no review-volume penalty was applied."
        )
    else:
        review_count = int(review_count)

        if review_count >= 100:
            strengths.append("Strong Customer Reviews")
            explanation_parts.append(
                f"Google review volume is healthy at {review_count} reviews."
            )
        elif review_count >= 51:
            score -= 10
            weaknesses.append("Google review count trails stronger local competitors.")
            improvements.append("Ask every completed job for a Google review.")
            revenue_opportunities.append({
                "condition": "low_review_count",
                "opportunity": "Build social proof to improve search-to-call conversion.",
            })
            service_opportunities.append("low_review_count")
            explanation_parts.append(
                f"Google review count is {review_count}, reducing score by 10."
            )
        elif review_count >= 25:
            score -= 20
            weaknesses.append("Google review count is low for a competitive service market.")
            improvements.append("Begin requesting Google Reviews after every completed project.")
            revenue_opportunities.append({
                "condition": "low_review_count",
                "opportunity": "Increase local credibility and quote requests.",
            })
            service_opportunities.append("low_review_count")
            explanation_parts.append(
                f"Google review count is {review_count}, reducing score by 20."
            )
        else:
            score -= 30
            weaknesses.append("Google review count is critically low.")
            improvements.append("Create a repeatable review request workflow.")
            revenue_opportunities.append({
                "condition": "low_review_count",
                "opportunity": "Improve customer trust before prospects choose competitors.",
            })
            service_opportunities.append("low_review_count")
            explanation_parts.append(
                f"Google review count is {review_count}, reducing score by 30."
            )

    if not explanation_parts:
        explanation_parts.append(
            "Google reputation showed no confirmed negative signals."
        )

    return make_category_output(
        score=clamp_score(score),
        confidence=confidence,
        explanation=" ".join(explanation_parts),
        strengths=strengths,
        weaknesses=weaknesses,
        recommended_improvements=improvements,
        revenue_opportunities=revenue_opportunities,
        service_opportunities=service_opportunities,
        missing_inputs=missing_inputs,
    )


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
