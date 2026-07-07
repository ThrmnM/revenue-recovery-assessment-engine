# CAP-01 — Assessment Engine
## MOD-04 — Business Intelligence Engine

---

# Metadata

Status: Frozen for Implementation

Version: 2.0

Owner: Revenue Recovery System

Last Updated: 2026-07-06

---

# Purpose

The Business Intelligence Engine is the master functional engine for evaluating the digital health, revenue opportunity, competitive position, and operational maturity of a local service business.

It produces structured assessment data that powers:

- Executive Summary
- Digital Business Health Assessment
- Competitive Analysis
- Recommendations
- Revenue Recovery Intelligence Report
- National Prospect Ranking Engine
- Weekly Outreach Queue

The engine must produce professional, explainable outputs suitable for a consulting-quality business report.

---

# Core Architecture

The engine must be modular, configuration-driven, and easy to extend.

The engine is responsible for:

- Running enabled assessment categories
- Collecting category outputs
- Calculating the Business Intelligence Score
- Calculating the Revenue Opportunity Score
- Calculating the Priority Score
- Calculating Assessment Confidence
- Producing structured strengths, weaknesses, opportunities, services, and quick wins

The engine must not contain PDF rendering logic.

The engine must not embed service sales logic inside scoring calculations.

The engine must keep scoring, revenue opportunity analysis, priority ranking, and service mapping as separate responsibilities.

---

# Three Independent Scores

The Business Intelligence Engine produces three independent scores:

- Business Intelligence Score
- Revenue Opportunity Score
- Priority Score

These represent three different business concepts and must never be combined.

They must not be substituted for one another.

They must not be averaged into a single master score.

## Business Intelligence Score

The Business Intelligence Score measures the overall health and maturity of the business.

Higher score = healthier business.

This score may be shown to the prospect.

## Revenue Opportunity Score

The Revenue Opportunity Score measures the size and importance of the business improvement opportunity.

Higher score = greater opportunity to recover or create revenue.

This score may be used to support revenue opportunity analysis and recommended services.

## Priority Score

The Priority Score measures internal outreach urgency.

Higher score = higher priority for sales follow-up or outreach.

This score is internal only and must not be shown to prospects.

---

# Primary Outputs

The engine must produce:

- Business Intelligence Score
- Business Grade
- Revenue Opportunity Score
- Priority Score
- Assessment Confidence
- Category Scores
- Strengths
- Weaknesses
- Recommended Improvements
- Revenue Opportunities
- Service Opportunities
- Recommended Services
- Quick Wins
- Missing Inputs

---

# Business Intelligence Score

The Business Intelligence Score is a 0–100 score.

Higher scores represent healthier businesses.

Lower scores represent businesses with more weaknesses, maturity gaps, or improvement needs.

The Business Intelligence Score must be calculated only from enabled business health categories.

Revenue Opportunity Score and Priority Score must not be included in the Business Intelligence Score calculation.

Every Business Intelligence Score must be supported by category-level explanations.

---

# Business Grade Boundaries

Business Grade must be derived from the Business Intelligence Score.

Grade boundaries must be configurable.

Default grade boundaries:

| Grade | Score Range |
| --- | --- |
| A+ | 95–100 |
| A | 90–94 |
| B | 80–89 |
| C | 70–79 |
| D | 60–69 |
| F | 0–59 |

---

# Revenue Opportunity Score

The Revenue Opportunity Score measures the potential business upside associated with identified weaknesses.

It is separate from the Business Intelligence Score.

It may consider:

- Estimated Revenue Leakage
- Review gap
- Rating gap
- Missed-call risk
- Quote-delay risk
- Automation gaps
- Website conversion gaps
- Social media inactivity
- Competitive disadvantage

Weaknesses should identify Revenue Opportunities.

Revenue Opportunities should then map to Service Opportunities and Recommended Services.

The revenue opportunity calculation must remain separate from the service mapping layer.

---

# Priority Score

The Priority Score determines internal outreach order.

It is used by:

- National Prospect Ranking Engine
- Weekly Outreach Queue
- Sales prioritization workflows

Priority Score is internal only.

Priority Score must not be displayed in prospect-facing reports.

Priority Score rules must be configuration-driven.

Priority Score may consider:

- Low Business Intelligence Score
- High Revenue Opportunity Score
- Low Assessment Confidence requiring follow-up
- Strategic market fit
- Severity of confirmed weaknesses

Priority Score must remain separate from Business Intelligence Score and Revenue Opportunity Score.

---

# Assessment Categories

Each assessment category must be independently extendable.

