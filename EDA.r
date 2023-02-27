library(ggplot2)
library(dplyr)
library(gridExtra)
library(grid)

path <- "C:/Users/mateo/OneDrive - INSTITUTO TECNOLOGICO AUTONOMO DE MEXICO/cobi_data/"

arribos <- read.csv(paste(path, "Arribos2017-2021.csv", sep=""))
sensores <- read.csv(paste(path, "all_sites_miniDOT_data_09_2017-09_2018.csv", sep=""))
glimpse(sensores)

#turn Local_time column(YYYY-MM-DD HH:MM:SS) into date format
sensores$date <- as.POSIXct(sensores$Local_time, format="%Y-%m-%d %H:%M:%S")
sensores$date <- as.Date(sensores$date)

ggplot(sensores, aes(x=date, y=Dissolved.Oxygen, color=Site)) + geom_line() + theme_bw()
ggplot(sensores, aes(x=date, y=Dissolved.Oxygen.Saturation, color=Site)) + geom_line() + theme_bw()
ggplot(sensores, aes(x=date, y=Temperature, color=Site)) + geom_line() + theme_bw()
