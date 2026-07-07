"""Automation readiness scoring."""

from typing import Any, Dict, Mapping, Optional, Sequence

from modules.business_intelligence.category_output import (
    clamp_score,
    make_category_output,
)


def score_automation_readiness(
    company: Mapping[str, Any],
    competitors: Optional[Sequence[Mapping[str, Any]]] = None,
    assessment: Optional[Mapping[str, Any]] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Score business automation readiness."""

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

    automation_score = company.get("automation_score")

    if automation_score is not None:
        score = int(automation_score)
        explanation_parts.append(
            f"Automation score was provided directly as {score}/100."
        )

        if score >= 80:
            strengths.append("Good Automation")
        elif score < 50:
            weaknesses.append("Automation maturity is low.")
            improvements.append("Install core lead capture and follow-up automation.")
            revenue_opportunities.append({
                "condition": "low_automation",
                "opportunity": "Recover missed leads and improve follow-up consistency.",
            })
            service_opportunities.append("low_automation")

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

    operational_fields = [
        "missed_calls",
        "quote_delay",
        "poor_communication",
        "late_technicians",
    ]
    has_operational_data = any(field in company for field in operational_fields)

    if not has_operational_data:
        confidence -= confidence_penalty
        missing_inputs.append("Automation Score")
        explanation_parts.append(
            "Automation data was unavailable, so no automation penalty was applied."
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

    if company.get("missed_calls"):
        score -= 25
        weaknesses.append("Missed inbound calls are present.")
        improvements.append("Install AI Receptionist or missed-call text back.")
        revenue_opportunities.append({
            "condition": "missed_calls",
            "opportunity": "Capture leads that would otherwise be lost.",
            "estimated_revenue_improvement": 35000,
        })
        service_opportunities.append("missed_calls")
        explanation_parts.append("Missed calls reduce automation readiness by 25.")

    if company.get("quote_delay"):
        score -= 25
        weaknesses.append("Quote delays are present.")
        improvements.append("Automate quote follow-up and reminders.")
        revenue_opportunities.append({
            "condition": "quote_delay",
            "opportunity": "Increase quote conversion and reduce lead leakage.",
            "estimated_revenue_improvement": 30000,
        })
        service_opportunities.append("quote_delay")
        explanation_parts.append("Quote delays reduce automation readiness by 25.")

    if company.get("poor_communication"):
        score -= 20
        weaknesses.append("Customer communication is inconsistent.")
        improvements.append("Automate customer communication touchpoints.")
        revenue_opportunities.append({
            "condition": "low_automation",
            "opportunity": "Improve response consistency and customer experience.",
            "estimated_revenue_improvement": 25000,
        })
        service_opportunities.append("low_automation")
        explanation_parts.append(
            "Poor communication reduces automation readiness by 20."
        )

    if company.get("late_technicians"):
        score -= 10
        weaknesses.append("Technician timing issues are present.")
        improvements.append("Use scheduling and ETA notifications.")
        revenue_opportunities.append({
            "condition": "low_automation",
            "opportunity": "Improve customer experience with scheduling automation.",
            "estimated_revenue_improvement": 20000,
        })
        service_opportunities.append("low_automation")
        explanation_parts.append(
            "Technician timing issues reduce automation readiness by 10."
        )

    if score == 100:
        strengths.append("Good Automation")
        explanation_parts.append(
            "No confirmed operational automation gaps were found."
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