Each category must return the standard Category Output Contract.

Initial assessment categories:

## Google Reputation

Inputs:

- Google Rating
- Google Review Count
- Review quality indicators, where available

## Competitive Position

Inputs:

- Competitor Rating Gap
- Competitor Review Gap
- Market rank
- Top competitor comparison

## Digital Presence

Inputs:

- Website Exists
- HTTPS Enabled
- Mobile Friendly
- Contact Form
- Facebook Business Page
- Facebook Active Within 90 Days

## Automation Readiness

Inputs:

- Automation Score
- Missed-call indicators
- Quote follow-up indicators
- Lead follow-up indicators
- Online booking indicators, where available
- CRM indicators, where available

## Revenue Opportunity

Inputs:

- Estimated Revenue Leakage
- Opportunity Level
- Confirmed revenue leak indicators
- Competitive disadvantage indicators

The Revenue Opportunity category informs Revenue Opportunity Score and opportunity analysis.

It must not be weighted into Business Intelligence Score unless explicitly configured as a health category.

---

# Category Output Contract

Every assessment category must return the same structured object.

Required fields:

- Score
- Confidence
- Explanation
- Strengths
- Weaknesses
- Recommended Improvements
- Revenue Opportunities
- Service Opportunities
- Missing Inputs

## Score

The category score must be a 0–100 score.

Higher score = healthier performance in that category.

## Confidence

The category confidence score must measure data quality only.

## Explanation

Every category score must include a human-readable explanation of why the score was awarded.

No unexplained scores are acceptable.

The explanation must be suitable for a professional consulting document.

## Strengths

Strengths must identify what the business is already doing well.

## Weaknesses

Weaknesses must identify confirmed gaps or risks.

## Recommended Improvements

Recommended Improvements must describe practical business improvements, not just services for sale.

## Revenue Opportunities

Revenue Opportunities must identify the business upside connected to weaknesses.

## Service Opportunities

Service Opportunities must identify potential services that could address the weakness.

Service mapping must remain separate from scoring logic.

## Missing Inputs

Missing Inputs must identify unavailable, incomplete, failed, or unverified data.

Missing Inputs affect confidence, not health score, unless the negative condition has been confirmed.

---

# Assessment Confidence

Assessment Confidence measures data quality only.

Assessment Confidence does not measure business quality.

Assessment Confidence must not reduce the Business Intelligence Score unless the negative condition has been confirmed.

Examples that reduce confidence only:

- Website unavailable
- Facebook unavailable
- Google lookup failed
- Competitor data incomplete
- Revenue estimate unavailable
- Automation data unavailable

Examples of confirmed conditions that may affect score:

- Confirmed no website
- Confirmed inactive Facebook page
- Confirmed poor Google rating
- Confirmed low Google review count
- Confirmed missing contact form
- Confirmed no automation process

Assessment Confidence must be reported as a percentage from 0–100%.

Confidence penalties must be configuration-driven.

---

# Strengths and Positive Reinforcement

Every assessment should identify what the business is already doing well.

The report must acknowledge strengths so the assessment feels fair, balanced, and credible.

Examples:

- Excellent Google Rating
- Strong Customer Reviews
- Professional Website
- Mobile-Friendly Website
- Recent Facebook Activity
- Good Automation
- Strong Competitive Position

Strengths should be included in category outputs and summarized in the Digital Business Health Assessment page.

---

# Weaknesses and Revenue Opportunities

Weaknesses must identify confirmed gaps, risks, or performance issues.

Each meaningful weakness should produce one or more Revenue Opportunities where appropriate.

Examples:

| Weakness | Revenue Opportunity |
| --- | --- |
| Inactive Facebook | Improve local visibility and trust |
| No Website | Capture search traffic and quote requests |
| Poor Reviews | Increase conversion from local search |
| Low Automation | Recover missed leads and improve follow-up |
| No Contact Form | Convert website visitors into quote requests |

Revenue Opportunities should describe the business upside before mapping to services.

---

# Service Opportunity Mapping

Service mapping must be separate from scoring logic.

Scoring categories identify conditions, strengths, weaknesses, and opportunities.

A separate service mapping layer translates Revenue Opportunities into Service Opportunities and Recommended Services.

Examples:

| Condition | Revenue Opportunity | Recommended Service |
| --- | --- | --- |
| Inactive Facebook | Improve visibility and trust | Monthly Social Media Management |
| No Website | Capture search traffic and quote requests | Website Design |
| Outdated Website | Improve credibility and conversion | Website Refresh |
| Poor Reviews | Increase trust and conversion | Review Growth System |
| Low Automation | Recover missed leads and improve follow-up | Revenue Recovery Installation |
| No CRM | Improve lead tracking and follow-up | CRM Implementation |
| No Booking | Reduce friction for prospects | Online Booking System |

