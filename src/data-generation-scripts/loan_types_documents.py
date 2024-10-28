import json

# Possible values for loan_type_name and repayment_period
loan_type_names = ["Micro Loan", "Personal Loan", "Business Loan", "Housing Loan", "Education Loan", "Emergency Loan", "Consumer Loan"]
repayment_periods_in_months = [6, 12, 18, 24]

# Interest rates and max loan amounts for each loan type
loan_type_details = {
    "Micro Loan": {
        "max_loan_amount": 1500,  # Increased max amount for microloans
        "interest_rate": 5,        # Competitive interest rate
        "repayment_period_in_months": 6  # Common repayment period
    },
    "Personal Loan": {
        "max_loan_amount": 3000,   # Reasonable amount for personal loans
        "interest_rate": 8,         # Slightly higher interest rate
        "repayment_period_in_months": 12  # Standard repayment period
    },
    "Business Loan": {
        "max_loan_amount": 20000,   # Higher limit for business needs
        "interest_rate": 10,         # Typical interest rate for business loans
        "repayment_period_in_months": 24  # Longer repayment period for businesses
    },
    "Housing Loan": {
        "max_loan_amount": 25000,   # Sufficient for housing projects
        "interest_rate": 6,          # Competitive rate for housing loans
        "repayment_period_in_months": 36  # Longer term suitable for housing
    },
    "Education Loan": {
        "max_loan_amount": 10000,   # Adequate amount for education expenses
        "interest_rate": 7,          # Reasonable interest rate for education loans
        "repayment_period_in_months": 24  # Standard repayment period for education loans
    },
    "Emergency Loan": {
        "max_loan_amount": 5000,     # Sufficient for emergency needs
        "interest_rate": 9,           # Higher rate due to urgency
        "repayment_period_in_months": 12  # Shorter repayment period for emergencies
    },
    "Consumer Loan": {
        "max_loan_amount": 4000,     # Reasonable amount for consumer goods
        "interest_rate": 8.5,         # Competitive rate for consumer loans
        "repayment_period_in_months": 18  # Standard repayment period for consumer loans
    }
}

# Eligibility criteria (for simplicity, we'll use one common criterion for now)
eligibility_criteria = "Minimum income $500/month"

# Generate the loan_types documents
loan_types = []
loan_type_id = 1

for loan_type in loan_type_names:
    interest_rate_increment = 0
    loan_sub_type_id = 1
    for period in repayment_periods_in_months:
        loan_types.append({
            "loan_type_id": int(f"{loan_type_id}{loan_sub_type_id}"),
            "loan_type_name": loan_type,
            "max_loan_amount": loan_type_details[loan_type]["max_loan_amount"],
            "interest_rate": loan_type_details[loan_type]["interest_rate"] + interest_rate_increment,
            "repayment_period_in_months": period,
            "eligibility_criteria": eligibility_criteria
        })
        loan_sub_type_id += 1
        interest_rate_increment += 1
    loan_type_id += 1

# Write the data to a JSON file
loan_types_json = json.dumps(loan_types, indent=4)
output_path = "../../data/loan_types.json"
with open(output_path, "w") as f:
    f.write(loan_types_json)
