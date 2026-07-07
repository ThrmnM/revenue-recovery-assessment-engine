"""Standardized assessment object for business assessments."""

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


ASSESSMENT_VERSION = "1.0"


@dataclass
class AssessmentMetadata:
    """Identity fields for an assessment."""

    assessment_id: str
    campaign_id: str
    prospect_id: str
    assessment_date: str
    assessment_version: str = ASSESSMENT_VERSION


@dataclass
class ProspectProfile:
    """Prospect identity and contact fields."""

    company_name: str
    industry: str
    country: str
    state: str
    city: str
    website: str
    google_business_profile: str
    facebook: str
    email: str
    phone: str


@dataclass
class BusinessIntelligenceSnapshot:
    """Business Intelligence scores copied from the engine output."""

    business_intelligence_score: int
    business_grade: str
    revenue_opportunity_score: int
    priority_score: int
    assessment_confidence: int


@dataclass
class CategoryAssessment:
    """Standard category assessment section."""

    score: Optional[int]
    confidence: Optional[int]
    evidence: List[str] = field(default_factory=list)
    explanation: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommended_improvements: List[str] = field(default_factory=list)
    revenue_opportunities: List[Dict[str, Any]] = field(default_factory=list)
    service_opportunities: List[str] = field(default_factory=list)


@dataclass
class CategoryScores:
    """All standardized category assessments."""

    google_reputation: CategoryAssessment
    competitive_position: CategoryAssessment
    digital_presence: CategoryAssessment
    communication_readiness: CategoryAssessment
    automation_readiness: CategoryAssessment


@dataclass
class ExecutiveSummary:
    """Narrative summary fields for downstream report consumers."""

    executive_summary: str
    overall_assessment: str
    business_impact: str


@dataclass
class RecommendedService:
    """Recommended service details for downstream consumers."""

    service_name: str
    reason: str
    estimated_business_impact: str
    estimated_revenue_improvement: Any
    implementation_difficulty: str
    estimated_time_to_implement: str


@dataclass
class RawAssessmentData:
    """Source data used to create the assessment."""

    company_profile: Dict[str, Any]
    competitor_profile: List[Dict[str, Any]]


