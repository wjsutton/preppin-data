# Preppin' Data 2023 Week 04

# Load packages
library(dplyr)
library(tidyr)
library(readxl)

# Input the data
# We want to stack the tables on top of one another, since they have the same fields in each sheet.
# Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these fields together
sheet_names <- excel_sheets('2023/unprepped_data/PD 2023 Wk 4 New Customers.xlsx')

# loop over all tabs in excel file into one dataframe
my_data <- list()
for (i in seq_along(sheet_names)) {
  df <- read_excel('2023/unprepped_data/PD 2023 Wk 4 New Customers.xlsx',sheet = sheet_names[i])
  names(df) <- c('ID','Joining Day','Demographic','Value')
  df['sheet_name'] <- sheet_names[i]
  my_data[[i]] <- df
}

big_data <- dplyr::bind_rows(my_data)

# Make a Joining Date field based on the Joining Day, Table Names and the year 2023
big_data$joining_month <- as.numeric(factor(as.character(big_data$sheet_name), levels = month.name))
big_data$joining_date <- as.Date(paste0(2023,'-',big_data$joining_month,'-',big_data$`Joining Day`))

# Now we want to reshape our data so we have a field for each demographic, for each new customer
big_data <- big_data[,c('ID','joining_date','Demographic','Value')]
df_pivot <- tidyr::pivot_wider(big_data,id_cols = c('ID','joining_date'),names_from = 'Demographic',values_from = 'Value')

# Make sure all the data types are correct for each field
df_pivot$ID <- as.integer(df_pivot$ID)
df_pivot$`Date of Birth`<- as.Date(df_pivot$`Date of Birth`,format = '%m/%d/%Y')

# Remove duplicates
# If a customer appears multiple times take their earliest joining date
df_pivot <- df_pivot %>% group_by(ID) %>%
  mutate(rank = rank(joining_date)) %>%
  arrange(joining_date)

df_pivot <- filter(df_pivot,rank == 1)

# Output the data
df_pivot <- df_pivot[,1:5]
names(df_pivot)[2] <- 'Joining Date'

write.csv(df_pivot,"2023/R/outputs/pd2023wk04_output.csv",row.names = F)




