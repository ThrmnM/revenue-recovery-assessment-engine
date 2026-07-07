"""Configuration for the Business Intelligence Engine."""

from copy import deepcopy
from typing import Any, Dict, Optional


DEFAULT_CONFIG: Dict[str, Any] = {
    "enabled_categories": [
        "google_reputation",
        "competitive_position",
        "digital_presence",
        "automation_readiness",
        "revenue_opportunity",
    ],
    "business_intelligence_weights": {
        "google_reputation": 25,
        "competitive_position": 20,
        "digital_presence": 20,
        "automation_readiness": 15,
    },
    "grade_boundaries": [
        {"grade": "A+", "minimum": 95},
        {"grade": "A", "minimum": 90},
        {"grade": "B", "minimum": 80},
        {"grade": "C", "minimum": 70},
        {"grade": "D", "minimum": 60},
        {"grade": "F", "minimum": 0},
    ],
    "confidence_penalties": {
        "missing_required_input": 15,
        "missing_optional_input": 8,
        "lookup_failed": 25,
    },
    "priority_rules": {
        "business_health_gap_weight": 0.45,
        "revenue_opportunity_weight": 0.45,
        "confidence_gap_weight": 0.10,
    },
    "service_opportunity_mappings": {
        "inactive_facebook": {
            "service": "Monthly Social Media Management",
            "estimated_business_impact": "MEDIUM",
            "implementation_difficulty": "LOW",
            "estimated_implementation_time": "1-3 days",
        },
        "no_website": {
            "service": "Website Design",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "2-4 weeks",
        },
        "outdated_or_weak_website": {
            "service": "Website Refresh",
            "estimated_business_impact": "MEDIUM",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "1-2 weeks",
        },
        "poor_reviews": {
            "service": "Review Growth System",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "LOW",
            "estimated_implementation_time": "1-3 days",
        },
        "low_review_count": {
            "service": "Google Review Campaign",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "LOW",
            "estimated_implementation_time": "1-3 days",
        },
        "low_automation": {
            "service": "Revenue Recovery Installation",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "30-90 days",
        },
        "no_crm": {
            "service": "CRM Implementation",
            "estimated_business_impact": "MEDIUM",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "2-4 weeks",
        },
        "no_booking": {
            "service": "Online Booking System",
            "estimated_business_impact": "MEDIUM",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "1-2 weeks",
        },
        "missed_calls": {
            "service": "AI Receptionist and Missed Call Text Back",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "1-2 weeks",
        },
        "quote_delay": {
            "service": "Automated Quote Follow-Up System",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "1-2 weeks",
        },
        "competitive_review_gap": {
            "service": "Local Reputation Growth Program",
            "estimated_business_impact": "HIGH",
            "implementation_difficulty": "MEDIUM",
            "estimated_implementation_time": "30-90 days",
        },
    },
    "recommended_service_defaults": {
        "estimated_revenue_improvement": "Unavailable",
    },
}


def get_config(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return engine configuration with optional shallow section overrides."""

    config = deepcopy(DEFAULT_CONFIG)

    if not overrides:
        return config

    for key, value in overrides.items():
        if (
            isinstance(value, dict)
            and isinstance(config.get(key), dict)
        ):
            config[key].update(value)
        else:
            config[key] = value

    return config
