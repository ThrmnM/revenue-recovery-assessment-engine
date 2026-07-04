import json


def calculate_revenue_recovery_score(company):
    score = 100

    if company["missed_calls"]:
        score -= 15

    if company["quote_delay"]:
        score -= 10

    if company["poor_communication"]:
        score -= 10

    if company["late_technicians"]:
        score -= 5

    rating_penalty = max(0, (5 - company["rating"]) * 10)
    score -= rating_penalty

    return max(0, int(score))


def calculate_competitive_advantage_score(company):
    score = 100

    score -= int((5 - company["rating"]) * 15)

    if company["review_count"] < 50:
        score -= 20
    elif company["review_count"] < 100:
        score -= 10

    return max(0, score)


def calculate_automation_maturity_score(company):
    score = 100

    if company["missed_calls"]:
        score -= 25

    if company["quote_delay"]:
        score -= 25

    if company["poor_communication"]:
        score -= 25

    if company["late_technicians"]:
        score -= 10

    return max(0, score)


def calculate_business_opportunity_score(rr_score):
    return 100 - rr_score


if __name__ == "__main__":

    with open("data/companies/abc_gates.json") as f:
        company = json.load(f)

    revenue_score = calculate_revenue_recovery_score(company)
    competitive_score = calculate_competitive_advantage_score(company)
    automation_score = calculate_automation_maturity_score(company)
    opportunity_score = calculate_business_opportunity_score(
        revenue_score
    )

    print()
    print("Revenue Recovery Assessment")
    print("--------------------------------")
    print(f"Revenue Recovery Score: {revenue_score}/100")
    print(f"Competitive Advantage Score: {competitive_score}/100")
    print(f"Automation Maturity Score: {automation_score}/100")
    print(f"Business Opportunity Score: {opportunity_score}/100")
