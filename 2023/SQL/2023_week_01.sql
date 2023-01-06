-- Preppin' Data 2023 Week 01
/*
Split the Transaction Code to extract the letters at the start of the transaction code. 
These identify the bank who processes the transaction 
Rename the new field with the Bank code 'Bank'. 
Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values. 
Change the date to be the day of the week
Different levels of detail are required in the outputs. You will need to sum up the values of the transactions in three ways (help):
1. Total Values of Transactions by each bank
2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
3. Total Values by Bank and Customer Code

SELECT 
LEFT(transaction_code,charindex('-', transaction_code)-1) as bank,
CASE online_or_in_person
WHEN 1 THEN 'Online'
WHEN 2 THEN 'In-Person'
END as online_or_in_person,
to_char((RIGHT(LEFT(transaction_date,10),4) || '-' || RIGHT(LEFT(transaction_date,5),2) || '-' || LEFT(transaction_date,2))::date, 'dy')  as transaction_date,
customer_code,
value
FROM PD2023_WK01
*/

-- OUTPUT 1 
SELECT 
LEFT(transaction_code,charindex('-', transaction_code)-1) as bank,
SUM(value) as value
FROM PD2023_WK01
GROUP BY LEFT(transaction_code,charindex('-', transaction_code)-1);

-- OUTPUT 2 
WITH CTE AS (
SELECT 
LEFT(transaction_code,charindex('-', transaction_code)-1) as bank,
CASE online_or_in_person
WHEN 1 THEN 'Online'
WHEN 2 THEN 'In-Person'
END as online_or_in_person,
to_char((RIGHT(LEFT(transaction_date,10),4) || '-' || RIGHT(LEFT(transaction_date,5),2) || '-' || LEFT(transaction_date,2))::date, 'dy') as transaction_date,
value
FROM PD2023_WK01
)

SELECT 
bank,
online_or_in_person,
CASE transaction_date
    WHEN 'Tue' THEN 'Tuesday'
    WHEN 'Wed' THEN 'Wednesday'
    WHEN 'Thu' THEN 'Thursday'
    WHEN 'Sat' THEN 'Saturday'
    ELSE transaction_date || 'day'
END as transaction_date,
SUM(value) as value
FROM CTE
GROUP BY bank,
online_or_in_person,
CASE transaction_date
    WHEN 'Tue' THEN 'Tuesday'
    WHEN 'Wed' THEN 'Wednesday'
    WHEN 'Thu' THEN 'Thursday'
    WHEN 'Sat' THEN 'Saturday'
    ELSE transaction_date || 'day'
END;

-- OUTPUT 3
SELECT 
LEFT(transaction_code,charindex('-', transaction_code)-1) as bank,
customer_code,
SUM(value) as value
FROM PD2023_WK01
GROUP BY LEFT(transaction_code,charindex('-', transaction_code)-1),
customer_code;