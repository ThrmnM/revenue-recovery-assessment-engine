import unittest

from modules.business_intelligence import (
    calculate_business_intelligence,
)
from modules.business_intelligence.category_output import (
    CATEGORY_OUTPUT_FIELDS,
)
from modules.executive_summary import (
    generate_summary,
)


class BusinessIntelligenceEngineTest(unittest.TestCase):

    def test_every_category_returns_shared_contract(self):
        assessment = calculate_business_intelligence(
            _sample_company(),
            _sample_competitors(),
            {"estimated_loss": 135250, "review_gap": 270.5},
        )

        for category_output in assessment["category_scores"].values():
            for field in CATEGORY_OUTPUT_FIELDS:
                self.assertIn(field, category_output)

            self.assertTrue(category_output["explanation"])

    def test_three_scores_are_independent(self):
        assessment = calculate_business_intelligence(
            _sample_company(),
            _sample_competitors(),
            {"estimated_loss": 135250, "review_gap": 270.5},
        )

        self.assertIn("business_intelligence_score", assessment)
        self.assertIn("revenue_opportunity_score", assessment)
        self.assertIn("priority_score", assessment)
        self.assertNotEqual(
            assessment["business_intelligence_score"],
            assessment["revenue_opportunity_score"],
        )

    def test_missing_data_reduces_confidence_not_health(self):
        company = {
            "company_name": "Healthy Operator",
            "rating": 4.9,
            "review_count": 225,
            "missed_calls": False,
            "quote_delay": False,
            "poor_communication": False,
            "late_technicians": False,
        }
        competitors = [
            {"name": "Smaller Competitor", "rating": 4.5, "review_count": 80},
        ]

        assessment = calculate_business_intelligence(company, competitors)
        digital_presence = assessment["category_scores"]["digital_presence"]

        self.assertEqual(digital_presence["score"], 100)
        self.assertLess(digital_presence["confidence"], 100)
        self.assertEqual(assessment["business_intelligence_score"], 100)
        self.assertLess(assessment["assessment_confidence"], 100)

    def test_recommended_services_include_required_metadata(self):
        assessment = calculate_business_intelligence(
            _sample_company(),
            _sample_competitors(),
            {"estimated_loss": 135250, "review_gap": 270.5},
        )

        self.assertTrue(assessment["recommended_services"])

        for service in assessment["recommended_services"]:
            self.assertIn("estimated_business_impact", service)
            self.assertIn("estimated_revenue_improvement", service)
            self.assertIn("implementation_difficulty", service)
            self.assertIn("estimated_implementation_time", service)

    def test_summary_preserves_existing_entrypoint(self):
        summary = generate_summary("abc_gates")

        self.assertIn("business_intelligence_assessment", summary)
        self.assertIn("business_intelligence_score", summary)
        self.assertIn("business_grade", summary)
        self.assertIn("revenue_opportunity_score", summary)
        self.assertIn("priority_score", summary)
        self.assertIn("assessment_confidence", summary)


def _sample_company():
    return {
        "company_name": "ABC Gates & Fencing",
        "city": "Sacramento",
        "state": "CA",
        "rating": 3.8,
        "review_count": 43,
        "missed_calls": True,
        "quote_delay": True,
        "poor_communication": True,
        "late_technicians": True,
        "estimated_revenue": 450000,
    }


def _sample_competitors():
    return [
        {
            "name": "Elite Gates & Security",
            "rating": 4.9,
            "review_count": 386,
        },
        {
            "name": "California Fence & Gates",
            "rating": 4.8,
            "review_count": 241,
        },
    ]


if __name__ == "__main__":
    unittest.main()
