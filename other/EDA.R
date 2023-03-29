library(ggplot2)
library(dplyr)
library(magrittr)
library(lubridate)
library(tidyverse)
library(plotly)
library(tidyquant)



# Load the CSV file into a data frame
df <- read.csv(
  'C:\\Users\\javi2\\Documents\\CD_aplicada_1\\COBI\\data\\arribos_BC_17_21.csv',
  fileEncoding = "latin1")

# Print the first 5 rows of the data frame
head(df)

# Get the dimensions of the data frame
dim(df)

# Get information about the columns
str(df)

# Get basic statistics about the data frame
summary(df)

# Get the number of unique values in each column
sapply(df, function(x) length(unique(x)))

# Check for missing values in the data frame
colSums(is.na(df))

# Fechas:
#convert character to date format
df$PESO.DESEMBARCADO <- as.numeric(df$PESO.DESEMBARCADO)
df$date <- mdy(df$FECHA.EXPEDICION)

# Días con menos pesos desembarcados (abajo del 1er cuartil)
df_days = df %>% 
  group_by(date) %>%
  summarise(mean = mean(PESO.DESEMBARCADO, na.rm = TRUE))
df_days$month <- format(df_days$date, '%m-%Y')
df_days = df_days[df_days$date > "2006-01-01" & df_days$date < "2024-01-01", ]
df_days = df_days[df_days$mean < quantile(df_days$mean, c(.25), na.rm=TRUE), ]
df_days = df_days[order(df_days$date, df_days$mean),]

# Días con pesos desembarcados arriba del 1er cuartil
df_days = df %>% 
  group_by(date) %>%
  summarise(mean = mean(PESO.DESEMBARCADO, na.rm = TRUE))
df_days$month <- format(df_days$date, '%m-%Y')
df_days = df_days[df_days$date > "2006-01-01" & df_days$date < "2024-01-01", ]
df_days = df_days[df_days$mean >= quantile(df_days$mean, c(.25), na.rm=TRUE), ]
df_days = df_days[order(df_days$date, df_days$mean),]

