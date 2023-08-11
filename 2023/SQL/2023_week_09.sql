-- Preppin' Data 2023 Week 09

-- For the Transaction Path table:
--     Make sure field naming convention matches the other tables
--         - i.e. instead of Account_From it should be Account From
-- Filter out the cancelled transactions
-- Split the flow into incoming and outgoing transactions 
-- Bring the data together with the Balance as of 31st Jan 
-- Work out the order that transactions occur for each account
--     Hint: where multiple transactions happen on the same day, assume the highest value transactions happen first
-- Use a running sum to calculate the Balance for each account on each day 
-- The Transaction Value should be null for 31st Jan, as this is the starting balance
-- Output the data

WITH CTE AS (
SELECT 
account_to as account_id,
transaction_date,
value,
balance
FROM pd2023_wk07_transaction_detail as D
INNER JOIN pd2023_wk07_transaction_path as P on D.transaction_id = P.transaction_id
INNER JOIN pd2023_wk07_account_information as A on A.account_number = P.account_to
WHERE cancelled_ <> 'Y'
AND balance_date = '2023-01-31'

UNION ALL

SELECT 
account_from as account_id,
transaction_date,
value * (-1) as value,
balance
FROM pd2023_wk07_transaction_detail as D
INNER JOIN pd2023_wk07_transaction_path as P on D.transaction_id = P.transaction_id
INNER JOIN pd2023_wk07_account_information as A on A.account_number = P.account_from
WHERE cancelled_ <> 'Y'
AND balance_date = '2023-01-31'

UNION ALL

SELECT 
account_number as account_id,
balance_date as transaction_date,
NULL as value,
balance
FROM pd2023_wk07_account_information
)

SELECT 
account_id,
transaction_date,
value as transcation_value,
SUM(COALESCE(value,0)) OVER(PARTITION BY account_id ORDER BY transaction_date, value DESC) + balance as balance
FROM CTE
ORDER BY account_id, transaction_date, value DESC
;
