"""Digital presence scoring."""

from typing import Any, Dict, Mapping, Optional, Sequence

from modules.business_intelligence.category_output import (
    clamp_score,
    make_category_output,
)


def score_digital_presence(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Score website and Facebook presence."""

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

    website_exists = _get_value(company, "website_exists", "has_website")

    if website_exists is None:
        confidence -= confidence_penalty
        missing_inputs.append("Website Exists")
        explanation_parts.append(
            "Website status was unavailable, so no website penalty was applied."
        )
    elif website_exists:
        strengths.append("Professional Website")
        explanation_parts.append("A website is confirmed.")
        score = _score_website_details(
            company,
            score,
            strengths,
            weaknesses,
            improvements,
            revenue_opportunities,
            service_opportunities,
            explanation_parts,
            missing_inputs,
            confidence_penalty,
        )
        confidence = _confidence_after_website_details(
            company,
            confidence,
            confidence_penalty,
            missing_inputs,
        )
    else:
        score -= 35
        weaknesses.append("No website is confirmed.")
        improvements.append("Create a professional website with quote-request paths.")
        revenue_opportunities.append({
            "condition": "no_website",
            "opportunity": "Capture search traffic and convert visitors into quote requests.",
        })
        service_opportunities.append("no_website")
        explanation_parts.append(
            "No website is confirmed, reducing score by 35."
        )

    facebook_page = _get_value(
        company,
        "facebook_business_page",
        "facebook_page_exists",
    )

    if facebook_page is None:
        confidence -= confidence_penalty
        missing_inputs.append("Facebook Business Page")
        explanation_parts.append(
            "Facebook page status was unavailable, so no Facebook penalty was applied."
        )
    elif facebook_page:
        strengths.append("Facebook Business Page")
        explanation_parts.append("A Facebook business page is confirmed.")
        active = _get_value(
            company,
            "facebook_active_within_90_days",
            "facebook_active_90_days",
        )

        if active is None:
            confidence -= confidence_penalty
            missing_inputs.append("Facebook Active Within 90 Days")
            explanation_parts.append(
                "Facebook activity was unavailable, so no activity penalty was applied."
            )
        elif active:
            strengths.append("Recent Facebook Activity")
            explanation_parts.append("Facebook activity is recent.")
        else:
            score -= 15
            weaknesses.append("Facebook page is inactive.")
            improvements.append("Post one completed project every week.")
            revenue_opportunities.append({
                "condition": "inactive_facebook",
                "opportunity": "Improve visibility and trust with recent project activity.",
            })
            service_opportunities.append("inactive_facebook")
            explanation_parts.append(
                "Facebook page is inactive, reducing score by 15."
            )
    else:
        score -= 10
        weaknesses.append("No Facebook business page is confirmed.")
        improvements.append("Create or claim a Facebook business page.")
        revenue_opportunities.append({
            "condition": "inactive_facebook",
            "opportunity": "Improve local visibility and customer trust.",
        })
        service_opportunities.append("inactive_facebook")
        explanation_parts.append(
            "No Facebook business page is confirmed, reducing score by 10."
        )

    if not explanation_parts:
        explanation_parts.append(
            "Digital presence showed no confirmed negative signals."
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


def _score_website_details(
    company: Mapping[str, Any],
    score: int,
    strengths: list,
    weaknesses: list,
    improvements: list,
    revenue_opportunities: list,
    service_opportunities: list,
    explanation_parts: list,
    missing_inputs: list,
    confidence_penalty: int,
) -> int:
    """Apply confirmed website detail scoring."""

    del missing_inputs, confidence_penalty

    detail_checks = [
        (
            ("website_https", "https_enabled"),
            "HTTPS Enabled",
            "Website has HTTPS enabled.",
            "Website does not use HTTPS.",
            "Enable HTTPS for trust and browser compatibility.",
            10,
        ),
        (
            ("website_mobile_friendly", "mobile_friendly"),
            "Mobile-Friendly Website",
            "Website is mobile friendly.",
            "Website is not mobile friendly.",
            "Improve the mobile website experience.",
            10,
        ),
        (
            ("website_contact_form", "contact_form"),
            "Online Quote Form",
            "Website includes a contact or quote form.",
            "Website is missing a contact or quote form.",
            "Add an Online Quote Form.",
            15,
        ),
    ]

    for keys, strength, positive, weakness, improvement, deduction in detail_checks:
        value = _get_value(company, *keys)

        if value is None:
            continue

        if value:
            strengths.append(strength)
            explanation_parts.append(positive)
        else:
            score -= deduction
            weaknesses.append(weakness)
            improvements.append(improvement)
            revenue_opportunities.append({
                "condition": "outdated_or_weak_website",
                "opportunity": "Improve website trust and quote-request conversion.",
            })
            service_opportunities.append("outdated_or_weak_website")
            explanation_parts.append(
                f"{weakness} This reduces score by {deduction}."
            )

    return score


def _confidence_after_website_details(
    company: Mapping[str, Any],
    confidence: int,
    confidence_penalty: int,
    missing_inputs: list,
) -> int:
    """Reduce confidence for unavailable confirmed-website details."""

    fields = [
        ("website_https", "https_enabled", "HTTPS Enabled"),
        ("website_mobile_friendly", "mobile_friendly", "Mobile Friendly"),
        ("website_contact_form", "contact_form", "Contact Form"),
    ]

    for first_key, second_key, label in fields:
        if _get_value(company, first_key, second_key) is None:
            missing_inputs.append(label)
            confidence -= confidence_penalty

    return confidence


def _get_value(company: Mapping[str, Any], *keys: str) -> Any:
    """Return the first present value for the supplied keys."""

    for key in keys:
        if key in company:
            return company.get(key)

    return None


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
