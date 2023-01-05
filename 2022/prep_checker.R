#install.packages("dplyr")
library(dplyr)

tb_prep <- read.csv('C:/Users/WillSutton/Documents/GitHub/preppin-data/2022/tableau_prep_flows/outputs/PD_2022_WK4.csv',stringsAsFactors = F)
alteryx <- read.csv('C:/Users/WillSutton/Documents/GitHub/preppin-data/2022/alteryx_workflows/outputs/PD_2022_WK5.csv',stringsAsFactors = F)
python <- read.csv('C:/Users/WillSutton/Documents/GitHub/preppin-data/2022/prepped_data/PD 2022 Wk 2 Output.csv',stringsAsFactors = F)
solution <- read.csv('C:/Users/WillSutton/Documents/GitHub/preppin-data/2022/solutions/PD 2022 Wk 5 Output.csv',stringsAsFactors = F)

setdiff(tb_prep,solution)
#setdiff(python,solution)
#setdiff(alteryx,solution)

alteryx <- arrange(alteryx,Number.of.Trips)
#python <- arrange(python,Pupil.Name)
solution <- arrange(solution,Number.of.Trips)

alteryx <- arrange(alteryx,Method.of.Travel)
#python <- arrange(python,Pupil.Name)
solution <- arrange(solution,Method.of.Travel)

solution$Date.of.Birth <- as.Date(solution$Date.of.Birth, format = "%d/%m/%Y")
solution$This.Year.s.Birthday <- as.Date(solution$This.Year.s.Birthday, format = "%d/%m/%Y")

alteryx$Date.of.Birth <- as.Date(alteryx$Date.of.Birth, format = "%Y-%m-%d")
alteryx$This.Year.s.Birthday <- as.Date(alteryx$This.Year.s.Birthday, format = "%Y-%m-%d")

setdiff(alteryx,solution)

python$Date.of.Birth <- as.Date(alteryx$Date.of.Birth, format = "%Y-%m-%d")
python$This.Year.s.Birthday <- as.Date(alteryx$This.Year.s.Birthday, format = "%Y-%m-%d")

setdiff(python,solution)


