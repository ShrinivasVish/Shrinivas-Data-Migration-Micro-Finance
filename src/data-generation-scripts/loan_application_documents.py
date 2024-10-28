"""
- This script is to generate the documents for the loan_applications collection. 


- There are a few things we need to consider when creating documents which are specified as follows:

    - Not all the customers from the customers collection will have a load registered. 
      Hence, we're only creating the documents for only the 70% of the customers i.e., 3,500 loan applications.
    
    - But the number of loan applications can exceed than the no. of loan applicants as 1 applicant can have multiple loans.

    
- Our approach is going to be as follows:

    - Step 1: Select 5% to 10% of customers to have multiple loans
    
    - Step 2: Assign multiple loans to the selected customers
    
    - Step 3: Fill the remaining applications randomly for the rest of the customers. 
      While we're executing currect step, there's a possibility that the appicants from the previous subset can also be selected this time as well, due to the randomness of the selection. 

"""


# # ------------------------------------------------------------------

# ---------------------------
# Import necessary libraries
import json
import random
from datetime import datetime, timedelta

# ---------------------------
# Load necessary .json files

# Load customers and loan_types data from JSON files
with open('../../data/customers.json', 'r') as f:
    customers = json.load(f)

with open('../../data/loan_types.json', 'r') as f:
    loan_types = json.load(f)

# ------------------------------------------------------------------
# Define helper functions and fixed values for common data generation

# Generate a random date between two dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Generate a random loan ID (8-digit numeric)
def generate_loan_id():
    return random.randint(100000000000000000, 999999999999999999)

# Loan status options
loan_status_options = ["Pending", "Approved", "Rejected", "Disbursed"]

# Date range for application_date
start_date = datetime.strptime("2018-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-09-30", "%Y-%m-%d")

# List to hold generated loan applications
loan_applications = []

# Step 1: Select 70% of customers to apply for loans
total_customers = len(customers)
loan_applicant_percentage = 0.7
num_customers_with_loans = int(total_customers * loan_applicant_percentage)

# Randomly select customers who will apply for loans
customers_with_loans = random.sample(customers, num_customers_with_loans)

# Step 2: Select 15% of customers (from those applying for loans) to have multiple loans
multiple_loan_percentage = 0.15 
num_customers_with_multiple_loans = int(num_customers_with_loans * multiple_loan_percentage)

# Randomly select customers who will have multiple loans
customers_with_multiple_loans = random.sample(customers_with_loans, num_customers_with_multiple_loans)

# Step 3: Dictionary to hold loan_ids applied by each customer
customer_loans = {}

# Step 4: Assign loans to selected customers and generate loan applications
for customer in customers_with_loans:
    num_loans = 1  # Default is 1 loan
    
    # If the customer is in the selected multiple loans group, assign multiple loans
    if customer in customers_with_multiple_loans:
        num_loans = random.randint(2, 5)  # Between 2 to 5 loans
    
    # Generate loan applications for this customer
    for _ in range(num_loans):
        # Randomly select a loan_type
        loan_type = random.choice(loan_types)
        
        # Generate a loan_id
        loan_id = generate_loan_id()
        
        # Set customer_id and loan_type_id
        customer_id = customer['customer_id']
        loan_type_id = loan_type['loan_type_id']
        
        # Generate a loan_amount that is less than the max_loan_amount of the selected loan type
        max_loan_amount = loan_type['max_loan_amount']
        loan_amount = round(random.uniform(100, max_loan_amount), 2)
        
        # Randomly select a loan_status
        loan_status = random.choice(loan_status_options)
        
        # Generate application_date
        application_date = random_date(start_date, end_date)
        
        # If loan_status is "Approved", set an approval_date after the application_date
        if loan_status == "Approved":
            approval_date = random_date(application_date, end_date)
        else:
            approval_date = None
        
        # Create the loan application document
        loan_application = {
            "loan_id": loan_id,
            "customer_id": customer_id,
            "loan_type_id": loan_type_id,
            "loan_amount": loan_amount,
            "loan_status": loan_status,
            "application_date": application_date.strftime("%Y-%m-%d"),
            "approval_date": approval_date.strftime("%Y-%m-%d") if approval_date else None
        }
        
        # Add the document to the loan_applications list
        loan_applications.append(loan_application)
        
        # Update customer_loans dictionary to add the loan_id to the customer's list of loans
        if customer_id in customer_loans:
            customer_loans[customer_id].append(loan_id)
        else:
            customer_loans[customer_id] = [loan_id]

# Step 5: Update customers data by adding the `loans_applied` field
for customer in customers:
    customer_id = customer['customer_id']
    
    # If the customer has applied for loans, add the loan_ids under `loans_applied`
    if customer_id in customer_loans:
        customer['loans_applied'] = customer_loans[customer_id]
    else:
        customer['loans_applied'] = []  # No loans applied

# Step 6: Write the loan applications and updated customers data to JSON files

with open('../../data/loan_applications.json', 'w') as f:
    json.dump(loan_applications, f, indent=4)

with open('../../data/customers_with_loans.json', 'w') as f:
    json.dump(customers, f, indent=4)

print(f"{len(loan_applications)} loan applications generated and written to loan_applications.json.")
print(f"{len(customers)} customers processed, customers_with_loans.json file created.")
