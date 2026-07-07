# Assessment Object Specification

Project Version: Revenue Recovery Assessment Engine 0.1

Assessment Version: 1.0

Date Generated: 2026-07-07

---

## 1. Overview

The Assessment Object is the standardized domain object for one completed business assessment. It exists to prevent downstream modules from recalculating Business Intelligence values after an assessment has already been created.

The object is now the single source of truth for assessment identity, prospect profile data, Business Intelligence scores, category outputs, recommended services, quick wins, and raw source data references.

Current flow:

1. Campaign Orchestrator loads campaign and prospect data.
2. Campaign Orchestrator loads the matching company and competitor profiles.
3. Business Intelligence Engine calculates the structured assessment values once.
4. `Assessment.from_business_intelligence()` converts that output into a standardized `Assessment` object.
5. `CampaignResultsRepository` stores the `Assessment` object.
6. Exporters consume the stored `Assessment` object through its flat projection.

No current downstream consumer recalculates Business Intelligence after the `Assessment` object is created.

---

## 2. Object Hierarchy

```text
Assessment
├── Metadata
│   ├── assessment_id
│   ├── campaign_id
│   ├── prospect_id
│   ├── assessment_date
│   └── assessment_version
├── Prospect
│   ├── company_name
│   ├── industry
│   ├── country
│   ├── state
│   ├── city
│   ├── website
│   ├── google_business_profile
│   ├── facebook
│   ├── email
│   └── phone
├── Business Intelligence
│   ├── business_intelligence_score
│   ├── business_grade
│   ├── revenue_opportunity_score
│   ├── priority_score
│   └── assessment_confidence
├── Executive Summary
│   ├── executive_summary
│   ├── overall_assessment
│   └── business_impact
├── Category Scores
│   ├── google_reputation
│   ├── competitive_position
│   ├── digital_presence
│   ├── communication_readiness
│   └── automation_readiness
├── Strengths
├── Weaknesses
├── Quick Wins
├── Recommended Services
└── Raw Data
    ├── company_profile
    └── competitor_profile
```

---

## 3. Field Inventory

### Assessment

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| metadata | AssessmentMetadata | Identity and version fields. | Yes | Implemented |
| prospect | ProspectProfile | Prospect identity and contact profile. | Yes | Implemented |
| business_intelligence | BusinessIntelligenceSnapshot | Final BI scores copied from the BI Engine output. | Yes | Implemented |
| category_scores | CategoryScores | Standardized category assessments. | Yes | Implemented |
| executive_summary | ExecutiveSummary | Narrative summary fields for downstream reports. | Yes | Placeholder |
| strengths | List[str] | Consolidated strengths from BI Engine output. | Yes | Calculated |
| weaknesses | List[str] | Consolidated weaknesses from BI Engine output. | Yes | Calculated |
| quick_wins | List[str] | Practical immediate actions from BI Engine output. | Yes | Calculated |
| recommended_services | List[RecommendedService] | Service recommendations mapped from BI opportunities. | Yes | Implemented |
| raw_data | RawAssessmentData | Original company and competitor source data. | Yes | Implemented |

### Metadata

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| assessment_id | str | Unique assessment identifier composed from campaign and prospect IDs. | Yes | Implemented |
| campaign_id | str | Campaign identifier from campaign configuration. | Yes | Implemented |
| prospect_id | str | Prospect identifier from mock prospect data. | Yes | Implemented |
| assessment_date | str | ISO date when the assessment object was created. | Yes | Implemented |
| assessment_version | str | Assessment model version. Current default is `1.0`. | Yes | Implemented |

### Prospect

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| company_name | str | Business name. | Yes | Implemented |
| industry | str | Campaign industry value. | Yes | Implemented |
| country | str | Prospect or campaign country. | Yes | Implemented |
| state | str | Prospect or company state. | Yes | Implemented |
| city | str | Prospect or company city. | Yes | Implemented |
| website | str | Prospect or company website URL. | No | Implemented |
| google_business_profile | str | Google Business Profile reference. | No | Placeholder |
| facebook | str | Facebook profile URL. | No | Implemented |
| email | str | Prospect email address. | No | Implemented |
| phone | str | Prospect phone number. | No | Implemented |

### Business Intelligence

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| business_intelligence_score | int | Overall business health score from BI Engine. | Yes | Calculated |
| business_grade | str | Grade derived from Business Intelligence Score. | Yes | Calculated |
| revenue_opportunity_score | int | Separate opportunity score from BI Engine. | Yes | Calculated |
| priority_score | int | Internal outreach priority score from BI Engine. | Yes | Calculated |
| assessment_confidence | int | Data-quality confidence from BI Engine. | Yes | Calculated |

