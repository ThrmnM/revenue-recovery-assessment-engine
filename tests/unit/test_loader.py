from modules.data_loader import (
    load_company,
    load_competitors,
)

company = load_company("abc_gates")
competitors = load_competitors("abc_gates")

print(company["company_name"])
print()

for competitor in competitors:
    print(competitor["name"])
