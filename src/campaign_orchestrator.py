"""Campaign Orchestrator.

This module reads campaign configuration, loads mock prospects, prepares a
campaign output workspace, and runs each prospect through the Business
Intelligence Engine. It intentionally does not generate assessment reports,
send messages, call Supabase, or use APIs.
"""

import json
import logging
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from exporters.campaign_exporter import export_campaign_results
from models.assessment import Assessment
from modules.business_intelligence import calculate_business_intelligence
from repositories.campaign_results_repository import (
    CampaignResultsRepository,
)


CAMPAIGN_CONFIG_PATH = Path("config/campaign_config.json")
MOCK_PROSPECTS_PATH = Path("data/mock/mock_prospects.json")
CAMPAIGN_OUTPUT_ROOT = Path("output/campaigns")
COMPANY_DATA_DIR = Path("data/companies")
COMPETITOR_DATA_DIR = Path("data/competitors")

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure console logging for the orchestrator."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def load_json_file(path: Path) -> Any:
    """Load and return JSON data from a file path."""

    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Required file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in file: {path}") from exc


def load_campaign_config(path: Path = CAMPAIGN_CONFIG_PATH) -> Dict[str, Any]:
    """Load and validate the campaign configuration."""

    config = load_json_file(path)

    if not isinstance(config, dict):
        raise ValueError("Campaign configuration must be a JSON object.")

    validate_campaign_config(config)

    return config


def load_mock_prospects(path: Path = MOCK_PROSPECTS_PATH) -> List[Dict[str, Any]]:
    """Load and validate mock prospects for the campaign."""

    prospects = load_json_file(path)

    if not isinstance(prospects, list):
        raise ValueError("Mock prospects must be a JSON array.")

    for prospect in prospects:
        if not isinstance(prospect, dict):
            raise ValueError("Each mock prospect must be a JSON object.")

    return prospects


def validate_campaign_config(config: Dict[str, Any]) -> None:
    """Validate required campaign configuration fields."""

    required_fields = [
        ("campaign", "campaign_id"),
        ("campaign", "campaign_name"),
        ("geography", "region"),
        ("geography", "country"),
        ("geography", "state"),
        ("industry", "primary"),
        ("prospect_selection", "max_prospects"),
    ]

    for section, key in required_fields:
        get_required_value(config, section, key)


def get_required_value(
    data: Dict[str, Any],
    section: str,
    key: str,
) -> Any:
    """Return a required nested configuration value."""

    section_data = data.get(section)

    if not isinstance(section_data, dict):
        raise ValueError(f"Missing configuration section: {section}")

    value = section_data.get(key)

    if value is None:
        raise ValueError(f"Missing configuration value: {section}.{key}")

    return value


def prepare_campaign_workspace(config: Dict[str, Any]) -> Path:
    """Create and return the campaign output directory."""

    campaign_id = str(
        get_required_value(config, "campaign", "campaign_id")
    )
    output_dir = CAMPAIGN_OUTPUT_ROOT / campaign_id
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def print_campaign_summary(
    config: Dict[str, Any],
    prospects: List[Dict[str, Any]],
) -> None:
    """Print the required campaign startup summary."""

    campaign_id = get_required_value(config, "campaign", "campaign_id")
    campaign_name = get_required_value(config, "campaign", "campaign_name")
    region = get_required_value(config, "geography", "region")
    country = get_required_value(config, "geography", "country")
    state = get_required_value(config, "geography", "state")
    industry = get_required_value(config, "industry", "primary")
    max_prospects = get_required_value(
        config,
        "prospect_selection",
        "max_prospects",
    )

    print("Campaign Started")
    print(f"Campaign ID: {campaign_id}")
    print(f"Campaign Name: {campaign_name}")
    print(f"Region: {region}")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"Industry: {industry}")
    print(f"Maximum Prospects: {max_prospects}")
    print(f"Number of prospects loaded: {len(prospects)}")
    print("Campaign Ready")


