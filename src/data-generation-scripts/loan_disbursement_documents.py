import json
import random
from datetime import datetime
from pathlib import Path

# Load loan applications data
with open("../../data/loan_applications.json") as f:
    loan_applications = json.load(f)

# Possible disbursement methods
disbursement_methods = [
    "Bank Transfer", 
    "Check", 
    "Cash", 
    "Mobile Payment", 
    "Online Transfer"
]

# Function to generate a unique 12-digit disbursement ID
def generate_disbursement_id():
    return random.randint(100000000000000000, 999999999999999999)

# List to hold loan disbursement documents
loan_disbursement_documents = []

# Create loan disbursement documents only for approved loans
for application in loan_applications:
    if application['loan_status'] == 'Approved':
        disbursement_document = {
            "disbursement_id": generate_disbursement_id(),
            "loan_id": application['loan_id'],
            "disbursement_amount": application['loan_amount'],
            "disbursement_date": application['approval_date'],  # Approval date as disbursement date
            "disbursement_method": random.choice(disbursement_methods)  # Randomly select a method
        }
        loan_disbursement_documents.append(disbursement_document)

# Save the loan disbursement documents to a JSON file
with open('../../data/loan_disbursement.json', 'w') as outfile:
    json.dump(loan_disbursement_documents, outfile, indent=4)

print(f"{len(loan_disbursement_documents)} loan disbursement documents created.")