Recommended Services must not be hardcoded inside category scoring calculations.

---

# Recommended Service Metadata

Every Recommended Service must include:

- Estimated Business Impact
- Estimated Revenue Improvement, where available
- Implementation Difficulty
- Estimated Implementation Time

## Estimated Business Impact

Allowed values:

- HIGH
- MEDIUM
- LOW

## Estimated Revenue Improvement

Estimated Revenue Improvement should be included when enough data is available.

If data is insufficient, the value may be marked unavailable rather than guessed.

## Implementation Difficulty

Implementation Difficulty should communicate practical delivery complexity.

Allowed values:

- LOW
- MEDIUM
- HIGH

## Estimated Implementation Time

Estimated Implementation Time should use business-friendly ranges.

Examples:

- Same day
- 1–3 days
- 1–2 weeks
- 2–4 weeks
- 30–90 days

---

# Quick Wins

Quick Wins are required in every report.

Quick Wins are practical, low-cost or immediate actions the business owner can take today.

Quick Wins should provide genuine value before any sales conversation.

Examples:

- Claim Google Business Profile
- Post one completed project every week
- Begin requesting Google Reviews
- Add an Online Quote Form
- Add a click-to-call button
- Install AI Receptionist
- Respond to recent reviews
- Add service-area language to the website

Quick Wins must be business-readable and action-oriented.

---

# Configuration Requirements

The following must be configuration-driven:

- Category Weights
- Grade Boundaries
- Priority Rules
- Confidence Penalties
- Enabled Categories
- Service Opportunity Mappings
- Recommended Service Metadata defaults

Avoid duplicated constants.

Avoid unexplained scoring values.

Do not over-engineer configuration.

A lightweight configuration file or module is sufficient for Version 2.0 implementation.

---

# PDF Integration

The Revenue Recovery Intelligence Report must include a dedicated page immediately after the Executive Summary.

Page title:

Digital Business Health Assessment

This page must display:

- Business Intelligence Score
- Business Grade
- Assessment Confidence
- Category Scores
- Strengths
- Weaknesses
- Revenue Opportunities
- Quick Wins
- Recommended Services

The PDF layer must consume structured Business Intelligence Engine output.

The PDF layer must not recalculate scores.

The PDF layer must not apply service mapping logic.

---

# Modularity and Future Categories

Each assessment category should be implemented as a lightweight independent module or function.

Heavy plugin architectures are not required for Version 2.0.

Future categories must plug into the engine without redesign.

Future categories may include:

- SEO
- AI Readiness
- CRM
- Customer Experience
- Advertising
- Operations
- Referral Systems
- Website Performance
- Lead Response Time
- Email Marketing
- SMS Marketing
- Review Velocity
- Business Automation
- Operational Maturity

Future categories must follow the same Category Output Contract.

---

# Acceptance Criteria

✓ Status, version, owner, and update date are defined.

✓ Business Intelligence Score, Revenue Opportunity Score, and Priority Score are separate.

✓ Business Intelligence Score measures business health.

✓ Revenue Opportunity Score measures business upside.

✓ Priority Score measures internal outreach urgency.

✓ Priority Score is internal only.

✓ Explicit Business Grade boundaries are defined.

✓ Every category returns the same output contract.

✓ Every category score includes a human-readable explanation.

✓ Assessment Confidence measures data quality only.

✓ Missing or unavailable data reduces confidence only unless a negative condition is confirmed.

✓ Strengths and positive reinforcement are required.

✓ Quick Wins are required.

✓ Weaknesses map to Revenue Opportunities.

✓ Revenue Opportunities map to Recommended Services.

✓ Service mapping remains separate from scoring logic.

✓ Recommended Services include impact, revenue improvement, difficulty, and implementation time.

✓ Scoring weights, grade boundaries, priority rules, confidence penalties, and enabled categories are configuration-driven.

✓ PDF integration requirements are defined.

✓ Future categories can be added without redesign.

---

# Acceptance Checklist

Before implementation begins, confirm:

- The document is treated as the frozen Version 2.0 functional specification.
- No implementation code is included in this specification.
- No Python files were modified as part of this documentation task.
- No tests were created as part of this documentation task.
- Runtime behavior was not changed.
- The implementation team can build the engine from this specification without redefining core architecture.
