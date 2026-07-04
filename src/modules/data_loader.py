import json


def load_company(company_id):
    filepath = f"data/companies/{company_id}.json"

    with open(filepath) as f:
        return json.load(f)


def load_competitors(company_id):
    filepath = (
        f"data/competitors/"
        f"{company_id}_competitors.json"
    )

    with open(filepath) as f:
        data = json.load(f)

    return data["competitors"]
