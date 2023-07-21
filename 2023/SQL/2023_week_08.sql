-- Preppin' Data 2023 Week 08

-- Create a 'file date' using the month found in the file name
--     - The Null value should be replaced as 1
-- Clean the Market Cap value to ensure it is the true value as 'Market Capitalisation'
--     - Remove any rows with 'n/a'
-- Categorise the Purchase Price into groupings
    -- 0 to 24,999.99 as 'Low'
    -- 25,000 to 49,999.99 as 'Medium'
    -- 50,000 to 74,999.99 as 'High'
    -- 75,000 to 100,000 as 'Very High'
-- Categorise the Market Cap into groupings
    -- Below $100M as 'Small'
    -- Between $100M and below $1B as 'Medium'
    -- Between $1B and below $100B as 'Large' 
    -- $100B and above as 'Huge'
-- Rank the highest 5 purchases per combination of: file date, Purchase Price Categorisation and Market Capitalisation Categorisation.
-- Output only records with a rank of 1 to 5

WITH CTE AS (
SELECT 1 as file,* FROM pd2023_wk08_01

UNION ALL 

SELECT 2 as file,* FROM pd2023_wk08_02

UNION ALL 

SELECT 3 as file,* FROM pd2023_wk08_03

UNION ALL 

SELECT 4 as file,* FROM pd2023_wk08_04

UNION ALL 

SELECT 5 as file,* FROM pd2023_wk08_05

UNION ALL 

SELECT 6 as file,* FROM pd2023_wk08_06

UNION ALL 

SELECT 7 as file,* FROM pd2023_wk08_07

UNION ALL 

SELECT 8 as file,* FROM pd2023_wk08_08

UNION ALL 

SELECT 9 as file,* FROM pd2023_wk08_09

UNION ALL 

SELECT 10 as file,* FROM pd2023_wk08_10

UNION ALL 

SELECT 11 as file,* FROM pd2023_wk08_11

UNION ALL 

SELECT 12 as file,* FROM pd2023_wk08_12
)
,CATEGORIES AS (
SELECT 
DATE_FROM_PARTS(2023,file,1) as file_date,
CASE
    WHEN 
    ((SUBSTR(market_cap,2,LENGTH(market_cap)-2))::float *
    (CASE 
    WHEN RIGHT(market_cap,1)='B' THEN 1000000000
    WHEN RIGHT(market_cap,1)='M' THEN 1000000
    END))<100000000 THEN 'Small' 
    WHEN 
    ((SUBSTR(market_cap,2,LENGTH(market_cap)-2))::float *
    (CASE 
    WHEN RIGHT(market_cap,1)='B' THEN 1000000000
    WHEN RIGHT(market_cap,1)='M' THEN 1000000
    END))<1000000000 THEN 'Medium' 
    WHEN 
    ((SUBSTR(market_cap,2,LENGTH(market_cap)-2))::float *
    (CASE 
    WHEN RIGHT(market_cap,1)='B' THEN 1000000000
    WHEN RIGHT(market_cap,1)='M' THEN 1000000
    END))<100000000000 THEN 'Large'
    ELSE 'Huge'
END as market_cap_category,
CASE 
WHEN (SUBSTR(purchase_price,2,LENGTH(purchase_price)))::float < 25000 THEN 'Low'
WHEN (SUBSTR(purchase_price,2,LENGTH(purchase_price)))::float < 50000 THEN 'Medium'
WHEN (SUBSTR(purchase_price,2,LENGTH(purchase_price)))::float < 75000 THEN 'High'
WHEN (SUBSTR(purchase_price,2,LENGTH(purchase_price)))::float <= 100000 THEN 'Very High'
END as price_category,
*
FROM CTE
WHERE market_cap <> 'n/a'
)
,RANKED AS (
SELECT 
RANK() OVER(PARTITION BY file_date, market_cap_category, price_category ORDER BY (SUBSTR(purchase_price,2,LENGTH(purchase_price)))::float DESC) as rnk,
*
FROM CATEGORIES
)
SELECT 
market_cap_category, 
price_category,
file_date,
ticker,
sector,
market,
stock_name,
market_cap,
purchase_price,
rnk as rank
FROM RANKED 
WHERE rnk <=5

