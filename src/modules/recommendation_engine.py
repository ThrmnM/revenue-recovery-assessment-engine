def generate_recommendations(
    company,
    scores,
    competitor_analysis=None
):
    """
    Generates recommendations based on
    company data and scoring metrics.
    """

    recommendations = []
    problems = []
    priority_actions = []
    estimated_recovery = 0

    # Missed Calls
    if company.get("missed_calls"):

        problems.append(
            "Missed inbound calls are causing lost leads."
        )

        recommendations.append({
            "solution":
                "AI Receptionist and Missed Call Text Back",
            "benefit":
                "Capture leads that would otherwise be lost.",
            "estimated_recovery":
                35000,
            "priority":
                1
        })

        estimated_recovery += 35000

    # Poor Communication
    if company.get("poor_communication"):

        problems.append(
            "Poor customer communication is damaging reputation."
        )

        recommendations.append({
            "solution":
                "Customer Communication Automation",
            "benefit":
                "Improve response times and customer satisfaction.",
            "estimated_recovery":
                25000,
            "priority":
                2
        })

        estimated_recovery += 25000

    # Quote Delays
    if company.get("quote_delay"):

        problems.append(
            "Slow quotes are reducing conversion rates."
        )

        recommendations.append({
            "solution":
                "Automated Quote Follow-Up System",
            "benefit":
                "Increase quote conversions and reduce lead leakage.",
            "estimated_recovery":
                30000,
            "priority":
                2
        })

        estimated_recovery += 30000

    # Technician Issues
    if company.get("late_technicians"):

        problems.append(
            "Late technicians are negatively affecting reviews."
        )

        recommendations.append({
            "solution":
                "Technician Scheduling and ETA Notifications",
            "benefit":
                "Improve customer experience and online reviews.",
            "estimated_recovery":
                20000,
            "priority":
                3
        })

        estimated_recovery += 20000

    # Low Automation Score
    if scores["automation_score"] < 30:

        recommendations.append({
            "solution":
                "CRM and Business Process Automation",
            "benefit":
                "Create scalable systems and improve efficiency.",
            "estimated_recovery":
                40000,
            "priority":
                1
        })

        estimated_recovery += 40000

    # Sort recommendations
    recommendations = sorted(
        recommendations,
        key=lambda x: x["priority"]
    )

    # Priority actions list
    priority_actions = [
        r["solution"]
        for r in recommendations
    ]

    # 90-Day Plan
    ninety_day_plan = [
        "Days 1-30: Deploy AI Receptionist and Communication Systems.",
        "Days 31-60: Implement Review and Quote Automation.",
        "Days 61-90: Optimize workflows and scale lead generation."
    ]

    return {
        "problems": problems,
        "recommendations": recommendations,
        "priority_actions": priority_actions,
        "estimated_recovery": estimated_recovery,
        "ninety_day_plan": ninety_day_plan
    }
