/*
Preppin' Data 2023 Week 3

For the transactions file:
 - Filter the transactions to just look at DSB
    - These will be transactions that contain DSB in the Transaction Code field
 - Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
 - Change the date to be the quarter
 - Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person) 

For the targets file:
 - Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter 
 - Rename the fields
 - Remove the 'Q' from the quarter field and make the data type numeric
Join the two datasets together
 - You may need more than one join clause!
Remove unnecessary fields
Calculate the Variance to Target for each row 
*/
WITH CTE AS (
    SELECT 
        CASE online_or_in_person
            WHEN 1 THEN 'Online'
            WHEN 2 THEN 'In-Person'
        END as online_or_in_person,
        DATE_PART('quarter',DATE(LEFT(transaction_date,10),'DD/MM/YYYY')) as quarter,
        SUM(value) as value
    FROM pd2023_wk01
    WHERE UPPER(transaction_code) LIKE '%DSB%'
    GROUP BY 1,2
)
SELECT 
    T.online_or_in_person,
    REPLACE(T.quarter,'Q','') as quarter, 
    CTE.value,
    quarterly_targets,
    CTE.value - quarterly_targets as variance_to_target
FROM pd2023_wk03_targets as T
UNPIVOT(quarterly_targets FOR quarter IN (Q1, Q2, Q3, Q4))
INNER JOIN CTE ON T.online_or_in_person = CTE.online_or_in_person
AND REPLACE(T.quarter,'Q','') = CTE.quarter ;
