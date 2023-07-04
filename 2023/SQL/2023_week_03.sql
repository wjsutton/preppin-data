-- Preppin' Data 2023 Week 03

-- For the transactions file:
    -- Filter the transactions to just look at DSB (help)
        -- These will be transactions that contain DSB in the Transaction Code field
    -- Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
    -- Change the date to be the quarter (help)
    -- Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person) (help)
-- For the targets file:
    -- Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter (help)
    -- Rename the fields
    -- Remove the 'Q' from the quarter field and make the data type numeric (help)
-- Join the two datasets together (help)
    -- You may need more than one join clause!
-- Remove unnecessary fields
-- Calculate the Variance to Target for each row 
WITH CTE AS (
SELECT 
CASE 
WHEN online_or_in_person = 1 THEN 'Online'
WHEN online_or_in_person = 2 THEN 'In-Person'
END as online_in_person,
DATE_PART('quarter',DATE(transaction_date,'dd/MM/yyyy HH24:MI:SS')) as quarter,
SUM(value) as total_value
FROM pd2023_wk01
WHERE SPLIT_PART(transaction_code,'-',1) = 'DSB'
GROUP BY 1,2
)

SELECT 
online_or_in_person,
REPLACE(T.quarter,'Q','')::int as quarter,
V.total_value,
target,
V.total_value - target as variance_from_target
FROM pd2023_wk03_targets as T
UNPIVOT(target FOR quarter IN (Q1,Q2,Q3,Q4))
INNER JOIN CTE AS V ON T.ONLINE_OR_IN_PERSON = V.online_in_person AND REPLACE(T.quarter,'Q','')::int = V.quarter
