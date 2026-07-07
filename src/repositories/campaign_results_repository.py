"""In-memory repository for campaign assessment results."""

import copy
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


@dataclass
class CampaignResultsRepository:
    """Store and summarize campaign assessment results in memory."""

    campaign_results: List[Dict[str, Any]] = field(default_factory=list)

    def add_result(self, result: Dict[str, Any]) -> None:
        """Add one campaign assessment result."""

        prospect_id = result.get("prospect_id")

        if not prospect_id:
            raise ValueError("Campaign result must include prospect_id.")

        logger.info("Adding campaign assessment result: %s", prospect_id)
        self.campaign_results.append(copy.deepcopy(result))

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all campaign assessment results."""

        return copy.deepcopy(self.campaign_results)

    def get_by_prospect_id(self, prospect_id: str) -> Optional[Dict[str, Any]]:
        """Return one assessment result by Prospect ID."""

        for result in self.campaign_results:
            if result.get("prospect_id") == prospect_id:
                return copy.deepcopy(result)

        return None

    def count(self) -> int:
        """Return the number of stored campaign assessment results."""

        return len(self.campaign_results)

    def summary(self) -> Dict[str, Any]:
        """Return aggregate campaign assessment statistics."""

        if not self.campaign_results:
            return {
                "count": 0,
                "average_business_intelligence_score": None,
                "average_revenue_opportunity_score": None,
                "average_priority_score": None,
                "highest_priority_prospect": None,
                "lowest_business_intelligence_score": None,
            }

        return {
            "count": self.count(),
            "average_business_intelligence_score":
                self._average("business_intelligence_score"),
            "average_revenue_opportunity_score":
                self._average("revenue_opportunity_score"),
            "average_priority_score":
                self._average("priority_score"),
            "highest_priority_prospect":
                self._highest_by("priority_score"),
            "lowest_business_intelligence_score":
                self._lowest_by("business_intelligence_score"),
        }

    def _average(self, field_name: str) -> float:
        """Return the average numeric value for a result field."""

        total = sum(
            int(result[field_name])
            for result in self.campaign_results
        )

        return total / self.count()

    def _highest_by(self, field_name: str) -> Dict[str, Any]:
        """Return the result with the highest value for a field."""

        return copy.deepcopy(
            max(
                self.campaign_results,
                key=lambda result: int(result[field_name]),
            )
        )

    def _lowest_by(self, field_name: str) -> Dict[str, Any]:
        """Return the result with the lowest value for a field."""

        return copy.deepcopy(
            min(
                self.campaign_results,
                key=lambda result: int(result[field_name]),
            )
        )
