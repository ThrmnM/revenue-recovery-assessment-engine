import json
import os
import matplotlib.pyplot as plt

from scoring_engine import (
    calculate_revenue_recovery_score
)


def create_score_chart():

    with open(
        "data/companies/abc_gates.json"
    ) as f:
        company = json.load(f)

    prospect_score = (
        calculate_revenue_recovery_score(
            company
        )
    )

    competitor_average = 87

    labels = [
        company["company_name"],
        "Competitor Average"
    ]

    scores = [
        prospect_score,
        competitor_average
    ]

    plt.figure(figsize=(8, 5))

    bars = plt.bar(labels, scores)

    plt.title(
        "Revenue Recovery Score Comparison"
    )

    plt.ylabel("Score")

    plt.ylim(0, 100)

    for bar in bars:
        height = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            height + 2,
            str(height),
            ha="center"
        )

    os.makedirs(
        "assets/charts",
        exist_ok=True
    )

    plt.tight_layout()

    filename = (
        "assets/charts/"
        "revenue_score_comparison.png"
    )

    plt.savefig(filename)

    print()
    print("Chart saved:")
    print(filename)


if __name__ == "__main__":
    create_score_chart()
