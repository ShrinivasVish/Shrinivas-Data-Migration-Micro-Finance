# config.py
from datetime import datetime, timedelta
import pytz

# Define unique ID mappings for collections and nested document info
unique_id_mapping = {
    "customers": {
        "unique_id_key_col": "customer_id",
        "table_name": "tbl_customers",
        "nested_documents": [],
    },
    "loan_types": {
        "unique_id_key_col": "loan_type_id",
        "table_name": "tbl_loan_types",
        "nested_documents": [],
    },
    "loan_applications": {
        "unique_id_key_col": "loan_id",
        "table_name": "tbl_loan_applications",
        "nested_documents": [],
    },
    "loan_repayments": {
        "unique_id_key_col": "repayment_id",
        "table_name": "tbl_loan_repayments",
        "nested_documents": [],
    },
    "loan_history": {
        "unique_id_key_col": "history_id",
        "table_name": "tbl_loan_history",
        "nested_documents": [],
    },
    "loan_collateral": {
        "unique_id_key_col": "collateral_id",
        "table_name": "tbl_loan_collateral",
        "nested_documents": [],
    },
    "loan_restructuring": {
        "unique_id_key_col": "restructuring_id",
        "table_name": "tbl_loan_restructuring",
        "nested_documents": ["new_loan_terms", "restructure_terms"],
    },
    "loan_disbursements": {
        "unique_id_key_col": "disbursement_id",
        "table_name": "tbl_loan_disbursements",
        "nested_documents": [],
    },
    "new_loan_terms": {
        "unique_id_key_col": "new_loan_term_id",
        "table_name": "tbl_new_loan_terms",
        "nested_documents": [],
    },
    "restructure_terms": {
        "unique_id_key_col": "restructure_term_id",
        "table_name": "tbl_restructure_terms",
        "nested_documents": [],
    },
}


# Define fixed IST date
def specific_ist_time():
    ist = pytz.timezone("Asia/Kolkata")
    fixed_date_utc = datetime(2024, 10, 27, 0, 0, 0)
    return fixed_date_utc.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")


fixed_date_ist = specific_ist_time()

# Collection date fields mapping
collections_with_date_keys = {
    "customers": ["joined_date"],
    "loan_types": [],
    "loan_applications": ["application_date", "approval_date"],
    "loan_repayments": ["repayment_date"],
    "loan_history": ["loan_disbursed_date", "loan_repaid_date"],
    "loan_collateral": [],
    "loan_restructuring": [],
    "loan_disbursements": ["disbursement_date", "application_date"],
    "new_loan_terms": [],
    "restructure_terms": [],
}

collections = list(collections_with_date_keys.keys())
