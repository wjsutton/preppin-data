# Preppin' Data Week 2023 01

# load libraries
library(dplyr)
library(tidyr)

# Input the data
df <- read.csv('2023\\unprepped_data\\PD 2023 Wk 1 Input.csv')

# Split the Transaction Code to extract the letters at the start of the transaction code. These identify the bank who processes the transaction (help)
# Rename the new field with the Bank code 'Bank'. 
df <- df %>% separate(col = Transaction.Code,into = c('Bank'),sep = '-')

# Rename the values in the Online or In-person field, 
# Online of the 1 values and In-Person for the 2 values. 
df$Online.or.In.Person <- ifelse(df$Online.or.In.Person == 1,'Online','In-Person')

# Change the date to be the day of the week
df$Transaction.Date <- as.Date(df$Transaction.Date,format = '%d/%m/%Y')
df$Transaction.Date <- weekdays(df$Transaction.Date)

# Different levels of detail are required in the outputs. 
# You will need to sum up the values of the transactions in three ways:
# 1. Total Values of Transactions by each bank
output_1 <- df %>% 
  group_by(Bank) %>% 
  summarise(Value = sum(Value))

# 2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
output_2 <- df %>% 
  group_by(Bank,Transaction.Date,Online.or.In.Person) %>% 
  summarise(Value = sum(Value))
names(output_2) <- c('Bank','Transaction Date','Online or In Person','Value')

# 3. Total Values by Bank and Customer Code
output_3 <- df %>% 
  group_by(Bank,Customer.Code) %>% 
  summarise(Value = sum(Value))
names(output_3) <- c('Bank','Customer Code','Value')

# Output each data file
write.csv(output_1,'2023\\R\\outputs\\pd2023wk01_output1.csv',row.names = F)
write.csv(output_2,'2023\\R\\outputs\\pd2023wk01_output2.csv',row.names = F)
write.csv(output_3,'2023\\R\\outputs\\pd2023wk01_output3.csv',row.names = F)

print("data prepped!")

