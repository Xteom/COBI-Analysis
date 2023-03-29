# Leaflet

library(leaflet)

df1 <- read.csv('C:/Users/javi2/Documents/CD_aplicada_1/COBI/data/geo/sensors_stations.csv')

a <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=df1, popup = ~paste(Community, sep=' '))

a

df2 <- read.csv('C:/Users/javi2/Documents/CD_aplicada_1/COBI/data/geo/chl1_measures.csv')

b <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=df2, popup = ~paste(lon, lat, CHL1_mean, sep=' '))

b

df3 <- read.csv('C:/Users/javi2/Documents/CD_aplicada_1/COBI/data/geo/res_4.csv')

c <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=df3, popup = ~paste(lon, lat, sep=' '))

c


df4 <- read.csv('C:/Users/javi2/Documents/CD_aplicada_1/COBI/data/geo/coord_copernicus.csv')

d <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=df4, popup = ~paste(lon, lat, analysed_sst, sep=' '))

d


