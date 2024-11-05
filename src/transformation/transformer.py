# normalizer.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, timedelta, timezone
import pandas as pd

from config import (
    unique_id_mapping,
    fixed_date_ist,
    collections_with_date_keys,
    collections,
)


class Transformer:
    def __init__(self):
        """
        Initializes the Normalizer class.
        Loads environment variables and sets up MongoDB and PostgreSQL connection parameters.
        """

        # Load environment variables from .env file
        load_dotenv()

        # MongoDB setup
        self.mongo_url = os.getenv("MONGO_DB_URL")
        self.mongo_db_database_name = os.getenv("MONGODB_DB_NAME")
        self.mongo_client = MongoClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_database_name]

        # PostgreSQL setup
        self.pg_host = os.getenv("PG_HOST")
        self.pg_database = os.getenv("PG_DATABASE")
        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")
        self.pg_port = os.getenv("PG_PORT")
        self.pg_connection = self.create_pg_connection()

    def create_pg_connection(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        return psycopg2.connect(
            host=self.pg_host,
            database=self.pg_database,
            user=self.pg_user,
            password=self.pg_password,
            port=self.pg_port,
        )

    # Supports `add_ist_timestamp_fields_mongodb_aggregation` method
    def specific_ist_time(self):
        """Sets and returns a specific date (27 October 2024) adjusted to IST (UTC+5:30)."""
        # Create the specified date in UTC and adjust to IST

        # Set the fixed UTC date for 27 October 2024 at midnight (00:00:00)
        fixed_date_utc = datetime(2024, 10, 27, 0, 0, tzinfo=timezone.utc)

        # Adjust to Indian Standard Time (UTC+5:30)
        fixed_date_ist = fixed_date_utc + timedelta(hours=5, minutes=30)
        return fixed_date_ist

    # Changes are refled in MONGODB COLLECTIONS
    def add_ist_timestamp_fields_mongodb_aggregation(self, collections_list):
        """
        Adds 'added_at' and 'modified_at' fields with specific IST-adjusted timestamp
        to all collections in the database using $addFields.
        """
        for collection_name in collections_list:
            collection = self.db[collection_name]
            pipeline = [
                {
                    "$set": {
                        "added_at": self.specific_ist_time(),
                        "modified_at": self.specific_ist_time(),
                    }
                }
            ]
            collection.update_many({}, pipeline[0])
            print(f"Updated collection '{collection_name}' with IST timestamps.")

    # Replace pd.NaT with None in the specified columns of each collection
    # Changes are reflected in PANDAS DF;
    # Post EXTRACTION, Pre Loading for smooth transition
    def replace_nat_with_none(self, collections_dict, columns_to_replace):
        """
        Replaces pd.NaT with None in the specified columns of each collection in collections_dict.

        Parameters:
        collections_dict (dict): Dictionary where keys are collection names and values are DataFrames.
        columns_to_replace (dict): Dictionary where keys are collection names and values are lists of columns
                                in which to replace pd.NaT with None.
        """
        for collection_name, columns in columns_to_replace.items():
            for column in columns:
                if column in collections_dict[collection_name].columns:
                    collections_dict[collection_name][column] = collections_dict[
                        collection_name
                    ][column].replace({pd.NaT: None})

    # Changes are refled in POSTGRESQL TABLE
    def normalize_loan_restructuring(self):
        """
        Populates `tbl_loan_restructuring_normalized` from `tbl_loan_restructuring` by
        linking foreign keys to `tbl_new_loan_terms` and `tbl_restructure_terms`.
        """
        with self.pg_connection.cursor() as cursor:
            cursor.execute(
                "SELECT restructuring_id, loan_id, new_loan_terms, restructure_terms, added_at, modified_at FROM tbl_loan_restructuring"
            )
            restructuring_records = cursor.fetchall()

            for record in restructuring_records:
                (
                    restructuring_id,
                    loan_id,
                    new_loan_terms,
                    restructure_terms,
                    added_at,
                    modified_at,
                ) = record

                # Insert or fetch new_loan_terms_id
                cursor.execute(
                    "SELECT new_loan_term_id FROM tbl_new_loan_terms WHERE interest_rate = %s AND repayment_period_in_months = %s",
                    (
                        new_loan_terms["interest_rate"],
                        new_loan_terms["repayment_period_in_months"],
                    ),
                )
                new_loan_terms_id = cursor.fetchone()
                if not new_loan_terms_id:
                    cursor.execute(
                        "INSERT INTO tbl_new_loan_terms (interest_rate, repayment_period_in_months) VALUES (%s, %s) RETURNING new_loan_term_id",
                        (
                            new_loan_terms["interest_rate"],
                            new_loan_terms["repayment_period_in_months"],
                        ),
                    )
                    new_loan_terms_id = cursor.fetchone()[0]

                # Insert or fetch restructure_terms_id
                cursor.execute(
                    "SELECT restructure_term_id FROM tbl_restructure_terms WHERE reason = %s AND new_schedule = %s AND concessions = %s",
                    (
                        restructure_terms["reason"],
                        restructure_terms["new_schedule"],
                        restructure_terms["concessions"],
                    ),
                )
                restructure_terms_id = cursor.fetchone()
                if not restructure_terms_id:
                    cursor.execute(
                        "INSERT INTO tbl_restructure_terms (reason, new_schedule, concessions) VALUES (%s, %s, %s) RETURNING restructure_term_id",
                        (
                            restructure_terms["reason"],
                            restructure_terms["new_schedule"],
                            restructure_terms["concessions"],
                        ),
                    )
                    restructure_terms_id = cursor.fetchone()[0]

                # Insert or update tbl_loan_restructuring_normalized
                cursor.execute(
                    """
                    INSERT INTO tbl_loan_restructuring_normalized (
                        restructuring_id, loan_id, new_loan_term_id, restructure_term_id, added_at, modified_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (restructuring_id) DO UPDATE 
                    SET new_loan_term_id = EXCLUDED.new_loan_term_id,
                        restructure_term_id = EXCLUDED.restructure_term_id,
                        added_at = EXCLUDED.added_at,
                        modified_at = EXCLUDED.modified_at
                """,
                    (
                        restructuring_id,
                        loan_id,
                        new_loan_terms_id,
                        restructure_terms_id,
                        added_at,
                        modified_at,
                    ),
                )

            self.pg_connection.commit()
            print("Normalization of loan restructuring data completed.")
