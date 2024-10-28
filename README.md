# Python Data Migration Assignment

## The project is to build to acheive the following 2 goals:

-   **ELT pipeline** for Data Migration from _MongoDB_ databse to _PostgreSQL_ database OR _MySQL_ database, by utilising the Python Scripts as intermediate and post medium.
-   Implement **full load** and **incremental load**, to simulate real-world scenarios with respect to data.
    -   A _**full load**_ involves transferring _all data_ from the source system to the target system in its entirety.
    -   An _**incremental load**_, on the other hand, focuses on loading only the _new or modified records_ from the source system since the last load.

## Project Workflow

### Setup Source System

The dataset has been created to simulate a start-up within micro-finance sector. The collections have been specified in the order of creation as follows for better context:

| **Collection Name**       | **Description**                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| **customers**             | Demographics of customers.                                                                               |
| **loan_types**            | Types of loans that are provided to the customers and their corresponding attributes..                   |
| **loan_applications**     | Connected with customer_id and has keeps track of all loan applications registered / initiated.          |
| **loan_repayments**       | Keeps tracks of repayment of loan that are only loan*status as \_Approved*.                              |
| **customer_loan_history** | Keeps meta-data about loan_applications for every customer.                                              |
| **loan_collatreal**       | Hold information for the asset been registered in case the customer is not able to repay the loan.       |
| **loan_restructuring**    | Specifies the new_loan_terms and restructure_terms for particular Approved loan.                         |
| **loan_disburesement**    | Holds data about transaction details of the loan that has been approved and by the bank to the customer. |

### ELT Processes

NOTE: Define Database Schemas already into the PostgreSQL Database.

1. **Extacttion** Phase
    - Establish connnection with MongoDB DB and extract data from the MongoDB (source system) DB into the Python Script as pandas dataframes.
2. **Loading** Phase
    - Establish connnection with PostgreSQL DB and load data to the PostgreSQL DB by performing WRITE operations to the DB.

-   **Transformatino** Phase
    -   Here all the data transformation and processsing will be conducted in order to make it suitable for Analysis.
    -   Some necessary step we'd perfrom are as data as necessary
    -   faltten data and normalize tables as necessary
    -   format data into interpretable form
    -   keep track of full load and incremental load
