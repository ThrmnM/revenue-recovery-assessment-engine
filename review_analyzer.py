with open("reviews.txt", "r") as file:
    reviews = file.readlines()

categories = {
    "missed_calls": [
        "answered",
        "callback",
        "phone"
    ],
    "late_technician": [
        "late",
        "hours"
    ],
    "quote_delay": [
        "quote"
    ],
    "communication": [
        "communication"
    ]
}

results = {
    "missed_calls": 0,
    "late_technician": 0,
    "quote_delay": 0,
    "communication": 0
}

for review in reviews:
    review_lower = review.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in review_lower:
                results[category] += 1
                break

print("\nRevenue Recovery Assessment\n")
print("--------------------------------")

for category, count in results.items():
    print(f"{category}: {count}")

total_issues = sum(results.values())

print("\n--------------------------------")

if total_issues == 0:
    score = 100
else:
    score = max(100 - (total_issues * 10), 0)

print(f"Revenue Recovery Score: {score}/100")

recommendations = []

if results["missed_calls"] > 0:
    recommendations.append(
        "- Install AI Receptionist and Missed-Call Text Back automation."
    )

if results["late_technician"] > 0:
    recommendations.append(
        "- Implement technician route scheduling and ETA notifications."
    )

if results["quote_delay"] > 0:
    recommendations.append(
        "- Set up automated quote reminders and follow-up sequences."
    )

if results["communication"] > 0:
    recommendations.append(
        "- Introduce customer communication workflows and status updates."
    )

print("\nRecommendations")
print("--------------------------------")

if recommendations:
    for recommendation in recommendations:
        print(recommendation)
else:
    print("No major operational issues detected.")