### Category Scores

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| google_reputation | CategoryAssessment | Google rating and review category output. | Yes | Calculated |
| competitive_position | CategoryAssessment | Competitor comparison category output. | Yes | Calculated |
| digital_presence | CategoryAssessment | Website and Facebook category output. | Yes | Calculated |
| communication_readiness | CategoryAssessment | Communication readiness category. | Yes | Placeholder |
| automation_readiness | CategoryAssessment | Automation and operational readiness output. | Yes | Calculated |

### Executive Summary

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| executive_summary | str | Customer-facing executive summary narrative. | No | Placeholder |
| overall_assessment | str | Human-readable overall assessment. | No | Placeholder |
| business_impact | str | Narrative description of likely business impact. | No | Placeholder |

### Top-Level Lists

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| strengths | List[str] | Consolidated positive findings. | Yes | Calculated |
| weaknesses | List[str] | Consolidated confirmed gaps or risks. | Yes | Calculated |
| quick_wins | List[str] | Practical immediate improvements. | Yes | Calculated |

### Raw Data

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| company_profile | Dict[str, Any] | Original company profile data used by the assessment. | Yes | Implemented |
| competitor_profile | List[Dict[str, Any]] | Original competitor profile data used by the assessment. | Yes | Implemented |

---

## 4. Category Assessment Structure

`CategoryAssessment` is the reusable model for every category inside `CategoryScores`.

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| score | Optional[int] | Category score, 0-100 where higher is healthier. | No | Calculated |
| confidence | Optional[int] | Category data-quality confidence. | No | Calculated |
| evidence | List[str] | Supporting evidence for the category result. Currently populated from missing input references. | No | Placeholder |
| explanation | str | Human-readable score explanation from category output. | Yes | Calculated |
| strengths | List[str] | Category-level strengths. | No | Calculated |
| weaknesses | List[str] | Category-level weaknesses. | No | Calculated |
| recommended_improvements | List[str] | Practical category-level improvements. | No | Calculated |
| revenue_opportunities | List[Dict[str, Any]] | Category-level revenue opportunities. | No | Calculated |
| service_opportunities | List[str] | Category-level service opportunity keys. | No | Calculated |

Current instantiated categories:

- `google_reputation`
- `competitive_position`
- `digital_presence`
- `communication_readiness`
- `automation_readiness`

`communication_readiness` is currently a placeholder because no Communication Readiness scorer exists yet.

---

## 5. Recommended Service Structure

`RecommendedService` standardizes service recommendations for downstream consumers.

| Field Name | Type | Description | Required | Current Status |
| --- | --- | --- | --- | --- |
| service_name | str | Name of the recommended service. | Yes | Implemented |
| reason | str | Revenue opportunity or business reason for the service. | Yes | Implemented |
| estimated_business_impact | str | HIGH, MEDIUM, or LOW impact label. | Yes | Implemented |
| estimated_revenue_improvement | Any | Revenue improvement estimate where available. | No | Implemented |
| implementation_difficulty | str | LOW, MEDIUM, or HIGH difficulty label. | Yes | Implemented |
| estimated_time_to_implement | str | Business-readable implementation time range. | Yes | Implemented |

Source mapping:

- Created from Business Intelligence Engine `recommended_services`.
- Converted by `_recommended_service_from_output()` in `src/models/assessment.py`.
- No service recommendation is recalculated by the Assessment model.

---

## 6. Business Intelligence

### Calculated Fields

The following fields are calculated by the Business Intelligence Engine in `src/modules/business_intelligence/engine.py`:

- `business_intelligence_score`
- `business_grade`
- `revenue_opportunity_score`
- `priority_score`
- `assessment_confidence`
- `category_scores`
- `strengths`
- `weaknesses`
- `recommended_improvements`
- `revenue_opportunities`
- `service_opportunities`
- `recommended_services`
- `quick_wins`
- `missing_inputs`

### Calculation Modules

The Business Intelligence Engine orchestrates category scorers in:

- `src/modules/business_intelligence/categories/google_reputation.py`
- `src/modules/business_intelligence/categories/competitive_position.py`
- `src/modules/business_intelligence/categories/digital_presence.py`
- `src/modules/business_intelligence/categories/automation_readiness.py`
- `src/modules/business_intelligence/categories/revenue_opportunity.py`

Service recommendations are mapped in:

- `src/modules/business_intelligence/service_mapper.py`

Configuration lives in:

- `src/modules/business_intelligence/config.py`

### Current Consumers

Current consumers of calculated BI fields are:

- `src/models/assessment.py`: copies calculated output into the Assessment object.
- `src/repositories/campaign_results_repository.py`: summarizes stored Assessment objects through `to_flat_dict()`.
- `src/exporters/campaign_exporter.py`: exports stored Assessment objects through `to_flat_dict()`.
- `src/campaign_orchestrator.py`: creates the Assessment object after running BI.
- Existing non-campaign report flow still consumes raw BI dictionary output through `src/modules/executive_summary.py` and `src/generate_report.py`.

### Recalculation Confirmation

Current campaign downstream modules do not recalculate Business Intelligence after the `Assessment` object is created.