@dataclass
class Assessment:
    """Single source of truth for one business assessment."""

    metadata: AssessmentMetadata
    prospect: ProspectProfile
    business_intelligence: BusinessIntelligenceSnapshot
    category_scores: CategoryScores
    executive_summary: ExecutiveSummary
    strengths: List[str]
    weaknesses: List[str]
    quick_wins: List[str]
    recommended_services: List[RecommendedService]
    raw_data: RawAssessmentData

    @classmethod
    def from_business_intelligence(
        cls,
        campaign_id: str,
        prospect: Mapping[str, Any],
        company_profile: Mapping[str, Any],
        competitor_profile: Sequence[Mapping[str, Any]],
        business_intelligence: Mapping[str, Any],
        industry: str,
        country: str,
        assessment_date: str,
    ) -> "Assessment":
        """Create an Assessment from existing Business Intelligence output."""

        prospect_id = str(prospect.get("prospect_id", ""))
        assessment_id = f"{campaign_id}-{prospect_id}"
        category_outputs = business_intelligence.get("category_scores", {})

        return cls(
            metadata=AssessmentMetadata(
                assessment_id=assessment_id,
                campaign_id=campaign_id,
                prospect_id=prospect_id,
                assessment_date=assessment_date,
            ),
            prospect=ProspectProfile(
                company_name=str(
                    company_profile.get(
                        "company_name",
                        prospect.get("company_name", ""),
                    )
                ),
                industry=industry,
                country=str(prospect.get("country", country)),
                state=str(
                    prospect.get("state", company_profile.get("state", ""))
                ),
                city=str(
                    prospect.get("city", company_profile.get("city", ""))
                ),
                website=str(
                    prospect.get("website", company_profile.get("website", ""))
                ),
                google_business_profile=str(
                    prospect.get(
                        "google_business_profile",
                        company_profile.get("google_business_profile", ""),
                    )
                ),
                facebook=str(
                    prospect.get(
                        "facebook_url",
                        company_profile.get("facebook_url", ""),
                    )
                ),
                email=str(prospect.get("email", company_profile.get("email", ""))),
                phone=str(prospect.get("phone", company_profile.get("phone", ""))),
            ),
            business_intelligence=BusinessIntelligenceSnapshot(
                business_intelligence_score=int(
                    business_intelligence["business_intelligence_score"]
                ),
                business_grade=str(business_intelligence["business_grade"]),
                revenue_opportunity_score=int(
                    business_intelligence["revenue_opportunity_score"]
                ),
                priority_score=int(business_intelligence["priority_score"]),
                assessment_confidence=int(
                    business_intelligence["assessment_confidence"]
                ),
            ),
            category_scores=CategoryScores(
                google_reputation=_category_from_output(
                    category_outputs.get("google_reputation")
                ),
                competitive_position=_category_from_output(
                    category_outputs.get("competitive_position")
                ),
                digital_presence=_category_from_output(
                    category_outputs.get("digital_presence")
                ),
                communication_readiness=_communication_readiness_category(),
                automation_readiness=_category_from_output(
                    category_outputs.get("automation_readiness")
                ),
            ),
            executive_summary=ExecutiveSummary(
                executive_summary="",
                overall_assessment="",
                business_impact="",
            ),
            strengths=list(business_intelligence.get("strengths", [])),
            weaknesses=list(business_intelligence.get("weaknesses", [])),
            quick_wins=list(business_intelligence.get("quick_wins", [])),
            recommended_services=[
                _recommended_service_from_output(service)
                for service in business_intelligence.get(
                    "recommended_services",
                    [],
                )
            ],
            raw_data=RawAssessmentData(
                company_profile={
                    key: value
                    for key, value in dict(company_profile).items()
                    if not str(key).startswith("_")
                },
                competitor_profile=[
                    dict(competitor)
                    for competitor in competitor_profile
                ],
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""

        return asdict(self)

    def to_json(self) -> str:
        """Return a JSON string representation."""

        return json.dumps(self.to_dict(), indent=2)

    def to_flat_dict(self) -> Dict[str, Any]:
        """Return backward-compatible flat fields for exporters and summaries."""

        return {
            "assessment_id": self.metadata.assessment_id,
            "campaign_id": self.metadata.campaign_id,
            "prospect_id": self.metadata.prospect_id,
            "assessment_date": self.metadata.assessment_date,
            "assessment_version": self.metadata.assessment_version,
            "company_name": self.prospect.company_name,
            "industry": self.prospect.industry,
            "country": self.prospect.country,
            "state": self.prospect.state,
            "city": self.prospect.city,
            "website": self.prospect.website,
            "google_business_profile":
                self.prospect.google_business_profile,
            "facebook": self.prospect.facebook,
            "email": self.prospect.email,
            "phone": self.prospect.phone,
            "business_intelligence_score":
                self.business_intelligence.business_intelligence_score,
            "business_grade": self.business_intelligence.business_grade,
            "revenue_opportunity_score":
                self.business_intelligence.revenue_opportunity_score,
            "priority_score": self.business_intelligence.priority_score,
            "assessment_confidence":
                self.business_intelligence.assessment_confidence,
            "communication_readiness": "Pending",
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
            "quick_wins": list(self.quick_wins),
            "recommended_services": [
                asdict(service)
                for service in self.recommended_services
            ],
        }


def _category_from_output(output: Optional[Mapping[str, Any]]) -> CategoryAssessment:
    """Create a CategoryAssessment from engine category output."""

    if not output:
        return CategoryAssessment(
            score=None,
            confidence=None,
            explanation="Category was not calculated.",
        )

    return CategoryAssessment(
        score=output.get("score"),
        confidence=output.get("confidence"),
        evidence=list(output.get("missing_inputs", [])),
        explanation=str(output.get("explanation", "")),
        strengths=list(output.get("strengths", [])),
        weaknesses=list(output.get("weaknesses", [])),
        recommended_improvements=list(
            output.get("recommended_improvements", [])
        ),
        revenue_opportunities=[
            dict(opportunity)
            for opportunity in output.get("revenue_opportunities", [])
        ],
        service_opportunities=list(output.get("service_opportunities", [])),
    )


def _communication_readiness_category() -> CategoryAssessment:
    """Return placeholder category object until communication scoring exists."""

    return CategoryAssessment(
        score=None,
        confidence=None,
        evidence=[],
        explanation="Communication readiness has not been calculated.",
        strengths=[],
        weaknesses=[],
        recommended_improvements=[],
        revenue_opportunities=[],
        service_opportunities=[],
    )


def _recommended_service_from_output(
    service: Mapping[str, Any],
) -> RecommendedService:
    """Create a RecommendedService from engine service output."""

    return RecommendedService(
        service_name=str(service.get("service", "")),
        reason=str(service.get("revenue_opportunity", "")),
        estimated_business_impact=str(
            service.get("estimated_business_impact", "")
        ),
        estimated_revenue_improvement=service.get(
            "estimated_revenue_improvement",
            "",
        ),
        implementation_difficulty=str(
            service.get("implementation_difficulty", "")
        ),
        estimated_time_to_implement=str(
            service.get("estimated_implementation_time", "")
        ),
    )
