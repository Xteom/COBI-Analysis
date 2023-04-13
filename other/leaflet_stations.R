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

icon_red <- makeIcon(iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
                     iconWidth = 25, iconHeight = 41)
icon_blue <- makeIcon(iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
                      iconWidth = 25, iconHeight = 41)
icon_green <- makeIcon(iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
                       iconWidth = 25, iconHeight = 41)
icon_yellow <- makeIcon(iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png",
                        iconWidth = 25, iconHeight = 41)

map <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=df1,
             popup = ~paste(Longitude, Latitude, sep=' '),
             icon=icon_blue,
             group = "Sensores COBI") %>%
  addMarkers(data=df2,
             popup = ~paste(lon, lat, sep=' '),
             icon=icon_blue,
             group = "GlobColour Res 100") %>%
  addMarkers(data=df3,
             popup = ~paste(lon, lat, sep=' '),
             icon=icon_blue,
             group = "Res 4") %>%
  addMarkers(data=df4,
             popup = ~paste(lon, lat, sep=' '),
             icon=icon_blue,
             group = "Copernicus") %>%
  addLayersControl(
    overlayGroups = c("Sensores COBI", "GlobColour Res 100","Res 4","Copernicus")
  ) 

map


