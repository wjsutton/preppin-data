
-- We want to stack the tables on top of one another, since they have the same fields in each sheet.
-- Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these fields together
-- Make a Joining Date field based on the Joining Day, Table Names and the year 2023
-- Now we want to reshape our data so we have a field for each demographic, for each new customer
-- Make sure all the data types are correct for each field
-- Remove duplicates
-- If a customer appears multiple times take their earliest joining date
WITH DATA_STACK AS (
    SELECT *,'january' as table_name  FROM pd2023_wk04_january
        UNION ALL
    SELECT *,'february' as table_name FROM pd2023_wk04_february
        UNION ALL
    SELECT *,'march' as table_name FROM pd2023_wk04_march
        UNION ALL
    SELECT *,'april' as table_name FROM pd2023_wk04_april 
        UNION ALL
    SELECT *,'may' as table_name FROM pd2023_wk04_may 
        UNION ALL
    SELECT *,'june' as table_name FROM pd2023_wk04_june 
        UNION ALL
    SELECT *,'july' as table_name FROM pd2023_wk04_july
        UNION ALL
    SELECT *,'august' as table_name FROM pd2023_wk04_august
        UNION ALL
    SELECT *,'september' as table_name FROM pd2023_wk04_september
        UNION ALL
    SELECT *,'october' as table_name FROM pd2023_wk04_october
        UNION ALL
    SELECT *,'november' as table_name FROM pd2023_wk04_november
        UNION ALL
    SELECT *,'december' as table_name FROM pd2023_wk04_december 
)
,PRE_PIVOT AS (
    SELECT 
    id,
    date_from_parts(2023
    ,CASE UPPER(LEFT(table_name,3))
           WHEN 'JAN' THEN 1
           WHEN 'FEB' THEN 2
           WHEN 'MAR' THEN 3
           WHEN 'APR' THEN 4
           WHEN 'MAY' THEN 5
           WHEN 'JUN' THEN 6
           WHEN 'JUL' THEN 7
           WHEN 'AUG' THEN 8
           WHEN 'SEP' THEN 9
           WHEN 'OCT' THEN 10
           WHEN 'NOV' THEN 11
           WHEN 'DEC' THEN 12
           ELSE NULL
    END
    ,joining_day) as joining_date,
    demographic,
    value
    FROM DATA_STACK
)
,POST_PIVOT AS (
    SELECT 
    id::int as id,
    joining_date::date as joining_date,
    ethnicity,
    account_type,
    date_of_birth::date as date_of_birth,
    ROW_NUMBER() OVER(PARTITION BY id ORDER BY joining_date::date ASC) as rn
    FROM PRE_PIVOT
    PIVOT(max(value) for demographic in ('Ethnicity','Account Type','Date of Birth'))
    AS P (id,joining_date,ethnicity,account_type,date_of_birth)
    ORDER BY id
)
SELECT 
    id,
    joining_date,
    ethnicity,
    account_type,
    date_of_birth
FROM POST_PIVOT
WHERE rn = 1;
