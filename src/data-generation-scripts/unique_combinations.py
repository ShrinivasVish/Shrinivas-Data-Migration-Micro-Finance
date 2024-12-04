import json

# Global lists for new loan terms
interest_rates = [3, 4, 5, 6]
repayment_periods = [36, 48, 60, 72]

# Global lists for restructure terms
restructure_reasons = [
    "Financial difficulties",
    "Interest rate reduction",
    "Change in income",
    "Unexpected expenses",
]
new_schedules = ["Monthly payments", "Bi-weekly payments", "Quarterly payments"]
concessions = [
    "2-month grace period",
    "No late fees for 3 months",
    "Payment deferral for 1 month",
]

new_loan_terms_id = 1
restructure_term_id = 1

unique_combinations__new_loan_terms = []
unique_combinations__restructure_terms = []

for interest_rate in interest_rates:
    for repayment_period in repayment_periods:
        doc = {
            "new_loan_term_id": new_loan_terms_id,
            "interest_rate": interest_rate,
            "repayment_period_in_months": repayment_period,
        }
        unique_combinations__new_loan_terms.append(doc)
        new_loan_terms_id += 1


for reason in restructure_reasons:
    for new_schedule in new_schedules:
        for concession in concessions:
            doc = {
                "restructure_term_id": restructure_term_id,
                "reason": reason,
                "new_schedule": new_schedule,
                "concessions": concession,
            }
            unique_combinations__restructure_terms.append(doc)
            restructure_term_id += 1

# Write the data to a JSON file
combinations__new_loan_terms_json = json.dumps(
    unique_combinations__new_loan_terms, indent=4
)
output_path = "../../data/new_loan_terms.json"
with open(output_path, "w") as f:
    f.write(combinations__new_loan_terms_json)


# Write the data to a JSON file
combinations__restructure_terms_json = json.dumps(
    unique_combinations__restructure_terms, indent=4
)
output_path = "../../data/restructure_terms.json"
with open(output_path, "w") as f:
    f.write(combinations__restructure_terms_json)
