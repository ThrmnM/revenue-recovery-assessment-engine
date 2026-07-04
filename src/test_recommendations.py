from modules.data_loader import load_company
from modules.executive_summary import generate_summary
from modules.recommendation_engine import (
    generate_recommendations
)

company = load_company("abc_gates")
summary = generate_summary("abc_gates")

scores = {
    "automation_score":
        summary["automation_score"]
}

results = generate_recommendations(
    company,
    scores
)

print()
print("Recommendation Engine")
print("--------------------------------")
print()

print("Problems Identified:")
for problem in results["problems"]:
    print(f"- {problem}")

print()
print("Recommendations:")

for rec in results["recommendations"]:
    print()
    print(
        f"Solution: {rec['solution']}"
    )
    print(
        f"Benefit: {rec['benefit']}"
    )
    print(
        f"Estimated Recovery: "
        f"${rec['estimated_recovery']:,}"
    )

print()
print(
    f"Total Estimated Recovery: "
    f"${results['estimated_recovery']:,}+"
)

print()
print("90-Day Plan")

for step in results[
    "ninety_day_plan"
]:
    print(f"- {step}")
