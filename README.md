# Python Data Migration

## Table of Contents

-   [What is Micro-Finance?](#what-is-micro-finance)
    -   [The Role of Microfinance in Financial Services](#the-role-of-microfinance-in-financial-services)
    -   [Key Products and Services in Microfinance](#key-products-and-services-in-microfinance)
-   [Project Goals](#project-goals)
-   [ELT Process](#elt-process)
    -   [Extraction](#extraction)
    -   [Loading](#loading)
    -   [Transformation](#transformation)
-   [Project Setup](#project-setup)
-   [Steps Executed](#steps-executed)
    -   [Sequence of Steps](#sequence-of-steps)
    -   [Full Load](#full-load)
    -   [Incremental Load](#incremental-load)
-   [Meta Data](#meta-data)

<a id="what-is-micro-finance"></a>

## What is Micro-Finance?

Microfinance is a specialized segment within the banking and financial services sector dedicated to providing financial services to individuals and small businesses who are typically underserved by traditional banks.

This sub-sector of finance focuses on inclusive financial access, aiming to bridge the gap for low-income individuals and entrepreneurs who may lack the credit history, assets, or resources needed to engage with conventional banking services.

<a id="the-role-of-microfinance-in-financial-services"></a>

### The Role of Microfinance in Financial Services

Microfinance falls within the financial inclusion category of the finance sector, focusing on providing essential banking services to those often excluded due to their financial or socioeconomic circumstances.

This includes individuals in rural or low-income areas, as well as small and micro-enterprises.

Microfinance institutions (MFIs) operate to support people in achieving self-sufficiency, promote local economic development, and address broader social issues like poverty and inequality.

<a id="key-products-and-services-in-microfinance"></a>

### Key Products and Services in Microfinance

Microfinance institutions typically offer a range of products designed to address the specific needs of their clients:

1. **Micro-Loans:** Small loans that allow individuals or small businesses to fund projects, start ventures, or cover daily expenses. These loans are usually short-term, and many are designed to be repaid in frequent installments to align with the borrower’s cash flow.

2. **Savings Accounts:** MFIs often provide savings accounts tailored to help people build a financial cushion, even with small, regular deposits.

3. **Micro-Insurance:** This includes basic insurance products, like health or life insurance, structured for affordability and accessibility.

4. **Remittances and Payment Services:** Some MFIs facilitate affordable money transfers and payments, providing crucial support for families dependent on income from abroad or remote work.

5. **Financial Education:** Many MFIs offer training to help clients manage their finances, improve business practices, and foster financial literacy in underserved communities.

<a id="project-goals"></a>

## Project Goals

1.  Built an **ELT pipeline** to conduct Data Migration from _MongoDB_ databse to _PostgreSQL_ database, by utilising the Python Scripts. (NOTE: MySLQ Database can also be used instead of PostgreSQL.)
2.  Implement **full load** and **incremental load**, to simulate real-world scenarios with respect to data operations.

    -   A _**full load**_ involves transferring _all data_ from the source system to the target system in its entirety.
    -   An _**incremental load**_, on the other hand, focuses on loading only the _new or modified records_ from the source system since the last load.

3.  **Write Clean Code.** We've utilise Object-Oriented Programming paradigm instead of simple Functional Programming paradigm as it offers the advantages specified as follows:

    -   **Modularity and Code Organization:** With classes for extraction, transformation, and loading, OOP allows you to logically separate these phases, making the code more modular and maintainable. Each phase’s responsibilities are encapsulated within its own class, improving readability and easing debugging.

    -   **Reusability:** OOP encourages reuse through inheritance and composition. For example, the Transformer class can build on functionality in Loader or Extractor classes, making code updates easier and promoting reuse of common logic.

    -   **State Management:** OOP allows each instance (e.g., MongoDB and PostgreSQL connections) to maintain its state within the class. This reduces the risk of unintended side effects and allows efficient resource handling through class attributes.

    -   **Scalability:** OOP's structure helps scale the project by allowing easy addition of new data sources or processing steps as new classes or methods, without significantly changing existing code.

<a id="elt-process"></a>

## ELT Processes

<a id="extraction"></a>

1. **Extaction** [ `src/extraction/mongo_extractor.py` ]

    - The **`MongoExtractor`** class is responsible for managing data extraction and updates from MongoDB collections and converting it into a format suitable for loading into PostgreSQL. Key functionalities include:

        - **Initialization and Connection**: Sets up a connection to the MongoDB database using credentials from environment variables and manages the MongoDB client.

        - **`convert_to_ist()`**: Adjusts date and time values to Indian Standard Time (IST) for consistent timestamp management.

        - **`load_collection_as_dataframe()`**: Fetches all documents from a specified MongoDB collection and converts them to a pandas DataFrame for easy processing. Removes the \_id field for compatibility with PostgreSQL.

        - **`insert_document()`**: Inserts a new document into a MongoDB collection after verifying that no existing document has the same unique identifier. Converts specified date fields to IST, and adds added_at and modified_at timestamps.

        - **`update_document()`**: Updates an existing document in MongoDB based on a unique identifier. Converts specified date fields to IST, and updates the modified_at timestamp.

<a id="loading"></a>

2. **Loading** [ `src/loading/postgres_loader.py` ]

    - The **`PostgresLoader`** class handles data loading and updating in PostgreSQL from MongoDB data sources. Its main responsibilities include establishing PostgreSQL connections, inserting data from pandas DataFrames, updating specific records, and tracking the latest timestamps for incremental loading. Key functionalities:

        - **Initialization and Connections**: Sets up MongoDB and PostgreSQL connections using credentials from environment variables and initializes the PostgreSQL connection.

        - **`create_pg_connection()`**: Establishes a connection to the PostgreSQL database.

        - **`load_dataframe_to_postgres()`**: Loads a pandas DataFrame into a specified PostgreSQL table. Supports JSON fields for columns containing JSON data, converting them to JSONB format during insertion.

        - **`update_record_in_postgres()`**: Updates an existing record in PostgreSQL based on a unique identifier. Only changes specified fields and handles transaction commits and rollbacks.

        - **`get_latest_timestamps()`**: Retrieves the latest added_at and modified_at timestamps from a specified PostgreSQL table, facilitating incremental load processes.

<a id="transformation"></a>

3. **Transformation** [ `src/transformation/tranformer.py` ]

    - The Transformer class handles data normalization and transformation between MongoDB and PostgreSQL. Its main responsibilities include applying timestamps, handling missing values, and normalizing loan restructuring data. Key functionalities:

        - **Initialization and Connections**: Sets up MongoDB and PostgreSQL connections using credentials from environment variables and initializes the PostgreSQL connection.

        - **`create_pg_connection()`**: Establishes a connection to the PostgreSQL database.

        - **`specific_ist_time()`**: Returns a fixed timestamp (27 October 2024, 00:00:00) adjusted to Indian Standard Time (IST).

        - **`add_ist_timestamp_fields_mongodb_aggregation()`**: Adds added_at and modified_at fields with IST timestamps to specified MongoDB collections.

        - **`replace_nat_with_none()`**: Replaces pd.NaT values with None in specified columns of DataFrames for smoother loading into PostgreSQL.

        - **`normalize_loan_restructuring()`**: Normalizes loan restructuring data by creating foreign key references for tbl_new_loan_terms and tbl_restructure_terms, then inserts or updates the tbl_loan_restructuring_normalized table.

## Project Setup

1. Clone the Git repository using the following command:

    ```
    git clone --branch shrinivas_assignment https://github.com/Data-science-interns-2024/Python-Assignments.git
    ```

2. Once the project has been coned from the specific branch of the repo, to install all the necessary libraries and dependencies, you would use the following command in your terminal:
    ```
    pip install -r requirements.txt
    ```
3. Configure the .env file for youre system variables as follows:

    ```
    MONGO_DB_URL=
    MONGODB_DB_NAME=
    PG_HOST=
    PG_DATABASE=
    PG_USER=
    PG_PASSWORD=
    PG_PORT=
    ```

4. From the root dreictor, use the following command to see the project in action:
    ```
    python main.py
    ```

## Steps Executed

Here’s the sequence of steps executed in main.py for both full load and incremental load, demonstrating the entry point of your ELT project:

### Sequence of Steps:

1. Create objects of Extractor, Transformer, and PostgresLoader:

    - Initializes the core components of the project:
    - `mongo_extractor`: Handles data extraction from MongoDB.
    - `postgres_loader`: Handles loading data into PostgreSQL.
    - `transformer`: Handles data transformation tasks.

2. Extract all collections as DataFrames:

    - The `mongo_extractor.load_collection_as_dataframe()` method is called for each collection in collections.
    - This loads the MongoDB collections into pandas DataFrames for further processing.

3. Replace pd.NaT with None in the specified columns of each collection:

    - The `transformer.replace_nat_with_none()` method processes the DataFrames, replacing pd.NaT (Not a Time) values with None in the columns that have date keys.

4. Run MongoDB aggregation to add timestamps:

    - The `transformer.add_ist_timestamp_fields_mongodb_aggregation()` method runs MongoDB aggregations to add the required timestamps (likely added_at and modified_at) to each collection.

### Full Load:

5. Load the data into PostgreSQL database tables (Full Load):

    - For each collection (now in the form of a DataFrame), the `postgres_loader.load_dataframe_to_postgres()` method inserts the DataFrame into the corresponding PostgreSQL table (tbl\*{collection}).
    - This is the full load process where all the data is loaded into PostgreSQL tables for the first time.

6. Execute normalization for loan restructuring:

    - The `transformer.normalize_loan_restructuring()` method is called to perform normalization of the loan restructuring data in the appropriate collections.

### Incremental Load:

7. Insert a new document into the customers collection (Incremental Load Step 1):

    - A new customer document (new_customer) is created and inserted into the MongoDB customers collection using `mongo_extractor.insert_document()`.

8. Load the new document into the corresponding PostgreSQL table:

    - The newly inserted customer document is loaded into the tbl_customers table in PostgreSQL using `postgres_loader.load_dataframe_to_postgres()`.

9. Execute normalization for loan restructuring again:

    - The normalization process is run once more to ensure that any new data (such as the newly added customer) is also properly normalized.

10. Insert another new document into the customers collection (Incremental Load Step 2):

    - Another new customer document (another_customer) is created and inserted into the MongoDB customers collection.

11. Load the new document into PostgreSQL:

    - The second new customer document is loaded into the tbl_customers table in PostgreSQL.

12. Execute normalization for loan restructuring again:

    - The normalization function is executed once more.

13. Update an existing document in the customers collection (Incremental Load Step 3):

    - An existing customer document (updated_customer) is created with updated information and is used to update the corresponding document in MongoDB using `mongo_extractor.update_document()`.

14. Load the updated document into PostgreSQL:

    - The updated customer document is loaded into the tbl_customers PostgreSQL table using `postgres_loader.update_record_in_postgres()`.

15. Execute normalization for loan restructuring again:

    - Finally, normalization is executed one last time for loan restructuring to ensure that any changes made during the incremental load are handled properly.

## Meta Data

The dataset has been created to simulate a start-up within micro-finance sector. The collections have been specified in the order of creation as follows for better context:

**`customers` OR `data/customers.json`**

Demographics of customers.

| Key               | MongoDB Data Type | PostgreSQL Data Type        |
| ----------------- | ----------------- | --------------------------- |
| customer_id       | Int64             | bigint                      |
| first_name        | String            | character varying           |
| last_name         | String            | character varying           |
| gender            | String            | character varying           |
| age               | Int32             | integer                     |
| employment_status | String            | character varying           |
| income_level      | String            | character varying           |
| location          | String            | character varying           |
| joined_date       | Date              | timestamp without time zone |
| added_at          | Date              | timestamp without time zone |
| modified_at       | Date              | timestamp without time zone |

**`loan_types` OR `data/loan_types.json`**

Types of loans that are provided to the customers and their corresponding attributes.

| Key                        | MongoDB Data Type | PostgreSQL Data Type        |
| -------------------------- | ----------------- | --------------------------- |
| loan_type_id               | Int32             | integer                     |
| loan_type_name             | String            | character varying           |
| max_loan_amount            | Int32             | integer                     |
| interest_rate              | Int32             | integer                     |
| repayment_period_in_months | Int32             | integer                     |
| eligibility_criteria       | String            | character varying           |
| added_at                   | Date              | timestamp without time zone |
| modified_at                | Date              | timestamp without time zone |

**`loan_applications` OR `data/loan_applications.json`**

Connected with customer_id and has keeps track of all loan applications registered / initiated.

| Key              | MongoDB Data Type | PostgreSQL Data Type        |
| ---------------- | ----------------- | --------------------------- |
| loan_id          | Int64             | bigint                      |
| customer_id      | Int64             | bigint                      |
| loan_type_id     | Int32             | integer                     |
| loan_amount      | Double            | numeric                     |
| loan_status      | String            | character varying           |
| application_date | Date              | timestamp without time zone |
| approval_date    | Date              | timestamp without time zone |
| added_at         | Date              | timestamp without time zone |
| modified_at      | Date              | timestamp without time zone |

**`loan_repayments` OR `data/loan_repayments.json`**

Keeps tracks of repayment of loan that have `loan_status` as Approved.

| Key              | MongoDB Data Type | PostgreSQL Data Type        |
| ---------------- | ----------------- | --------------------------- |
| repayment_id     | Int64             | bigint                      |
| loan_id          | Int64             | bigint                      |
| repayment_amount | Double            | numeric                     |
| repayment_date   | Date              | timestamp without time zone |
| repayment_status | String            | character varying           |
| added_at         | Date              | timestamp without time zone |
| modified_at      | Date              | timestamp without time zone |

**`loan_history` OR `data/loan_history.json`**

Keeps meta-data about loan_applications for every customer.

| Key                  | MongoDB Data Type | PostgreSQL Data Type        |
| -------------------- | ----------------- | --------------------------- |
| history_id           | Int64             | bigint                      |
| customer_id          | Int64             | bigint                      |
| loan_id              | Int64             | bigint                      |
| previous_loan_status | Boolean           | character varying           |
| loan_disbursed_date  | Date              | timestamp without time zone |
| loan_repaid_date     | Date              | timestamp without time zone |
| added_at             | Date              | timestamp without time zone |
| modified_at          | Date              | timestamp without time zone |

**`loan_collateral` OR `data/loan_collateral.json`**

Hold information for the asset been registered in case the customer is not able to repay the loan.

| Key              | MongoDB Data Type | PostgreSQL Data Type        |
| ---------------- | ----------------- | --------------------------- |
| collateral_id    | Int64             | bigint                      |
| loan_id          | Int64             | bigint                      |
| collateral_type  | String            | character varying           |
| collateral_value | Double            | numeric                     |
| added_at         | Date              | timestamp without time zone |
| modified_at      | Date              | timestamp without time zone |

**`loan_restructuring` OR `data/loan_restructuring.json`**

Specifies the new_loan_terms and restructure_terms for particular Approved loan.

| Key              | MongoDB Data Type | PostgreSQL Data Type        |
| ---------------- | ----------------- | --------------------------- |
| restructuring_id | Int64             | bigint                      |
| loan_id          | Int64             | bigint                      |
| new_loan_terms   | Object            | jsonb                       |
| added_at         | Date              | timestamp without time zone |
| modified_at      | Date              | timestamp without time zone |

**`loan_disbursements` OR `data/loan_disbursements.json`**

Holds data about transaction details of the loan that has been approved and by the bank to the customer.

| Key                 | MongoDB Data Type | PostgreSQL Data Type        |
| ------------------- | ----------------- | --------------------------- |
| disbursement_id     | Int64             | bigint                      |
| loan_id             | Int64             | bigint                      |
| disbursement_amount | Double            | numeric                     |
| disbursement_date   | Date              | timestamp without time zone |
| disbursement_method | String            | character varying           |
| application_date    | Date              | timestamp without time zone |
| added_at            | Date              | timestamp without time zone |
| modified_at         | Date              | timestamp without time zone |

**`new_loan_terms` OR `data/combinations__new_loan_terms.json`**

Holds data about transaction details of the loan that has been approved and by the bank to the customer.

| Key                        | MongoDB Data Type | PostgreSQL Data Type        |
| -------------------------- | ----------------- | --------------------------- |
| new_loan_term_id           | Int32             | integer                     |
| interest_rate              | Int32             | integer                     |
| repayment_period_in_months | Int32             | integer                     |
| added_at                   | Date              | timestamp without time zone |
| modified_at                | Date              | timestamp without time zone |

**`restructure_terms` OR `data/combinations__new_loan_terms.json`**

Holds data about transaction details of the loan that has been approved and by the bank to the customer.

| Key                 | MongoDB Data Type | PostgreSQL Data Type        |
| ------------------- | ----------------- | --------------------------- |
| restructure_term_id | Int32             | integer                     |
| reason              | String            | character varying           |
| new_schedule        | String            | character varying           |
| concessions         | String            | character varying           |
| added_at            | Date              | timestamp without time zone |
| modified_at         | Date              | timestamp without time zone |
