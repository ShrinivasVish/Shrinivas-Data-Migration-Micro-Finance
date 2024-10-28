import json
import random
import re
from datetime import datetime, timedelta

# Load loan applications and loan types data from JSON files
with open('../../data/loan_applications.json', 'r') as f:
    loan_applications = json.load(f)

with open('../../data/loan_types.json', 'r') as f:
    loan_types = json.load(f)

# Helper function to generate a unique repayment_id
def generate_repayment_id():
    return random.randint(100000000000000000, 999999999999999999)


# List to hold generated loan repayment documents
loan_repayments = []

# Process each approved loan application to create loan repayment documents
for application in loan_applications:
    if application['loan_status'] == "Approved":
        loan_id = application['loan_id']
        loan_type_id = application['loan_type_id']

        # Find the corresponding loan type to get repayment details
        loan_type = next((lt for lt in loan_types if lt['loan_type_id'] == loan_type_id), None)
        
        if loan_type:
            max_loan_amount = application['loan_amount']
            interest_rate = loan_type['interest_rate']
            repayment_period = loan_type['repayment_period_in_months']

            # Calculate the monthly repayment amount
            monthly_interest_rate = interest_rate / 100 / 12
            principal_amount = max_loan_amount
            repayment_amount = (principal_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -repayment_period)

            # Set the repayment dates
            approval_date = datetime.strptime(application['approval_date'], "%Y-%m-%d")
            first_repayment_date = approval_date + timedelta(days=30)  # 1 month after approval

            # Generate repayment documents
            for month in range(repayment_period):
                repayment_date = (first_repayment_date + timedelta(days=30 * month)).strftime("%Y-%m-%d")
                repayment_status = random.choice(["Paid", "Partial", "Overdue", "Missed"])  # Randomly select repayment status

                loan_repayment = {
                    "repayment_id": generate_repayment_id(),
                    "loan_id": loan_id,
                    "repayment_amount": round(repayment_amount, 2),
                    "repayment_date": repayment_date,
                    "repayment_status": repayment_status
                }

                loan_repayments.append(loan_repayment)

# Step 5: Write the loan repayments data to a JSON file
with open('../../data/loan_repayments.json', 'w') as f:
    json.dump(loan_repayments, f, indent=4)

print(f"{len(loan_repayments)} loan repayment records generated and written to loan_repayments.json.")
