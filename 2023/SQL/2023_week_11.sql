-- Preppin' Data 2023 Week 11

-- Append the Branch information to the Customer information
-- Transform the latitude and longitude into radians
-- Find the closest Branch for each Customer
--     Make sure Distance is rounded to 2 decimal places
-- For each Branch, assign a Customer Priority rating, the closest customer having a rating of 1
-- Output the data
WITH CTE AS (
SELECT 
*
,address_long/(180/PI()) as address_long_rads
,address_lat/(180/PI()) as address_lat_rads
,branch_long/(180/PI()) as branch_long_rads
,branch_lat/(180/PI()) as branch_lat_rads
,branch_long/(180/PI()) - address_long/(180/PI()) as difference_in_long
FROM pd2023_wk11_dsb_customer_locations
CROSS JOIN pd2023_wk11_dsb_branches
)
,CLOSEST_BRANCH AS (
SELECT 
branch
,branch_long
,branch_lat
,ROUND(3963 * acos((sin(address_lat_rads) * sin(branch_lat_rads)) + cos(address_lat_rads) * cos(branch_lat_rads) * cos(difference_in_long)),2) as distance
,ROW_NUMBER() OVER(PARTITION BY customer ORDER BY distance ASC) as closest_branch
,ROW_NUMBER() OVER(PARTITION BY branch ORDER BY distance ASC) as customer_priority
,customer
,address_long
,address_lat
FROM CTE
)
SELECT 
branch
,branch_long
,branch_lat
,distance
,customer_priority
,customer
,address_long
,address_lat
FROM CLOSEST_BRANCH
WHERE closest_branch = 1;
