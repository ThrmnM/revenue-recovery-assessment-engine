import matplotlib.pyplot as plt
import os


def create_score_chart():
    labels = [
        "Revenue Recovery",
        "Competitor Average"
    ]

    scores = [48, 87]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, scores)

    plt.title("Revenue Recovery Score Comparison")
    plt.ylabel("Score")
    plt.ylim(0, 100)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            str(height),
            ha="center"
        )

    os.makedirs(
        "assets/charts",
        exist_ok=True
    )

    plt.tight_layout()

    plt.savefig(
        "assets/charts/revenue_score_comparison.png"
    )

    print()
    print(
        "Chart saved:"
    )
    print(
        "assets/charts/revenue_score_comparison.png"
    )


if __name__ == "__main__":
    create_score_chart()
