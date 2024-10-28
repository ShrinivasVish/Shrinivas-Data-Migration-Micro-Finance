import json
import random

# Load necessary .json files
with open("../../data/loan_applications.json", "r") as f:
    loan_applications = json.load(f)

with open("../../data/loan_repayments.json", "r") as f:
    loan_repayments = json.load(f)


# Helper function to generate a unique 18-digit numeric repayment_id
def generate_repayment_id():
    return random.randint(100000000000000000, 999999999999999999)


# List to hold generated customer loan history records
loan_history = []

# Process loan applications to create loan history records
for application in loan_applications:
    loan_id = application["loan_id"]
    customer_id = application["customer_id"]
    approval_date = application["approval_date"]

    # Check loan repayments for this loan_id
    repayments = [
        repayment for repayment in loan_repayments if repayment["loan_id"] == loan_id
    ]

    # Determine if all installments are fully paid
    all_paid = all(repayment["repayment_status"] == "paid" for repayment in repayments)

    # Get loan disbursed date (set to approval date)
    loan_disbursed_date = approval_date

    # Get loan repaid date (if applicable)
    loan_repaid_date = None

    # Condition 1: Loan must have repayments
    if repayments:
        # Condition 2: All repayments must be fully paid
        if all_paid:
            # Set loan_repaid_date to the latest repayment date if all installments are paid
            loan_repaid_date = max(
                repayment["repayment_date"] for repayment in repayments
            )
        else:
            # If any repayment status is not 'paid', loan_repaid_date remains None
            loan_repaid_date = None
    else:
        # If there are no repayments for the loan, loan_repaid_date remains None
        loan_repaid_date = None

    # Create the customer loan history record
    history_record = {
        "history_id": generate_repayment_id(),
        "customer_id": customer_id,
        "loan_id": loan_id,
        "previous_loan_status": all_paid,
        "loan_disbursed_date": loan_disbursed_date,
        "loan_repaid_date": loan_repaid_date,
    }

    # Add record to the list
    loan_history.append(history_record)

# Write the customer loan history data to JSON file
with open("../../data/loan_history.json", "w") as f:
    json.dump(loan_history, f, indent=4)

print(
    f"{len(loan_history)} customer loan history records generated and written to loan_history.json."
)
