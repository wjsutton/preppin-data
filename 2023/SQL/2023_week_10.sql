-- Preppin' Data 2023 Week 10

-- Aggregate the data so we have a single balance for each day already in the dataset, for each account
-- Scaffold the data so each account has a row between 31st Jan and 14th Feb
-- Make sure new rows have a null in the Transaction Value field
-- Create a parameter so a particular date can be selected
-- Filter to just this date
-- Output the data 

SET SELECTED_DATE = '2023-02-01';

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
,WEEK09_OUTPUT as (
SELECT 
account_id,
transaction_date,
value as transaction_value,
SUM(COALESCE(value,0)) OVER(PARTITION BY account_id ORDER BY transaction_date, value DESC) + balance as balance
FROM CTE
ORDER BY account_id, transaction_date, value DESC
)
,DAY_TRANS AS (
SELECT 
account_id,
transaction_date,
SUM(transaction_value) as transaction_value
FROM WEEK09_OUTPUT
GROUP BY account_id,
transaction_date
)
,BALANCE_ORDERED AS (
SELECT 
*
,ROW_NUMBER() OVER(PARTITION BY account_id, transaction_date ORDER BY transaction_value ASC) as rn
FROM WEEK09_OUTPUT
)
,DAILY_SUMMARY AS (
SELECT 
B.account_id,
B.transaction_date,
T.transaction_value,
balance
FROM BALANCE_ORDERED as B
INNER JOIN DAY_TRANS as T on T.account_id = B.account_id AND T.transaction_date = B.transaction_date
WHERE rn=1
)
,ACCOUNTNUMS AS (
SELECT DISTINCT 
account_id 
FROM DAILY_SUMMARY
)
,NUMBERS AS (
SELECT '2023-01-31'::date as n,
account_id 
FROM ACCOUNTNUMS

UNION ALL

SELECT DATEADD('day',1,n),
account_id
FROM NUMBERS 
WHERE n < '2023-02-14'::date
)
,DAILY_VIEW AS (
SELECT 
N.account_id,
N.n as transaction_date,
D.transaction_value,
D.balance as balance_dontuse,
B.transaction_date as transaction_date2,
B.balance,
DATEDIFF('day',B.transaction_date,N.n) as datediff,
ROW_NUMBER() OVER(PARTITION BY N.account_id,N.n ORDER BY DATEDIFF('day',B.transaction_date,N.n)) as rn
FROM NUMBERS as N 
LEFT JOIN DAILY_SUMMARY as D on N.account_id = D.account_id AND N.n = D.transaction_date
INNER JOIN BALANCE_ORDERED as B on B.account_id = N.account_id AND B.transaction_date <= N.n
ORDER BY N.account_id, N.n
)
SELECT 
account_id,
transaction_date,
transaction_value,
balance
FROM DAILY_VIEW 
WHERE rn =1
AND transaction_date = $SELECTED_DATE;