def normalize_name(value: str) -> str:
    """Normalize a business name for local matching."""

    return "".join(
        character.lower()
        for character in value
        if character.isalnum()
    )


def find_company_file(
    prospect: Dict[str, Any],
    company_data_dir: Path = COMPANY_DATA_DIR,
) -> Optional[Path]:
    """Locate the company JSON file that matches a prospect."""

    company_id = prospect.get("company_id")

    if company_id:
        direct_path = company_data_dir / f"{company_id}.json"

        if direct_path.exists():
            return direct_path

    prospect_name = prospect.get("company_name")

    if not prospect_name:
        return None

    normalized_prospect_name = normalize_name(str(prospect_name))

    for company_file in sorted(company_data_dir.glob("*.json")):
        try:
            company = load_json_file(company_file)
        except (FileNotFoundError, ValueError) as exc:
            logger.warning("Skipping unreadable company file %s: %s", company_file, exc)
            continue

        if not isinstance(company, dict):
            logger.warning("Skipping invalid company file: %s", company_file)
            continue

        company_name = company.get("company_name")

        if (
            company_name
            and normalize_name(str(company_name)) == normalized_prospect_name
        ):
            return company_file

    return None


def find_competitor_file(
    company_file: Path,
    competitor_data_dir: Path = COMPETITOR_DATA_DIR,
) -> Optional[Path]:
    """Locate the competitor JSON file for a company JSON file."""

    competitor_file = competitor_data_dir / f"{company_file.stem}_competitors.json"

    if competitor_file.exists():
        return competitor_file

    return None


