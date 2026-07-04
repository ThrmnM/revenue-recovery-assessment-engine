from modules.data_loader import (
    load_company,
    load_competitors,
)


def generate_summary(company_id):

    company = load_company(company_id)
    competitors = load_competitors(company_id)

    average_competitor_reviews = (
        sum(
            c["review_count"]
            for c in competitors
        )
        / len(competitors)
    )

    review_gap = (
        average_competitor_reviews
        - company["review_count"]
    )

    estimated_loss = (
        review_gap * 500
    )

    summary = f"""
Executive Summary
--------------------------------

{company['company_name']} is significantly
underperforming compared to direct competitors
in {company['city']}, {company['state']}.

The business currently has
{company['review_count']} Google reviews,
while the average competitor has
{average_competitor_reviews:.0f} reviews.

Based on our benchmarking model,
the business may be losing approximately
${estimated_loss:,.0f}+ annually due to
online reputation and operational issues.

Immediate improvements in communication,
follow-up systems, and customer acquisition
processes could significantly increase
revenue and market share.
"""

    return summary

