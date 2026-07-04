from modules.executive_summary import (
    generate_summary
)

summary = generate_summary(
    "abc_gates"
)

print()
print("══════════════════════════════════════")
print("            KEY FINDINGS")
print("══════════════════════════════════════")
print()

for key, value in summary[
    "metrics"
].items():

    print("┌──────────────────────────────┐")
    print(f"│ {key:<28} │")
    print(f"│ {value:<28} │")
    print("└──────────────────────────────┘")
    print()

print("══════════════════════════════════════")
print("         TOP COMPETITOR")
print("══════════════════════════════════════")
print()

competitor = summary[
    "top_competitor"
]

print(
    f"Name: {competitor['name']}"
)
print(
    f"Rating: {competitor['rating']} ★"
)
print(
    f"Reviews: {competitor['review_count']}"
)

print()

print("══════════════════════════════════════")
print("          MARKET POSITION")
print("══════════════════════════════════════")
print()

position = summary[
    "market_position"
]

print(
    f"Rank: #{position['rank']} "
    f"of {position['total']}"
)

print(
    f"Standing: "
    f"{position['standing']}"
)

print()

print("══════════════════════════════════════")
print("    LOCAL VISIBILITY ASSESSMENT")
print("══════════════════════════════════════")
print()

visibility = summary[
    "visibility_assessment"
]

print(
    f"Estimated Search Visibility: "
    f"{visibility['search_visibility']}"
)

print(
    f"Likely Discovery Method: "
    f"{visibility['discovery_method']}"
)

print(
    f"Potential New Customer Loss: "
    f"{visibility['customer_loss']}"
)

print(
    f"Estimated Lead Distribution:"
)
print(
    visibility['caller_ratio']
)

print()

print("══════════════════════════════════════")
print("          ATTENTION ALERT")
print("══════════════════════════════════════")
print()

print(
    summary["attention_alert"]
)

print()

print(
    "Recommended Action:"
)

print(
    summary["recommended_action"]
)

print()
print(
    summary["narrative"]
)
