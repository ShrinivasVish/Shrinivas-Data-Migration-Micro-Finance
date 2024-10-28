SELECT COUNT(*) FROM tbl_customers;
SELECT * FROM tbl_customers;

SELECT * FROM tbl_customers
WHERE customer_id=569676395005;

SELECT * FROM tbl_loan_types;
SELECT * FROM tbl_loan_applications;
SELECT * FROM tbl_loan_repayments;
SELECT * FROM tbl_loan_history;
SELECT * FROM tbl_loan_collateral;
SELECT * FROM tbl_loan_restructuring;
SELECT * FROM tbl_loan_disbursements;

DELETE FROM tbl_customers;
DELETE FROM tbl_loan_types;
DELETE FROM tbl_loan_applications;
DELETE FROM tbl_loan_repayments;
DELETE FROM tbl_loan_history;
DELETE FROM tbl_loan_collateral;
DELETE FROM tbl_loan_restructuring;
DELETE FROM tbl_loan_disbursements;