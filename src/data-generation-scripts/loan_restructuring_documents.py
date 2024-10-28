import json
import random

# Load necessary .json files
with open('../../data/loan_applications.json', 'r') as f:
    loan_applications = json.load(f)

# Function to generate a unique 8-digit restructuring ID
def generate_restructuring_id():
    return random.randint(100000000000000000, 999999999999999999)

# Global lists for new loan terms
interest_rates = [3, 4, 5, 6]
repayment_periods = [36, 48, 60, 72]

# Global lists for restructure terms
restructure_reasons = ["Financial difficulties", "Interest rate reduction", "Change in income", "Unexpected expenses"]
new_schedules = ["Monthly payments", "Bi-weekly payments", "Quarterly payments"]
concessions = ["2-month grace period", "No late fees for 3 months", "Payment deferral for 1 month"]

# List to hold generated restructuring records
loan_restructuring = []

# Process loan applications to create restructuring records
for application in loan_applications:
    if application['loan_status'] == 'Approved':
        loan_id = application['loan_id']
        
        # Select unique random values from the global lists
        new_loan_terms = {
            "interest_rate": random.choice(interest_rates),
            "repayment_period_in_months": random.choice(repayment_periods)
        }
        
        restructure_terms = {
            "reason": random.choice(restructure_reasons),
            "new_schedule": random.choice(new_schedules),
            "concessions": random.choice(concessions)
        }
        
        # Create the restructuring record
        restructuring_record = {
            "restructuring_id": generate_restructuring_id(),
            "loan_id": loan_id,
            "new_loan_terms": new_loan_terms,
            "restructure_terms": restructure_terms
        }

        # Add the record to the list
        loan_restructuring.append(restructuring_record)

# Step 5: Write the loan restructuring data to JSON file
with open('../../data/loan_restructuring_new.json', 'w') as f:
    json.dump(loan_restructuring, f, indent=4)

print(f"{len(loan_restructuring)} loan restructuring records generated and written to loan_restructuring.json.")