- `CampaignResultsRepository` reads values from the stored `Assessment`.
- `Campaign Exporter` reads values from the stored `Assessment`.
- Campaign summary output reads repository statistics derived from the stored `Assessment`.

The older PDF report path still consumes the BI Engine dictionary directly before an `Assessment` object exists. That is outside the current campaign Assessment Object flow and should be migrated later if the Assessment Object is intended to be universal across all report generation.

---

## 7. Current Consumers

### Campaign Orchestrator

File:

- `src/campaign_orchestrator.py`

Responsibilities:

- Loads campaign, prospect, company, and competitor data.
- Runs Business Intelligence once.
- Creates one `Assessment` object per successful prospect using `Assessment.from_business_intelligence()`.
- Stores the `Assessment` in `CampaignResultsRepository`.

### Campaign Results Repository

File:

- `src/repositories/campaign_results_repository.py`

Responsibilities:

- Stores `Assessment` objects in memory.
- Retrieves all assessments.
- Retrieves one assessment by Prospect ID.
- Produces campaign statistics from Assessment object flat projections.

### Campaign Exporter

File:

- `src/exporters/campaign_exporter.py`

Responsibilities:

- Reads all `Assessment` objects from `CampaignResultsRepository`.
- Uses `Assessment.to_flat_dict()` to produce prospect list rows.
- Exports CSV, XLSX, and PDF prospect lists.

---

## 8. Future Consumers

Planned future consumers should consume `Assessment` directly:

- Assessment PDF Generator
- Email Generator
- Google Sheets
- Dashboard
- Supabase
- CRM
- REST API
- Business Intelligence & Growth Platform

Future consumers should not call Business Intelligence scoring modules directly when an `Assessment` object already exists.

---

## 9. Empty / Placeholder Fields

| Field | Location | Current Reason | Expected Future Populator |
| --- | --- | --- | --- |
| google_business_profile | ProspectProfile | Current mock and company data do not include a Google Business Profile URL/reference. | Google profile discovery/import module |
| communication_readiness | CategoryScores | No Communication Readiness scorer exists yet. | Future Communication Readiness module |
| evidence | CategoryAssessment | Currently stores missing input references, not true evidence artifacts. | Category scorers or evidence collection service |
| executive_summary | ExecutiveSummary | Assessment model reserves the field but does not yet receive narrative output. | Executive Summary generator |
| overall_assessment | ExecutiveSummary | Assessment model reserves the field but does not yet receive narrative output. | Executive Summary generator |
| business_impact | ExecutiveSummary | Assessment model reserves the field but does not yet receive narrative output. | Executive Summary generator |

---

## 10. Architectural Recommendations

### Strengths

- The Assessment Object is composed from small dataclasses rather than one large monolithic structure.
- Campaign downstream modules now consume stored Assessment objects instead of raw BI dictionaries.
- Business Intelligence calculations remain centralized in the Business Intelligence Engine.
- `to_dict()` and `to_json()` make the object serializable for future persistence and APIs.
- `to_flat_dict()` preserves compatibility for current summaries and exports.

### Weaknesses

- `executive_summary`, `overall_assessment`, and `business_impact` are placeholders, so narrative consumers cannot rely on them yet.
- `communication_readiness` is a placeholder category, while Communication Readiness also appears as a flat exporter column.
- `evidence` currently maps from `missing_inputs`, which is useful but not true supporting evidence.
- Existing non-campaign report generation still consumes raw Business Intelligence dictionary output rather than the standardized Assessment Object.
- Repository architecture documentation specifies lowercase `docs/architecture`, and the repository has been standardized to that path.

### Unnecessary Duplication

- The Assessment object exposes nested structured data and a flat projection. This is acceptable for compatibility, but future exporters should prefer a shared projection layer if more flat formats are added.
- Business Intelligence values exist both inside `business_intelligence` and in `to_flat_dict()`. This is not recalculation, but it is a projection duplication that should remain controlled.

### Suggested Improvements

- Add a real Communication Readiness category scorer before additional communication-related exports are expanded.
- Populate `ExecutiveSummary` from a dedicated narrative generator after the Assessment object is created.
- Add true evidence fields from source observations, not only missing input labels.
- Migrate the Assessment PDF Generator to consume `Assessment` instead of raw BI dictionaries.
- Standardize architecture document paths to lowercase `docs/architecture` in a dedicated repository cleanup task.

---

## Validation Results

Commands run:

```bash
python3 -m compileall src
python3 src/campaign_orchestrator.py
```

Results:

- No import errors.
- No runtime errors.
- One `Assessment` object is created for every successfully processed prospect.
- `CampaignResultsRepository` stores `Assessment` objects.
- Existing campaign behavior completed successfully.

---

## Field Counts

- Implemented fields: 32
- Calculated fields: 20
- Placeholder fields: 6
- Reserved for future fields: 0
