"""Campaign prospect list exporter."""

import csv
import logging
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
)

from repositories.campaign_results_repository import (
    CampaignResultsRepository,
)


logger = logging.getLogger(__name__)

PROSPECT_LIST_HEADERS = [
    "Prospect ID",
    "Company",
    "City",
    "State",
    "Business Intelligence Score",
    "Business Grade",
    "Revenue Opportunity Score",
    "Priority Score",
    "Assessment Confidence",
    "Communication Readiness",
    "Website",
    "Facebook",
    "Email",
    "Phone",
    "Campaign ID",
    "Assessment Date",
]


def export_campaign_results(
    repository: CampaignResultsRepository,
    campaign_id: str,
    output_dir: Path,
) -> Dict[str, Path]:
    """Export campaign assessment results to CSV, XLSX, and PDF."""

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        rows = build_prospect_rows(repository, campaign_id)

        csv_path = output_dir / "Prospect_List.csv"
        xlsx_path = output_dir / "Prospect_List.xlsx"
        pdf_path = output_dir / "Prospect_List.pdf"

        write_csv(rows, csv_path)
        write_xlsx(rows, xlsx_path)
        write_pdf(rows, pdf_path)

        logger.info("Campaign prospect list exported: %s", output_dir)

        return {
            "csv": csv_path,
            "xlsx": xlsx_path,
            "pdf": pdf_path,
        }
    except OSError as exc:
        raise OSError(f"Failed to export campaign results: {exc}") from exc


def build_prospect_rows(
    repository: CampaignResultsRepository,
    campaign_id: str,
) -> List[Dict[str, Any]]:
    """Build canonical prospect rows from repository assessments."""

    rows = []

    for assessment in repository.get_all():
        result = assessment.to_flat_dict()
        rows.append({
            "Prospect ID": result.get("prospect_id", ""),
            "Company": result.get("company_name", ""),
            "City": result.get("city", ""),
            "State": result.get("state", ""),
            "Business Intelligence Score":
                result.get("business_intelligence_score", ""),
            "Business Grade": result.get("business_grade", ""),
            "Revenue Opportunity Score":
                result.get("revenue_opportunity_score", ""),
            "Priority Score": result.get("priority_score", ""),
            "Assessment Confidence":
                result.get("assessment_confidence", ""),
            "Communication Readiness":
                result.get("communication_readiness", "Pending"),
            "Website": result.get("website", ""),
            "Facebook": result.get("facebook", ""),
            "Email": result.get("email", ""),
            "Phone": result.get("phone", ""),
            "Campaign ID": result.get("campaign_id", campaign_id),
            "Assessment Date": result.get("assessment_date", ""),
        })

    return rows


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    """Write prospect rows to CSV."""

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=PROSPECT_LIST_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: List[Dict[str, Any]], path: Path) -> None:
    """Write prospect rows to a simple XLSX workbook."""

    sheet_xml = _worksheet_xml(rows)

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _content_types_xml())
        archive.writestr("_rels/.rels", _root_relationships_xml())
        archive.writestr("xl/workbook.xml", _workbook_xml())
        archive.writestr("xl/_rels/workbook.xml.rels", _workbook_relationships_xml())
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def write_pdf(rows: List[Dict[str, Any]], path: Path) -> None:
    """Write prospect rows to a simple professional PDF table."""

    doc = SimpleDocTemplate(
        str(path),
        pagesize=landscape(letter),
        leftMargin=24,
        rightMargin=24,
        topMargin=24,
        bottomMargin=24,
    )
    styles = getSampleStyleSheet()
    table_data = [
        [
            Paragraph(str(header), styles["Normal"])
            for header in PROSPECT_LIST_HEADERS
        ]
    ]

    for row in rows:
        table_data.append([
            Paragraph(str(row.get(header, "")), styles["Normal"])
            for header in PROSPECT_LIST_HEADERS
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    doc.build([table])


def _worksheet_xml(rows: List[Dict[str, Any]]) -> str:
    """Return worksheet XML for the XLSX file."""

    xml_rows = []
    all_rows: List[Iterable[Any]] = [
        PROSPECT_LIST_HEADERS,
        *[
            [row.get(header, "") for header in PROSPECT_LIST_HEADERS]
            for row in rows
        ],
    ]

    for row_index, row in enumerate(all_rows, start=1):
        cells = []

        for column_index, value in enumerate(row, start=1):
            cell_reference = f"{_column_letter(column_index)}{row_index}"
            cells.append(
                f'<c r="{cell_reference}" t="inlineStr">'
                f"<is><t>{escape(str(value))}</t></is></c>"
            )

        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{''.join(xml_rows)}</sheetData>"
        "</worksheet>"
    )


def _column_letter(index: int) -> str:
    """Return Excel column letters for a 1-based column index."""

    letters = ""

    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters

    return letters


def _content_types_xml() -> str:
    """Return XLSX content types XML."""

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )


def _root_relationships_xml() -> str:
    """Return XLSX root relationships XML."""

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )


def _workbook_xml() -> str:
    """Return XLSX workbook XML."""

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Prospect List" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )


def _workbook_relationships_xml() -> str:
    """Return XLSX workbook relationships XML."""

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
