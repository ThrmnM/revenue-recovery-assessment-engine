import json

# Load company
with open("data/companies/abc_gates.json") as f:
    company = json.load(f)

# Load competitors
with open("data/competitors/abc_gates_competitors.json") as f:
    competitors = json.load(f)

print("\nCompetitor Analysis")
print("--------------------------------")

company_reviews = company["review_count"]
company_rating = company["rating"]

for competitor in competitors["competitors"]:

    review_gap = (
        competitor["review_count"]
        - company_reviews
    )

    rating_gap = (
        competitor["rating"]
        - company_rating
    )

    print(f"\n{competitor['name']}")
    print(
        f"Reviews: {competitor['review_count']}"
    )
    print(
        f"Rating: {competitor['rating']}"
    )

    print(f"Review Gap: {review_gap}")
    print(
        f"Rating Gap: {rating_gap:.1f}"
    )

    if review_gap > 50:
        print(
            "⚠️ Major review advantage."
        )

    if rating_gap > 0.2:
        print(
            "⚠️ Stronger online reputation."
        )

    estimated_revenue_loss = (
    review_gap * 500
    )

    print(
    f"Estimated Revenue Opportunity: "
    f"${estimated_revenue_loss:,.0f}+ annually"
    )

    print("\nCompetitive Strengths:")

    for strength in competitor["strengths"]:
        print(f"- {strength}")


