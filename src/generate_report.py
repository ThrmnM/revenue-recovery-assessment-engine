from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from modules.data_loader import (
    load_company,
    load_competitors,
)
from modules.executive_summary import (
    generate_summary,
)
from modules.recommendation_engine import (
    generate_recommendations,
)


PRIMARY = colors.HexColor("#1F2937")
SECONDARY = colors.HexColor("#4B5563")
ACCENT = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#EFF6FF")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
BORDER = colors.HexColor("#D1D5DB")
WHITE = colors.white

STATUS_COLORS = {
    "CRITICAL": colors.HexColor("#B91C1C"),
    "HIGH": colors.HexColor("#DC2626"),
    "MEDIUM": colors.HexColor("#D97706"),
    "LOW": colors.HexColor("#15803D"),
}

PRIORITY_COLORS = {
    "CRITICAL": colors.HexColor("#B91C1C"),
    "HIGH": colors.HexColor("#F97316"),
    "MEDIUM": colors.HexColor("#CA8A04"),
    "LOW": colors.HexColor("#15803D"),
}


def make_styles():
    """Create report typography styles."""

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CoverCompany",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=19,
            leading=24,
            textColor=PRIMARY,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CoverLocation",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=SECONDARY,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=PRIMARY,
            spaceBefore=4,
            spaceAfter=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CardTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=PRIMARY,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=PRIMARY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Muted",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=SECONDARY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="MetricLabel",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=SECONDARY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="MetricValue",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=PRIMARY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallCaps",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=ACCENT,
        )
    )

    return styles


def clean_text(value):
    """Return PDF-safe text without unsupported emoji glyphs."""

    return str(value).encode("ascii", "ignore").decode("ascii").strip()


def safe(value):
    """Escape PDF paragraph text after removing unsupported glyphs."""

    return xml_escape(clean_text(value))


def status_label(value):
    """Return a clean status label without emoji or extra symbols."""

    return clean_text(value).split()[0].upper()


def narrative_text(value):
    """Convert source narrative line breaks into report-style paragraphs."""

    lines = [
        clean_text(line)
        for line in str(value).splitlines()
        if clean_text(line)
    ]
    lines = [
        line
        for line in lines
        if line != "Executive Summary"
        and set(line) != {"-"}
    ]

    return " ".join(lines)


def draw_header(canvas, doc):
    """Draw a consistent header on body pages."""

    if doc.page == 1:
        return

    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(SECONDARY)
    canvas.drawString(
        doc.leftMargin,
        letter[1] - 0.45 * inch,
        "Revenue Recovery Assessment",
    )
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin,
        letter[1] - 0.55 * inch,
        letter[0] - doc.rightMargin,
        letter[1] - 0.55 * inch,
    )
    canvas.restoreState()


def draw_footer(canvas, doc):
    """Draw page numbering and a subtle footer rule."""

    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin,
        0.5 * inch,
        letter[0] - doc.rightMargin,
        0.5 * inch,
    )
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SECONDARY)
    canvas.drawRightString(
        letter[0] - doc.rightMargin,
        0.32 * inch,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def draw_page_frame(canvas, doc):
    """Draw shared page furniture."""

    draw_header(canvas, doc)
    draw_footer(canvas, doc)


def section_title(title, styles):
    """Create a consulting-report section heading."""

    return KeepTogether(
        [
            Paragraph(safe(title), styles["SectionTitle"]),
            Table(
                [[""]],
                colWidths=[6.7 * inch],
                rowHeights=[2],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                        ("LINEBELOW", (0, 0), (-1, -1), 0, ACCENT),
                    ]
                ),
            ),
            Spacer(1, 10),
        ]
    )


def metric_box(label, value, styles, value_color=PRIMARY, width=3.12 * inch):
    """Create a compact metric box."""

    value_style = ParagraphStyle(
        name=f"MetricValue{label}",
        parent=styles["MetricValue"],
        textColor=value_color,
    )

    table = Table(
        [
            [Paragraph(safe(label), styles["MetricLabel"])],
            [Paragraph(safe(value), value_style)],
        ],
        colWidths=[width],
        rowHeights=[18, 28],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    return table


def colored_status(
    label,
    status,
    styles,
    palette=STATUS_COLORS,
    width=3.12 * inch,
):
    """Create a color-coded status row."""

    clean_status = status_label(status)
    status_color = palette.get(clean_status, SECONDARY)
    status_style = ParagraphStyle(
        name=f"Status{label}{clean_status}",
        parent=styles["MetricValue"],
        fontSize=10,
        textColor=status_color,
    )

    return Table(
        [
            [
                Paragraph(safe(label), styles["MetricLabel"]),
                Paragraph(safe(clean_status), status_style),
            ]
        ],
        colWidths=[width * 0.48, width * 0.52],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        ),
    )


