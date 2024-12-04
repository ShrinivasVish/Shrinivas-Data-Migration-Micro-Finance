import os
import json
import psycopg2
import pandas as pd
from psycopg2 import sql
from pymongo import MongoClient
from dotenv import load_dotenv

from config import (
    unique_id_mapping,
    fixed_date_ist,
    collections_with_date_keys,
    collections,
)


class PostgresLoader:
    def __init__(self):
        """
        Initializes the PostgresLoader class.
        Loads environment variables and sets up MongoDB and PostgreSQL connection parameters.
        """
        load_dotenv()

        # MongoDB parameters
        self.mongo_url = os.getenv("MONGO_DB_URL")
        self.mongo_db_database_name = os.getenv("MONGODB_DB_NAME")
        self.mongo_client = MongoClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_database_name]

        # PostgreSQL parameters
        self.pg_database = os.getenv("PG_DATABASE")
        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")
        self.pg_host = os.getenv("PG_HOST")
        self.pg_port = os.getenv("PG_PORT")
        self.pg_connection = self.create_pg_connection()

    def create_pg_connection(self):
        """Establishes a connection to PostgreSQL."""
        try:
            connection = psycopg2.connect(
                database=self.pg_database,
                user=self.pg_user,
                password=self.pg_password,
                host=self.pg_host,
                port=self.pg_port,
            )
            print("PostgreSQL connection established successfully.")
            return connection
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None

    def load_dataframe_to_postgres(
        self, df: pd.DataFrame, table_name: str, json_columns: list = []
    ):
        connection = self.create_pg_connection()
        if not connection:
            print("Failed to establish database connection.")
            return

        cursor = connection.cursor()
        connection.set_session(autocommit=True)  # Ensure autocommit is enabled

        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)

        for column in json_columns:
            if column in df.columns:
                df[column] = df[column].apply(json.dumps)

        columns = df.columns.tolist()
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(
                sql.SQL("%s::jsonb") if col in json_columns else sql.Placeholder()
                for col in columns
            ),
        )

        data_tuples = [tuple(row) for row in df.itertuples(index=False)]
        print(f"Insert query: {insert_query.as_string(cursor)}")
        print(f"Number of rows to insert: {len(data_tuples)}")

        batch_size = 1000
        try:
            for i in range(0, len(data_tuples), batch_size):
                batch = data_tuples[i : i + batch_size]
                cursor.executemany(insert_query, batch)
                connection.commit()  # Explicit commit after each batch
                print(
                    f"Inserted batch {i // batch_size + 1} with {len(batch)} records."
                )
        except Exception as error:
            print(f"Error inserting data into PostgreSQL: {error}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
            print("Connection closed.")

    def update_record_in_postgres(
        self,
        record: pd.Series,
        table_name: str,
        unique_id_col: str,
    ):
        """
        Updates an existing record in the PostgreSQL table based on a unique identifier.

        Parameters:
        record (pd.Series): The record to update.
        table_name (str): The name of the PostgreSQL table to update.
        unique_id_col (str): The name of the unique identifier column used for the update.
        """
        connection = self.create_pg_connection()
        cursor = connection.cursor()

        set_clause = ", ".join(
            [f"{col} = %s" for col in record.index if col != unique_id_col]
        )
        update_query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {unique_id_col} = %s
        """

        values = tuple(record[col] for col in record.index if col != unique_id_col) + (
            record[unique_id_col],
        )

        try:
            cursor.execute(update_query, values)
            connection.commit()
            print(
                f"Record with {unique_id_col} {record[unique_id_col]} updated successfully."
            )
        except Exception as error:
            print(f"Error updating record in PostgreSQL: {error}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    def get_latest_timestamps(self, table_name):
        """
        Retrieves the latest added_at and modified_at timestamps from the specified PostgreSQL table.
        """
        query = f"""
        SELECT MAX(added_at) AS last_added_at, MAX(modified_at) AS last_modified_at
        FROM {table_name};
        """
        connection = self.create_pg_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0], result[1]
