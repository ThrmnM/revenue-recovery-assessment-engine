from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet

from modules.data_loader import (
    load_company,
    load_competitors
)
from modules.executive_summary import (
    generate_summary
)
from modules.recommendation_engine import (
    generate_recommendations
)


company_id = "abc_gates"

company = load_company(company_id)
competitors = load_competitors(company_id)

summary = generate_summary(company_id)

scores = {
    "automation_score":
        summary["automation_score"]
}

recommendations = generate_recommendations(
    company,
    scores
)

filename = (
    f"output/reports/"
    f"{company['company_name'].replace(' ', '_')}"
    f"_Assessment.pdf"
)

doc = SimpleDocTemplate(
    filename,
    pagesize=letter
)

styles = getSampleStyleSheet()
story = []

# ==================================================
# COVER PAGE
# ==================================================

story.append(
    Paragraph(
        "<b>Revenue Recovery Assessment</b>",
        styles["Title"]
    )
)

story.append(Spacer(1, 30))

story.append(
    Paragraph(
        company["company_name"],
        styles["Heading1"]
    )
)

story.append(
    Paragraph(
        f"{company['city']}, {company['state']}",
        styles["Normal"]
    )
)

story.append(Spacer(1, 30))

story.append(
    Paragraph(
        (
            f"<b>Estimated Revenue Leakage:</b> "
            f"${summary['estimated_loss']:,.0f}+"
        ),
        styles["Heading2"]
    )
)

story.append(
    Paragraph(
        (
            f"<b>Opportunity Level:</b> "
            f"{summary['opportunity_level']}"
        ),
        styles["Heading2"]
    )
)

story.append(PageBreak())

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

story.append(
    Paragraph(
        "<b>Executive Summary</b>",
        styles["Heading1"]
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        summary["narrative"].replace(
            "\n",
            "<br/>"
        ),
        styles["Normal"]
    )
)

story.append(PageBreak())

# ==================================================
# RECOMMENDATIONS
# ==================================================

story.append(
    Paragraph(
        "<b>Recommendations</b>",
        styles["Heading1"]
    )
)

story.append(Spacer(1, 20))

for rec in recommendations["recommendations"]:

    story.append(
        Paragraph(
            f"<b>{rec['solution']}</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            rec["benefit"],
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            (
                f"Estimated Recovery: "
                f"${rec['estimated_recovery']:,}"
            ),
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

story.append(PageBreak())

# ==================================================
# 90-DAY PLAN
# ==================================================

story.append(
    Paragraph(
        "<b>90-Day Revenue Recovery Plan</b>",
        styles["Heading1"]
    )
)

story.append(Spacer(1, 20))

for step in recommendations["ninety_day_plan"]:

    story.append(
        Paragraph(
            f"• {step}",
            styles["Normal"]
        )
    )

story.append(Spacer(1, 30))

story.append(
    Paragraph(
        (
            f"<b>Total Estimated Recovery Opportunity:</b> "
            f"${recommendations['estimated_recovery']:,}+"
        ),
        styles["Heading2"]
    )
)

# ==================================================
# BUILD PDF
# ==================================================

doc.build(story)

print()
print("PDF Generated:")
print(filename)
