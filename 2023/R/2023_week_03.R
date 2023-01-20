# Preppin' Data Week 2023 03

# load libraries
library(dplyr)
library(tidyr)

# Input the data
tranct_df <- read.csv('2023/unprepped_data/PD 2023 Wk 1 Input.csv', stringsAsFactors = F)
targets_df <- read.csv('2023/unprepped_data/PD 2023 Wk 3 Targets.csv', stringsAsFactors = F)


# For the transactions file:
#  - Filter the transactions to just look at DSB 
#     - These will be transactions that contain DSB in the Transaction Code field
#  - Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
#  - Change the date to be the quarter 
#  - Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person) #
tranct_df <- tranct_df %>% separate(col = Transaction.Code,into = c('Bank'),sep = '-')
tranct_df <- filter(tranct_df,Bank == 'DSB')
tranct_df$Online.or.In.Person <- ifelse(tranct_df$Online.or.In.Person == 1,
                                        'Online','In-Person')

tranct_df$Transaction.Date <- as.Date(tranct_df$Transaction.Date,format = '%d/%m/%Y')
tranct_df$Quarter <- substr(quarters(as.Date(tranct_df$Transaction.Date)), 2, 2)

tranct_df <- tranct_df %>% 
  group_by(Online.or.In.Person, Quarter) %>%
  summarise(Value = sum(Value))
  

# For the targets file:
#  - Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter
#  - Rename the fields
#  - Remove the 'Q' from the quarter field and make the data type numeric 
targets_df <- pivot_longer(targets_df,cols = c('Q1','Q2','Q3','Q4'))
names(targets_df) <- c("Online.or.In.Person","Quarter","Quarterly Targets")
targets_df$Quarter <- gsub('Q','',targets_df$Quarter)

head(targets_df)
# Join the two datasets together 
#  - You may need more than one join clause!

df <- inner_join(tranct_df,targets_df, by = c('Online.or.In.Person','Quarter'))

# Remove unnecessary fields
# Calculate the Variance to Target for each row
df$Variance.to.Target <- df$Value - df$`Quarterly Targets`

# Output the data
names(df) <- gsub('\\.',' ',names(df))
write.csv(df,"2023/R/outputs/pd2023wk03_output.csv",row.names = F)








