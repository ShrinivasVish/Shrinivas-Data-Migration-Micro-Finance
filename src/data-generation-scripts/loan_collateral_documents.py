import json
import random

# Load necessary .json files
with open('../../data/loan_applications.json', 'r') as f:
    loan_applications = json.load(f)

# Define collateral types and their respective value ratios
collateral_types_and_ratios = {
    "Property": 1.2,
    "Vehicle": 1.0,
    "Gold": 0.9,
    "Stocks/Bonds": 0.8,
    "Cash Deposit": 1.0,
    "Equipment": 0.7,
    "Inventory": 0.6,
    "Other": 0.5
}

# Function to generate a unique 8-digit collateral ID
def generate_collateral_id():
    return random.randint(100000000000000000, 999999999999999999)

# List to hold generated collateral records
loan_collateral = []

# Process loan applications to create collateral records
for application in loan_applications:
    if application['loan_status'] == 'Approved':
        loan_id = application['loan_id']
        loan_amount = application['loan_amount']

        # Randomly select a collateral type based on the loan amount
        collateral_type = random.choice(list(collateral_types_and_ratios.keys()))
        
        # Calculate collateral value based on the collateral type
        collateral_value = loan_amount * collateral_types_and_ratios[collateral_type]
        
        # Create the collateral record
        collateral_record = {
            "collateral_id": generate_collateral_id(),
            "loan_id": loan_id,
            "collateral_type": collateral_type,
            "collateral_value": round(collateral_value, 2)  # Round to two decimal places
        }

        # Add the record to the list
        loan_collateral.append(collateral_record)

# Step 5: Write the loan collateral data to JSON file
with open('../../data/loan_collateral.json', 'w') as f:
    json.dump(loan_collateral, f, indent=4)

print(f"{len(loan_collateral)} loan collateral records generated and written to loan_collateral.json.")
