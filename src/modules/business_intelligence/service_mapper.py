"""Map revenue opportunities to recommended services."""

from typing import Any, Dict, Iterable, List, Mapping, Tuple


def map_recommended_services(
    category_outputs: Mapping[str, Mapping[str, Any]],
    config: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Return recommended services from category revenue opportunities."""

    mappings = config.get("service_opportunity_mappings", {})
    defaults = config.get("recommended_service_defaults", {})
    services: List[Dict[str, Any]] = []
    seen: set[Tuple[str, str]] = set()

    for category_name, output in category_outputs.items():
        for opportunity in output.get("revenue_opportunities", []):
            condition = _condition(opportunity)

            if not condition or condition not in mappings:
                continue

            mapping = mappings[condition]
            service_name = mapping["service"]
            key = (condition, service_name)

            if key in seen:
                continue

            seen.add(key)
            services.append({
                "service": service_name,
                "source_category": category_name,
                "source_condition": condition,
                "revenue_opportunity": _opportunity_text(opportunity),
                "estimated_business_impact":
                    mapping.get("estimated_business_impact", "MEDIUM"),
                "estimated_revenue_improvement":
                    _estimated_revenue(opportunity, defaults),
                "implementation_difficulty":
                    mapping.get("implementation_difficulty", "MEDIUM"),
                "estimated_implementation_time":
                    mapping.get("estimated_implementation_time", "Unavailable"),
            })

    return services


def collect_service_opportunities(
    recommended_services: Iterable[Mapping[str, Any]],
) -> List[str]:
    """Return unique service names from recommended service records."""

    services = []

    for service in recommended_services:
        name = service.get("service")

        if name and name not in services:
            services.append(name)

    return services


def _condition(opportunity: Any) -> str:
    """Return the condition identifier for an opportunity."""

    if isinstance(opportunity, Mapping):
        return str(opportunity.get("condition", "")).strip()

    return ""


def _opportunity_text(opportunity: Any) -> str:
    """Return display text for a revenue opportunity."""

    if isinstance(opportunity, Mapping):
        return str(opportunity.get("opportunity", "")).strip()

    return str(opportunity).strip()


def _estimated_revenue(
    opportunity: Any,
    defaults: Mapping[str, Any],
) -> Any:
    """Return opportunity-level revenue estimate when available."""

    if isinstance(opportunity, Mapping):
        value = opportunity.get("estimated_revenue_improvement")

        if value is not None:
            return value

    return defaults.get("estimated_revenue_improvement", "Unavailable")
