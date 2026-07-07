"""Competitive position scoring."""

from typing import Any, Dict, Mapping, Optional, Sequence

from modules.business_intelligence.category_output import (
    clamp_score,
    make_category_output,
)


def score_competitive_position(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Score competitive position against local competitors."""

    del assessment

    confidence_penalty = _penalty(config)
    competitor_list = list(competitors or [])
    score = 100
    confidence = 100
    strengths = []
    weaknesses = []
    improvements = []
    revenue_opportunities = []
    service_opportunities = []
    missing_inputs = []
    explanation_parts = []

    company_rating = company.get("rating")
    company_reviews = company.get("review_count")

    if not competitor_list:
        confidence -= confidence_penalty
        missing_inputs.append("Competitor Data")
        explanation_parts.append(
            "Competitor data was unavailable, so no competitive penalty was applied."
        )

        return make_category_output(
            score=score,
            confidence=confidence,
            explanation=" ".join(explanation_parts),
            strengths=strengths,
            weaknesses=weaknesses,
            recommended_improvements=improvements,
            revenue_opportunities=revenue_opportunities,
            service_opportunities=service_opportunities,
            missing_inputs=missing_inputs,
        )

    if company_rating is None:
        confidence -= confidence_penalty
        missing_inputs.append("Company Google Rating")
    else:
        company_rating = float(company_rating)

    if company_reviews is None:
        confidence -= confidence_penalty
        missing_inputs.append("Company Google Review Count")
    else:
        company_reviews = int(company_reviews)

    competitor_ratings = [
        float(competitor["rating"])
        for competitor in competitor_list
        if competitor.get("rating") is not None
    ]
    competitor_reviews = [
        int(competitor["review_count"])
        for competitor in competitor_list
        if competitor.get("review_count") is not None
    ]

    if not competitor_ratings:
        confidence -= confidence_penalty
        missing_inputs.append("Competitor Google Ratings")
    elif company_rating is not None:
        average_rating = sum(competitor_ratings) / len(competitor_ratings)
        rating_gap = average_rating - company_rating

        if rating_gap <= 0:
            strengths.append("Strong Competitive Rating")
            explanation_parts.append(
                f"Company rating is at or above the competitor average of {average_rating:.1f}."
            )
        elif rating_gap <= 0.3:
            score -= 8
            weaknesses.append("Competitors hold a slight rating advantage.")
            improvements.append("Improve review quality and respond to recent feedback.")
            revenue_opportunities.append({
                "condition": "poor_reviews",
                "opportunity": "Close the rating gap to improve customer trust.",
            })
            service_opportunities.append("poor_reviews")
            explanation_parts.append(
                f"Competitor average rating is {average_rating:.1f}, "
                f"{rating_gap:.1f} higher, reducing score by 8."
            )
        else:
            score -= 15
            weaknesses.append("Competitors hold a meaningful rating advantage.")
            improvements.append("Prioritize reputation recovery and review quality.")
            revenue_opportunities.append({
                "condition": "poor_reviews",
                "opportunity": "Recover leads lost to higher-rated competitors.",
            })
            service_opportunities.append("poor_reviews")
            explanation_parts.append(
                f"Competitor average rating is {average_rating:.1f}, "
                f"{rating_gap:.1f} higher, reducing score by 15."
            )

    if not competitor_reviews:
        confidence -= confidence_penalty
        missing_inputs.append("Competitor Google Review Counts")
    elif company_reviews is not None:
        average_reviews = sum(competitor_reviews) / len(competitor_reviews)
        review_gap = average_reviews - company_reviews
        top_reviews = max(competitor_reviews)

        if review_gap <= 0:
            strengths.append("Strong Competitive Review Volume")
            explanation_parts.append(
                "Company review volume is at or above the competitor average."
            )
        elif review_gap <= 50:
            score -= 10
            weaknesses.append("Competitors have a modest review-volume advantage.")
            improvements.append("Increase review requests after completed work.")
            revenue_opportunities.append({
                "condition": "competitive_review_gap",
                "opportunity": "Improve local search credibility by closing the review gap.",
                "estimated_revenue_improvement": _estimated_review_gap_value(review_gap),
            })
            service_opportunities.append("competitive_review_gap")
            explanation_parts.append(
                f"Competitors average {average_reviews:.0f} reviews, "
                f"{review_gap:.0f} more, reducing score by 10."
            )
        elif review_gap <= 150:
            score -= 20
            weaknesses.append("Competitors have a major review-volume advantage.")
            improvements.append("Launch a structured review growth campaign.")
            revenue_opportunities.append({
                "condition": "competitive_review_gap",
                "opportunity": "Improve search visibility and conversion by closing the review gap.",
                "estimated_revenue_improvement": _estimated_review_gap_value(review_gap),
            })
            service_opportunities.append("competitive_review_gap")
            explanation_parts.append(
                f"Competitors average {average_reviews:.0f} reviews, "
                f"{review_gap:.0f} more, reducing score by 20."
            )
        else:
            score -= 30
            weaknesses.append("Competitors have a severe review-volume advantage.")
            improvements.append("Treat reputation growth as a primary recovery initiative.")
            revenue_opportunities.append({
                "condition": "competitive_review_gap",
                "opportunity": "Recover demand that is likely going to more visible competitors.",
                "estimated_revenue_improvement": _estimated_review_gap_value(review_gap),
            })
            service_opportunities.append("competitive_review_gap")
            explanation_parts.append(
                f"Competitors average {average_reviews:.0f} reviews, "
                f"{review_gap:.0f} more, reducing score by 30."
            )

        if company_reviews >= top_reviews:
            strengths.append("Market-Leading Review Volume")

    if not explanation_parts:
        explanation_parts.append(
            "Competitive position showed no confirmed negative signals."
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


def _estimated_review_gap_value(review_gap: float) -> int:
    """Estimate annual value associated with the competitor review gap."""

    return max(0, int(review_gap * 500))


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
