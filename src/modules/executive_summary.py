from modules.data_loader import (
    load_company,
    load_competitors,
)
from modules.distress_score import (
    calculate_distress_score,
)


def generate_summary(company_id):

    company = load_company(company_id)
    competitors = load_competitors(company_id)

    average_reviews = (
        sum(c["review_count"] for c in competitors)
        / len(competitors)
    )

    review_gap = (
        average_reviews
        - company["review_count"]
    )

    estimated_loss = (
        review_gap * 500
    )

    # Temporary until we build the
    # full automation scoring module.
    automation_score = 15

    # Opportunity Level
    if estimated_loss >= 100000:
        opportunity = "HIGH 🔴"
        recommended_action = (
            "Implement Revenue Recovery Systems "
            "Within The Next 90 Days"
        )

    elif estimated_loss >= 50000:
        opportunity = "MEDIUM 🟠"
        recommended_action = (
            "Implement Process Improvements"
        )

    else:
        opportunity = "LOW 🟢"
        recommended_action = (
            "Maintain Current Performance"
        )

    # Top Competitor
    top_competitor = max(
        competitors,
        key=lambda x: x["review_count"]
    )

    review_multiple = (
        top_competitor["review_count"]
        / company["review_count"]
    )

    # Market Position
    total_companies = len(competitors) + 1

    all_companies = competitors + [
        {
            "name": company["company_name"],
            "review_count": company["review_count"]
        }
    ]

    sorted_companies = sorted(
        all_companies,
        key=lambda x: x["review_count"],
        reverse=True
    )

    rank = 1

    for i, c in enumerate(sorted_companies):
        if c["name"] == company["company_name"]:
            rank = i + 1
            break

    if rank == total_companies:
        standing = "⚠️ Last Place"
    elif rank == 1:
        standing = "🏆 Market Leader"
    else:
        standing = "Mid Pack"

    market_position = {
        "rank": rank,
        "total": total_companies,
        "standing": standing,
    }

    # Local Visibility Assessment
    if review_multiple >= 5:
        search_visibility = "LOW"
        customer_loss = "HIGH"
        caller_ratio = (
            "Approximately 9 out of 10 online "
            "searchers are likely contacting "
            "competitors first."
        )

    elif review_multiple >= 2:
        search_visibility = "MODERATE"
        customer_loss = "MEDIUM"
        caller_ratio = (
            "Approximately 6 out of 10 online "
            "searchers are likely contacting "
            "competitors first."
        )

    else:
        search_visibility = "GOOD"
        customer_loss = "LOW"
        caller_ratio = (
            "Your business is likely receiving "
            "a healthy share of online enquiries."
        )

    visibility_assessment = {
        "search_visibility":
            search_visibility,
        "customer_loss":
            customer_loss,
        "caller_ratio":
            caller_ratio,
        "discovery_method":
            "Referrals and Existing Customers",
    }

    attention_alert = (
        f"Your top competitor has earned "
        f"{top_competitor['review_count'] - company['review_count']} "
        f"more customer reviews and has "
        f"{review_multiple:.1f}x more social proof, "
        f"making them significantly more likely "
        f"to be contacted by new customers "
        f"searching online."
    )
    metrics = {
        "Revenue Leakage":
            f"${estimated_loss:,.0f}+",

        "Review Gap":
            f"{review_gap:.0f} Reviews",

        "Competitor Advantage":
            f"{review_multiple:.1f}x Higher",

        "Automation Score":
            f"{automation_score}/100",

        "Opportunity Level":
            opportunity,
    }

    narrative = f"""
Executive Summary
────────────────────────────────

{company['company_name']} is currently
underperforming compared to direct
competitors in the {company['city']},
{company['state']} market.

The company currently has
{company['review_count']} Google reviews,
while direct competitors average
{average_reviews:.0f} reviews.

This gap significantly impacts local
search visibility, customer trust,
and lead generation.

Based on our benchmarking model,
we estimate that the company may be
losing approximately
${estimated_loss:,.0f}+ in
annual revenue that may currently be
going to competitors.
By improving communication,
automating follow-up systems,
and strengthening online reputation,
the business has a significant
opportunity to increase market share
and revenue.

Overall Opportunity Assessment:
{opportunity}
"""

    assessment = {
        "metrics": metrics,
        "top_competitor": top_competitor,
        "market_position": market_position,
        "visibility_assessment":
            visibility_assessment,
        "review_multiple": review_multiple,
        "attention_alert": attention_alert,
        "recommended_action":
            recommended_action,
        "narrative": narrative,
        "estimated_loss":
            estimated_loss,
        "review_gap":
            review_gap,
        "automation_score":
            automation_score,
        "opportunity_level":
            opportunity,
    }

    distress_assessment = calculate_distress_score(
        company,
        competitors,
        assessment,
    )

    assessment["distress_assessment"] = distress_assessment
    assessment["distress_score"] = distress_assessment["score"]
    assessment["distress_grade"] = distress_assessment["grade"]
    assessment["distress_priority"] = distress_assessment["priority"]
    assessment["distress_reasons"] = distress_assessment["reasons"]

    return assessment
