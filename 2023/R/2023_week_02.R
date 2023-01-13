# Preppin' Data Week 2023 02

# load libraries
library(dplyr)

# Input the data
transct_df <- read.csv('2023\\unprepped_data\\PD 2023 Wk 2 Transactions.csv')
swift_df <- read.csv('2023\\unprepped_data\\PD 2023 Wk 2 Swift Codes.csv')

# In the Transactions table, there is a Sort Code field which 
# contains dashes. We need to remove these so just have a 6 digit string 
transct_df$Sort.Code <- gsub('-','',transct_df$Sort.Code)

# Use the SWIFT Bank Code lookup table to bring in additional 
# information about the SWIFT code and Check Digits of the receiving bank account
df <- inner_join(transct_df,swift_df, by = 'Bank')

# Add a field for the Country Code
# Hint: all these transactions take place in the UK so the Country Code should be GB
df$Country.Code <- 'GB'

# Create the IBAN as above
# Hint: watch out for trying to combine sting fields with numeric fields - check data types
df$IBAN <- paste0(df$Country.Code,df$Check.Digits,df$SWIFT.code,df$Sort.Code,df$Account.Number)

# Remove unnecessary fields
output_df <- df[,c('Transaction.ID','IBAN')]

# using gsub '\\.' to remove dots in column names
names(output_df) <- gsub('\\.',' ',names(output_df))

# Output the data
write.csv(output_df,'2023\\R\\outputs\\pd2023wk02_output.csv',row.names = F)

