-- Preppin' Data 2023 Week 12

-- Fill down the years and create a date field for the UK bank holidays
-- Combine with the UK New Customer dataset
-- Create a Reporting Day flag
--     - UK bank holidays are not reporting days
--     - Weekends are not reporting days
-- For non-reporting days, assign the customers to the next reporting day
-- Calculate the reporting month, as per the definition above
-- Filter our January 2024 dates
-- Calculate the reporting day, defined as the order of days in the reporting month
--     - You'll notice reporting months often have different numbers of days!
-- Now let's focus on ROI data. This has already been through a similar process to the above, but using the ROI bank holidays. We'll have to align it with the UK reporting schedule
-- Rename fields so it's clear which fields are ROI and which are UK
-- Combine with UK data
-- For days which do not align, find the next UK reporting day and assign new customers to that day (for more detail, refer to the above description of the challenge)
-- Make sure null customer values are replaced with 0's
-- Create a flag to find which dates have differing reporting months when using the ROI/UK systems
-- Output the data

WITH YEAR_FILL AS (
SELECT 
MAX(year) OVER(ORDER BY row_num) as year,
date,
bank_holiday
FROM pd2023_wk12_uk_bank_holidays
)
,BANK_HOLS AS (
SELECT 
DATE(date || '-' || year,'DD-Mon-YYYY') as date,
bank_holiday
FROM YEAR_FILL
WHERE date <> ''
)
,REPORTING_WITH_FLAG AS (
SELECT 
DATE(UK.date,'DD/MM/YYYY') as date,
DAYNAME(DATE(UK.date,'DD/MM/YYYY')) as weekday,
CASE 
WHEN LEFT(DAYNAME(DATE(UK.date,'DD/MM/YYYY')),1) = 'S' OR  BH.bank_holiday IS NOT NULL THEN 'N'
ELSE 'Y'
END as reporting_flag,
new_customers,
BH.bank_holiday
FROM pd2023_wk12_new_customers as UK
LEFT JOIN BANK_HOLS as BH on DATE(UK.date,'DD/MM/YYYY') = BH.date
)
,NON_REPORTING_DATES AS (
SELECT DISTINCT
date as non_reporting_date
FROM REPORTING_WITH_FLAG
WHERE reporting_flag = 'N'
)
,REPORTING_LOOKUP AS (
SELECT 
non_reporting_date,
MIN(date) as next_reporting_date
FROM REPORTING_WITH_FLAG as R
INNER JOIN NON_REPORTING_DATES as NR on NR.non_reporting_date < R.date
WHERE reporting_flag = 'Y'
GROUP BY non_reporting_date
)
, UK_REPORTING AS (
SELECT 
COALESCE(next_reporting_date,date) as date,
MONTHNAME(COALESCE(next_reporting_date,date)) || '-' || YEAR(COALESCE(next_reporting_date,date)) as month,
SUM(new_customers) as new_customers
FROM REPORTING_WITH_FLAG as R
LEFT JOIN REPORTING_LOOKUP as L on L.non_reporting_date = R.date
GROUP BY 1,2 
)
,UK_LAST_DAY AS (
SELECT 
month,
MAX(date) as last_date
FROM UK_REPORTING
GROUP BY month
)
,UK_REPORTING_ADJ AS (
SELECT 
CASE 
WHEN last_date IS NULL THEN MONTHNAME(date) || '-' || YEAR(date)
ELSE MONTHNAME(DATEADD('month',1,date)) || '-' || YEAR(DATEADD('month',1,date))
END  as reporting_month,
date,
ROW_NUMBER() OVER(PARTITION BY 
(CASE 
WHEN last_date IS NULL THEN MONTHNAME(date) || '-' || YEAR(date)
ELSE MONTHNAME(DATEADD('month',1,date)) || '-' || YEAR(DATEADD('month',1,date))
END) ORDER BY date
) as reporting_day,
new_customers as uk_new_customers
FROM UK_REPORTING as UK
LEFT JOIN UK_LAST_DAY as L on UK.date = L.last_date
WHERE date < '2023-12-31'
)
,ROI_DATA AS (
SELECT 
reporting_month as roi_reporting_month,
reporting_day as roi_reporting_day,
new_customers as roi_new_customers,
DATE(reporting_date,'DD/MM/YYYY') as roi_reporting_date
FROM pd2023_wk12_roi_new_customers
)
,MATCHING_UK_DATES AS (
SELECT 
reporting_month,
reporting_day,
date as reporting_date,
uk_new_customers,
COALESCE(roi_new_customers,0) as roi_new_customers,
roi_reporting_month
FROM UK_REPORTING_ADJ as UK
LEFT JOIN ROI_DATA as ROI on UK.date = ROI.roi_reporting_date
)
,ROI_DATA_ADJ AS (
SELECT 
roi_reporting_month,
roi_reporting_day,
roi_new_customers,
roi_reporting_date,
MIN(UK2.date) as next_uk_date
FROM ROI_DATA as ROI
LEFT JOIN UK_REPORTING_ADJ as UK on UK.date = ROI.roi_reporting_date
LEFT JOIN UK_REPORTING_ADJ as UK2 on UK2.date > ROI.roi_reporting_date
WHERE UK.date IS NULL
GROUP BY 
roi_reporting_month,
roi_reporting_day,
roi_new_customers,
roi_reporting_date
)
,COMBINED AS (
SELECT 
reporting_month,
reporting_day,
date as reporting_date,
0 as uk_new_customers,
roi_new_customers,
roi_reporting_month
FROM ROI_DATA_ADJ as ROI
INNER JOIN UK_REPORTING_ADJ as UK on UK.date = ROI.next_uk_date

UNION ALL

SELECT *
FROM MATCHING_UK_DATES
)
SELECT 
CASE 
WHEN roi_reporting_month IS NULL THEN 'x'
WHEN LEFT(reporting_month,3) <> LEFT(roi_reporting_month,3) THEN 'x'
ELSE '' 
END as misalignment_flag,
reporting_month,
reporting_day,
reporting_date,
SUM(uk_new_customers) as uk_new_customers,
SUM(roi_new_customers) as roi_new_customers,
roi_reporting_month
FROM COMBINED
GROUP BY 
CASE 
WHEN roi_reporting_month IS NULL THEN 'x'
WHEN LEFT(reporting_month,3) <> LEFT(roi_reporting_month,3) THEN 'x'
ELSE '' 
END,
reporting_month,
reporting_day,
reporting_date,
roi_reporting_month;