def metric_grid(metrics):
    """Lay metric boxes out in a two-column grid."""

    rows = []
    for index in range(0, len(metrics), 2):
        row = metrics[index:index + 2]
        if len(row) == 1:
            row.append(Spacer(1, 1))
        rows.append(row)

    table = Table(rows, colWidths=[3.25 * inch, 3.25 * inch])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return table


def card(title, body_items, styles):
    """Create a reusable consulting card."""

    content = [[Paragraph(safe(title), styles["CardTitle"])]]

    for item in body_items:
        content.append([item])

    table = Table(content, colWidths=[6.7 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return KeepTogether([table, Spacer(1, 8)])


def bullet_list(items, styles):
    """Format a list as simple PDF-safe bullets."""

    return [
        Paragraph(f"- {safe(item)}", styles["Body"])
        for item in items
    ]


def field_line(label, value, styles):
    """Create a compact label/value line."""

    return Paragraph(
        f"<b>{safe(label)}:</b> {safe(value)}",
        styles["Body"],
    )


def detail_grid(items, styles):
    """Create a compact two-column detail grid."""

    cells = [
        Paragraph(
            f"<b>{safe(label)}:</b> {safe(value)}",
            styles["Body"],
        )
        for label, value in items
    ]
    rows = []

    for index in range(0, len(cells), 2):
        row = cells[index:index + 2]
        if len(row) == 1:
            row.append(Paragraph("", styles["Body"]))
        rows.append(row)

    table = Table(rows, colWidths=[3.2 * inch, 3.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return table


def build_cover(story, company, summary, distress_assessment, styles):
    """Build the consulting-style cover page."""

    opportunity = status_label(summary["opportunity_level"])
    priority = status_label(distress_assessment["priority"])

    story.append(Spacer(1, 0.55 * inch))
    story.append(
        Paragraph("Revenue Recovery Assessment", styles["CoverTitle"])
    )
    story.append(Paragraph(safe(company["company_name"]), styles["CoverCompany"]))
    story.append(
        Paragraph(
            f"{safe(company['city'])}, {safe(company['state'])}",
            styles["CoverLocation"],
        )
    )
    story.append(Spacer(1, 0.45 * inch))

    top_metrics = Table(
        [
            [
                metric_box(
                    "Estimated Annual Revenue Leakage",
                    f"${summary['estimated_loss']:,.0f}+",
                    styles,
                    width=3.12 * inch,
                ),
                colored_status(
                    "Opportunity Level",
                    opportunity,
                    styles,
                    STATUS_COLORS,
                    width=3.12 * inch,
                ),
            ],
            [
                metric_box(
                    "Distress Score",
                    f"{distress_assessment['score']}/100",
                    styles,
                    width=3.12 * inch,
                ),
                colored_status(
                    "Priority",
                    priority,
                    styles,
                    PRIORITY_COLORS,
                    width=3.12 * inch,
                ),
            ],
        ],
        colWidths=[3.25 * inch, 3.25 * inch],
    )
    top_metrics.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(top_metrics)
    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Table(
            [
                [
                    Paragraph(
                        "Prepared as a market-position and revenue recovery "
                        "brief for leadership review.",
                        styles["Muted"],
                    )
                ]
            ],
            colWidths=[6.7 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#BFDBFE")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        )
    )
    story.append(PageBreak())


def build_executive_summary(story, company, summary, styles):
    """Build the executive summary section."""

    top_competitor = summary["top_competitor"]
    metrics = [
        metric_box(
            "Estimated Revenue Leakage",
            f"${summary['estimated_loss']:,.0f}+",
            styles,
        ),
        metric_box(
            "Google Review Gap",
            f"{summary['review_gap']:.0f} reviews",
            styles,
        ),
        metric_box("Top Competitor", top_competitor["name"], styles),
        metric_box("Google Rating", f"{company['rating']:.1f}", styles),
        metric_box("Google Reviews", company["review_count"], styles),
        colored_status(
            "Opportunity Level",
            summary["opportunity_level"],
            styles,
            STATUS_COLORS,
        ),
    ]

    story.append(section_title("Executive Summary", styles))
    story.append(metric_grid(metrics))
    story.append(Spacer(1, 12))
    story.append(
        Table(
            [[
                Paragraph(
                    safe(narrative_text(summary["narrative"])),
                    styles["Body"],
                )
            ]],
            colWidths=[6.7 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                    ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        )
    )
    story.append(Spacer(1, 16))


def build_distress_assessment(story, distress_assessment, styles):
    """Build the distress assessment section."""

    priority = status_label(distress_assessment["priority"])
    metrics = [
        metric_box(
            "Distress Score",
            f"{distress_assessment['score']}/100",
            styles,
        ),
        metric_box("Grade", distress_assessment["grade"], styles),
        colored_status("Priority", priority, styles, PRIORITY_COLORS),
    ]

    story.append(section_title("Distress Assessment", styles))
    story.append(metric_grid(metrics))
    story.append(Spacer(1, 8))

    reason_items = bullet_list(distress_assessment["reasons"], styles)
    story.append(card("Reasons", reason_items, styles))


def build_competitive_analysis(story, company, competitors, styles):
    """Build competitor benchmarking cards."""

    story.append(section_title("Competitive Analysis", styles))

    for competitor in competitors:
        review_gap = competitor["review_count"] - company["review_count"]
        rating_gap = competitor["rating"] - company["rating"]
        estimated_advantage = review_gap * 500

        details = [
            detail_grid(
                [
                    ("Google Rating", f"{competitor['rating']:.1f}"),
                    ("Google Reviews", competitor["review_count"]),
                    ("Review Gap", f"{review_gap:+,} reviews"),
                    ("Rating Gap", f"{rating_gap:+.1f}"),
                    (
                        "Estimated Revenue Advantage",
                        f"${estimated_advantage:,.0f}+ annually",
                    ),
                ],
                styles,
            ),
            Paragraph(
                (
                    f"<b>Strengths:</b> "
                    f"{safe('; '.join(competitor.get('strengths', [])))}"
                ),
                styles["Body"],
            ),
        ]

        story.append(card(competitor["name"], details, styles))

    story.append(PageBreak())


def build_recommendations(story, recommendations, styles):
    """Build professional recommendation cards."""

    story.append(section_title("Recommendations", styles))

    for index, recommendation in enumerate(
        recommendations["recommendations"],
        start=1,
    ):
        content = [
            field_line("Solution", recommendation["solution"], styles),
            field_line("Business Benefit", recommendation["benefit"], styles),
            field_line(
                "Estimated Revenue Recovery",
                f"${recommendation['estimated_recovery']:,}",
                styles,
            ),
        ]
        story.append(card(f"Recommendation {index}", content, styles))

    story.append(PageBreak())


def build_ninety_day_plan(story, recommendations, styles):
    """Build a formatted 90-day implementation timeline."""

    story.append(section_title("90-Day Revenue Recovery Plan", styles))

    phases = [
        ("Days 1-30", recommendations["ninety_day_plan"][0]),
        ("Days 31-60", recommendations["ninety_day_plan"][1]),
        ("Days 61-90", recommendations["ninety_day_plan"][2]),
    ]

    for title, description in phases:
        phase_content = [
            Paragraph(safe(description), styles["Body"]),
        ]
        story.append(card(title, phase_content, styles))

    story.append(Spacer(1, 10))
    story.append(
        Table(
            [[
                Paragraph(
                    "<b>Total Estimated Revenue Recovery</b>",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>${recommendations['estimated_recovery']:,}+</b>",
                    styles["MetricValue"],
                ),
            ]],
            colWidths=[4.35 * inch, 2.15 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#BFDBFE")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        )
    )


def build_report():
    """Generate the Revenue Recovery Assessment PDF."""

    company_id = "abc_gates"

    company = load_company(company_id)
    competitors = load_competitors(company_id)
    summary = generate_summary(company_id)
    distress_assessment = summary["distress_assessment"]

    scores = {
        "automation_score":
            summary["automation_score"]
    }

    recommendations = generate_recommendations(
        company,
        scores
    )

    report_dir = Path("output/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    filename = str(
        report_dir
        / f"{company['company_name'].replace(' ', '_')}_Assessment.pdf"
    )

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
    )

    styles = make_styles()
    story = []

    build_cover(story, company, summary, distress_assessment, styles)
    build_executive_summary(story, company, summary, styles)
    build_distress_assessment(story, distress_assessment, styles)
    build_competitive_analysis(story, company, competitors, styles)
    build_recommendations(story, recommendations, styles)
    build_ninety_day_plan(story, recommendations, styles)

    doc.build(
        story,
        onFirstPage=draw_page_frame,
        onLaterPages=draw_page_frame,
    )

    return filename


if __name__ == "__main__":
    report_filename = build_report()

    print()
    print("PDF Generated:")
    print(report_filename)
