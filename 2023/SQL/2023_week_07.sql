-- Preppin' Data 2023 Week 07

-- For the Transaction Path table:
--     - Make sure field naming convention matches the other tables
--         - i.e. instead of Account_From it should be Account From
-- For the Account Information table:
--     - Make sure there are no null values in the Account Holder ID
--     - Ensure there is one row per Account Holder ID
--         - Joint accounts will have 2 Account Holders, we want a row for each of them
-- For the Account Holders table:
--     - Make sure the phone numbers start with 07
-- Bring the tables together
-- Filter out cancelled transactions 
-- Filter to transactions greater than £1,000 in value 
-- Filter out Platinum accounts

WITH ACC as (
SELECT 
ACCOUNT_NUMBER, 
ACCOUNT_TYPE, 
value as ACCOUNT_HOLDER_ID, 
BALANCE_DATE, 
BALANCE
FROM pd2023_wk07_account_information, LATERAL SPLIT_TO_TABLE(account_holder_id,', ')
WHERE account_holder_id IS NOT NULL
)
SELECT 
D.transaction_id,
account_to,
transaction_date,
value,
account_number,
account_type,
balance_date,
balance,
name,
date_of_birth,
'0' || contact_number::varchar(20) as contact_number,
first_line_of_address
FROM pd2023_wk07_transaction_detail as D
INNER JOIN pd2023_wk07_transaction_path as P ON D.transaction_id = P.transaction_id
INNER JOIN ACC on ACC.account_number = P.account_from
INNER JOIN pd2023_wk07_account_holders as H ON H.account_holder_id = ACC.account_holder_id
WHERE cancelled_ = 'N'
AND value > 1000
AND account_type <> 'Platinum'
