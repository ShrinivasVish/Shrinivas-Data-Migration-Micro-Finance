# main.py

import pandas as pd
from extraction.mongo_extractor import MongoExtractor
from loading.postgres_loader import PostgresLoader
from transformation.transformer import Transformer

from config import (
    unique_id_mapping,
    fixed_date_ist,
    collections_with_date_keys,
    collections,
)


def main():
    # 1. Create objects of Extractor, Transformer, and PostgresLoader
    mongo_extractor = MongoExtractor()
    postgres_loader = PostgresLoader()
    transformer = Transformer()

    # 2. Extract all the collections as DataFrames

    dataframes = {
        collection: mongo_extractor.load_collection_as_dataframe(collection)
        for collection in collections
    }

    # 3. Replace pd.NaT with None in the specified columns of each collection
    transformer.replace_nat_with_none(dataframes, collections_with_date_keys)

    # 4. Run MongoDB aggregation to add timestamps
    transformer.add_ist_timestamp_fields_mongodb_aggregation(collections)

    # FULL LOAD
    # 5. Load that data into the PostgreSQL database tables
    for collection, df in dataframes.items():
        postgres_loader.load_dataframe_to_postgres(
            df, unique_id_mapping[collection]["table_name"]
        )

    # 6. Execute the normalization function for loan restructuring
    transformer.normalize_loan_restructuring()

    # 7. Insert a new document into the customers collection
    new_customer = {
        "customer_id": 311001854123,
        "first_name": "Iris",
        "last_name": "Stuckley",
        "gender": "Female",
        "age": 45,
        "employment_status": "freelancer",
        "income_level": "low",
        "location": "San Francisco",
        "joined_date": "2018-10-04T05:30:00+00:00",
    }

    # 8. Insert the new document into the customers collection
    mongo_extractor.insert_document(
        "customers", collections_with_date_keys["customers"], new_customer
    )

    # Incremental Load: #1
    # 9. Load this new document to the corresponding PostgreSQL database table
    postgres_loader.load_dataframe_to_postgres(
        pd.DataFrame([new_customer]), "tbl_customers"
    )

    # 01. Execute the normalization function for loan restructuring
    transformer.normalize_loan_restructuring()

    # 11. Insert another new document into the customers collection
    another_customer = {
        "customer_id": 233361086626,
        "first_name": "Francyne",
        "last_name": "Guerra",
        "gender": "Female",
        "age": 42,
        "employment_status": "entrepreneur",
        "income_level": "low",
        "location": "Denver",
        "joined_date": "2021-07-08T05:30:00+00:00",
    }

    # 12. Insert the new document into the customers collection
    mongo_extractor.insert_document(
        "customers", collections_with_date_keys["customers"], another_customer
    )

    # Incremental Load: #2
    # 13. Load this new document to the corresponding PostgreSQL database table
    postgres_loader.load_dataframe_to_postgres(
        pd.DataFrame([another_customer]), "tbl_customers"
    )

    # 14. Assigning tnewer values to a document that already exists in the collection
    updated_customer = {
        "customer_id": 311001854123,
        "first_name": "Ada",
        "last_name": "Shelby",
        "gender": "Female",
        "age": 32,
        "employment_status": "politician",
        "income_level": "low",
        "location": "Birmingham",
        "joined_date": "2018-10-04T05:30:00+00:00",
    }

    # 15. Update the document in the customers collection
    mongo_extractor.update_document(
        "customers",
        collections_with_date_keys["customers"],
        updated_customer[unique_id_mapping["customers"]["unique_id_key_col"]],
        updated_customer,
    )

    # Incremental Load: #3
    # 16. Load this updated document to the corresponding PostgreSQL database table
    postgres_loader.update_record_in_postgres(
        pd.Series(updated_customer),
        "tbl_customers",
        unique_id_mapping["customers"]["unique_id_key_col"],
    )

    transformer.normalize_loan_restructuring()


if __name__ == "__main__":
    main()
