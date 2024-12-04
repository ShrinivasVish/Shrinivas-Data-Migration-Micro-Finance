import os
from datetime import datetime, timezone, timedelta
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv


from config import (
    unique_id_mapping,
    fixed_date_ist,
    collections_with_date_keys,
    collections,
)


class MongoExtractor:
    def __init__(self):
        """
        Initializes the MongoExtractor class.
        Loads environment variables and sets up MongoDB connection parameters.
        """

        # Load environment variables from .env file
        load_dotenv()

        # MongoDB connection parameters
        self.mongo_url = os.getenv("MONGO_DB_URL")
        self.mongo_db_database_name = os.getenv("MONGODB_DB_NAME")
        self.mongo_client = MongoClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_database_name]

    def get_mongo_client(self) -> MongoClient:
        """
        Establishes and returns a MongoDB client connection.
        Returns:
            MongoClient: MongoDB client instance.
        """
        if self.mongo_client is None:
            self.mongo_client = MongoClient(self.mongo_url)
        return self.mongo_client

    def convert_to_ist(self, date_str):
        """Convert a date string to a datetime object adjusted to IST."""
        if date_str is not None:
            # Parse the date string
            date_obj = datetime.fromisoformat(str(date_str))
            # Adjust to IST (UTC+5:30)
            ist_time = date_obj + timedelta(hours=5, minutes=30)
            return ist_time
        return None

    def load_collection_as_dataframe(self, collection_name: str) -> pd.DataFrame:
        """
        Converts a MongoDB collection into a pandas DataFrame.

        Parameters:
            collection_name (str): The name of the MongoDB collection.

        Returns:
            pd.DataFrame: A DataFrame containing the MongoDB collection data.
        """
        collection = self.db[collection_name]
        data = list(collection.find())
        df = pd.DataFrame(data)

        # Drop '_id' column if it exists
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        return df

    def insert_document(self, collection_name: str, date_keys: list, document: dict):
        """
        Inserts a document into the specified MongoDB collection if no document with the
        same unique identifier exists.

        Parameters:
            collection_name (str): The name of the MongoDB collection.
            date_keys (list): List of date keys to adjust time zones.
            document (dict): The document to insert into the collection.
        """
        print("Insertion of document has begun.")
        config = unique_id_mapping.get(collection_name)
        if not config:
            print(
                f"No configuration for collection '{collection_name}'. Document not inserted."
            )
            return

        unique_id_field = config["unique_id_key_col"]
        collection = self.db[collection_name]

        if unique_id_field in document:
            if collection.find_one({unique_id_field: document[unique_id_field]}):
                print(
                    f"Document with {unique_id_field} = {document[unique_id_field]} already exists."
                )
                return

        # Convert dates and set timestamps
        for date_key in date_keys:
            if date_key in document:
                document[date_key] = self.convert_to_ist(document[date_key])

        current_time_ist = datetime.now(timezone.utc)
        document["added_at"] = current_time_ist
        document["modified_at"] = current_time_ist

        result = collection.insert_one(document)
        print(f"Document inserted with ID: {result.inserted_id}")

    def update_document(
        self, collection_name: str, date_keys: list, unique_id_value: int, update: dict
    ):
        """
        Updates an existing document in the specified MongoDB collection.

        Parameters:
            collection_name (str): The name of the MongoDB collection.
            unique_id_value (int): The unique identifier value of the document to update.
            update (dict): The updates to apply to the document.
        """
        collection = self.db[collection_name]
        unique_id_key_col = unique_id_mapping[collection_name]["unique_id_key_col"]

        update = collection.find_one({unique_id_key_col: update[unique_id_key_col]})

        # Convert dates and set timestamps
        for date_key in date_keys:
            if date_key in update:
                update[date_key] = self.convert_to_ist(update[date_key])

        query = {unique_id_key_col: unique_id_value}
        update["modified_at"] = datetime.now(timezone.utc)

        result = collection.update_one(query, {"$set": update})
        if result.matched_count > 0:
            print(f"Document updated: {result.modified_count} document(s) modified.")
        else:
            print("No document found matching the query.")