def load_company_profile(
    prospect: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Load the company profile for a prospect."""

    company_file = find_company_file(prospect)

    if company_file is None:
        logger.warning(
            "Company file not found for prospect: %s",
            prospect.get("company_name", "Unknown"),
        )
        return None

    company = load_json_file(company_file)

    if not isinstance(company, dict):
        raise ValueError(f"Company data must be a JSON object: {company_file}")

    company["_company_profile_path"] = str(company_file)

    return company


def load_competitor_profile(company: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Load the competitor profile for a company profile."""

    company_profile_path = company.get("_company_profile_path")

    if not company_profile_path:
        raise ValueError("Company profile path is required for competitor lookup.")

    company_file = Path(str(company_profile_path))
    competitor_file = find_competitor_file(company_file)

    if competitor_file is None:
        logger.warning(
            "Competitor file not found for company file: %s",
            company_file,
        )
        return None

    competitor_data = load_json_file(competitor_file)

    if not isinstance(competitor_data, dict):
        raise ValueError(
            f"Competitor data must be a JSON object: {competitor_file}"
        )

    competitors = competitor_data.get("competitors")

    if not isinstance(competitors, list):
        raise ValueError(
            f"Competitor data must contain a competitors array: {competitor_file}"
        )

    return competitors


def run_business_intelligence(
    company: Dict[str, Any],
    competitors: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Execute the Business Intelligence Engine for one company."""

    company_for_assessment = {
        key: value
        for key, value in company.items()
        if not key.startswith("_")
    }

    return calculate_business_intelligence(
        company_for_assessment,
        competitors,
    )


def process_prospect(
    prospect: Dict[str, Any],
    campaign_results_repository: CampaignResultsRepository,
    campaign_id: str,
    industry: str,
    country: str,
) -> bool:
    """Process one prospect and store its assessment in the repository."""

    try:
        company = load_company_profile(prospect)

        if company is None:
            return False

        competitors = load_competitor_profile(company)

        if competitors is None:
            return False

        business_intelligence = run_business_intelligence(company, competitors)
        assessment = Assessment.from_business_intelligence(
            campaign_id=campaign_id,
            prospect=prospect,
            company_profile=company,
            competitor_profile=competitors,
            business_intelligence=business_intelligence,
            industry=industry,
            country=country,
            assessment_date=date.today().isoformat(),
        )
        campaign_results_repository.add_result(assessment)
        return True
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.warning(
            "Skipping prospect %s: %s",
            prospect.get("company_name", "Unknown"),
            exc,
        )
        return False


def summarize_campaign(
    prospects: List[Dict[str, Any]],
    campaign_results_repository: CampaignResultsRepository,
) -> None:
    """Print the final campaign assessment summary."""

    total_prospects = len(prospects)
    successful_assessments = campaign_results_repository.count()
    failed_assessments = total_prospects - successful_assessments
    summary = campaign_results_repository.summary()

    print("Campaign Complete")
    print(f"Total Prospects: {total_prospects}")
    print(f"Successful Assessments: {successful_assessments}")
    print(f"Failed Assessments: {failed_assessments}")
    print(
        "Average Business Intelligence Score: "
        f"{_format_average(summary['average_business_intelligence_score'])}"
    )
    print(
        "Average Revenue Opportunity Score: "
        f"{_format_average(summary['average_revenue_opportunity_score'])}"
    )
    print(
        "Average Priority Score: "
        f"{_format_average(summary['average_priority_score'])}"
    )
    print(
        "Highest Priority Prospect: "
        f"{_format_highest_priority(summary['highest_priority_prospect'])}"
    )
    print(
        "Lowest Business Intelligence Score: "
        f"{_format_lowest_bi(summary['lowest_business_intelligence_score'])}"
    )


def _format_average(value: Optional[float]) -> str:
    """Return a formatted average score from repository statistics."""

    if value is None:
        return "N/A"

    return f"{value:.1f}"


def _format_highest_priority(result: Optional[Dict[str, Any]]) -> str:
    """Return formatted highest-priority prospect text."""

    if result is None:
        return "N/A"

    return (
        f"{result.get('company_name', 'Unknown')} "
        f"({result['priority_score']})"
    )


def _format_lowest_bi(result: Optional[Dict[str, Any]]) -> str:
    """Return formatted lowest Business Intelligence Score text."""

    if result is None:
        return "N/A"

    return (
        f"{result.get('company_name', 'Unknown')} "
        f"({result['business_intelligence_score']})"
    )


def run_campaign(
    config: Dict[str, Any],
    prospects: List[Dict[str, Any]],
) -> None:
    """Print campaign details and process loaded prospects."""

    print_campaign_summary(config, prospects)
    campaign_id = str(get_required_value(config, "campaign", "campaign_id"))
    industry = str(get_required_value(config, "industry", "primary"))
    country = str(get_required_value(config, "geography", "country"))
    output_dir = CAMPAIGN_OUTPUT_ROOT / campaign_id
    logger.info("Campaign workspace prepared: %s", output_dir)

    logger.info("Processing prospects through Business Intelligence Engine.")
    campaign_results_repository = CampaignResultsRepository()

    for prospect in prospects:
        process_prospect(
            prospect,
            campaign_results_repository,
            campaign_id,
            industry,
            country,
        )

    summarize_campaign(prospects, campaign_results_repository)
    export_campaign_results(
        campaign_results_repository,
        campaign_id,
        output_dir,
    )


def run_campaign_orchestrator() -> Path:
    """Run the complete campaign orchestration workflow."""

    logger.info("Loading campaign configuration.")
    config = load_campaign_config()

    logger.info("Loading mock prospects.")
    prospects = load_mock_prospects()

    logger.info("Preparing campaign workspace.")
    output_dir = prepare_campaign_workspace(config)

    run_campaign(config, prospects)

    return output_dir


def main() -> int:
    """Command-line entry point for the campaign orchestrator."""

    configure_logging()

    try:
        logger.info("Loading campaign configuration.")
        config = load_campaign_config()

        logger.info("Loading mock prospects.")
        prospects = load_mock_prospects()

        logger.info("Preparing campaign workspace.")
        prepare_campaign_workspace(config)

        run_campaign(config, prospects)
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("Campaign Orchestrator failed: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
