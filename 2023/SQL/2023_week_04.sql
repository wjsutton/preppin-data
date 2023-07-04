-- Preppin' Data 2023 Week 04

-- We want to stack the tables on top of one another, since they have the same fields in each sheet. We can do this one of 2 ways:
    -- Drag each table into the canvas and use a union step to stack them on top of one another
    -- Use a wildcard union in the input step of one of the tables
-- Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these fields together
-- Make a Joining Date field based on the Joining Day, Table Names and the year 2023
-- Now we want to reshape our data so we have a field for each demographic, for each new customer (help)
-- Make sure all the data types are correct for each field
-- Remove duplicates (help)
    -- If a customer appears multiple times take their earliest joining date
WITH CTE AS (
SELECT *, 'pd2023_wk04_january' as tablename FROM pd2023_wk04_january

UNION ALL 

SELECT *, 'pd2023_wk04_february' as tablename FROM pd2023_wk04_february

UNION ALL 

SELECT *, 'pd2023_wk04_march' as tablename FROM pd2023_wk04_march

UNION ALL 

SELECT *, 'pd2023_wk04_april' as tablename FROM pd2023_wk04_april

UNION ALL

SELECT *, 'pd2023_wk04_may' as tablename FROM pd2023_wk04_may

UNION ALL

SELECT *, 'pd2023_wk04_june' as tablename FROM pd2023_wk04_june

UNION ALL

SELECT *, 'pd2023_wk04_july' as tablename FROM pd2023_wk04_july

UNION ALL

SELECT *, 'pd2023_wk04_august' as tablename FROM pd2023_wk04_august

UNION ALL

SELECT *, 'pd2023_wk04_september' as tablename FROM pd2023_wk04_september

UNION ALL

SELECT *, 'pd2023_wk04_october' as tablename FROM pd2023_wk04_october

UNION ALL

SELECT *, 'pd2023_wk04_november' as tablename FROM pd2023_wk04_november

UNION ALL

SELECT *, 'pd2023_wk04_december' as tablename FROM pd2023_wk04_december
)
, PRE_PIVOT AS (
SELECT 
id,
date_from_parts(2023,DATE_PART('month',DATE(SPLIT_PART(tablename,'_',3),'MMMM')),joining_day) as joining_date,
demographic,
value
FROM CTE
)
,POST_PIVOT AS (
SELECT 
id,
joining_date,
ethnicity,
account_type,
date_of_birth::date as date_of_birth,
ROW_NUMBER() OVER(PARTITION BY id ORDER BY joining_date ASC) as rn
FROM PRE_PIVOT
PIVOT(MAX(value) FOR demographic IN ('Ethnicity','Account Type','Date of Birth')) AS P
(id,
joining_date,
ethnicity,
account_type,
date_of_birth)
)
SELECT 
id,
joining_date,
account_type,
date_of_birth,
ethnicity
FROM post_pivot
WHERE rn = 1

