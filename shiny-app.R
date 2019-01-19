library(shiny)
library(leaflet)
library(shinythemes)
library(leaflet.extras)
library(tidyverse)

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

## UI ----------------------------------

ui <- fluidPage(
  navbarPage("nicheRecommender", tabPanel("Map"), tabPanel("Data"), tabPanel("Plots")),
  theme = shinytheme("united"),
  leafletOutput("mymap"),
  p(),
  actionButton("recalc", "New points")
)


## SERVER ----------------------------------

server <- function(input, output, session) {
  dat <- read_csv('C:\\Users\\Mariam\\Documents\\yelp_dataset\\yelp_dataset~\\reviews_v1.csv')
  colnames(dat) = c("name", "rating", "review_count", "latitude", "longitude", "coordinates")
  output$mymap <- renderLeaflet({
    leaflet(data = dat) %>%
      addProviderTiles(providers$Stamen.TonerLite, options = providerTileOptions(noWrap = TRUE)) %>%
      addCircleMarkers(~longitude, ~latitude, clusterOptions = markerClusterOptions()
                       , group="CLUSTER", popup= ~paste('<b><font color="Black">','Restaurant Data','</font></b><br/>', 
                                                        'Name:', name, '<br/>', 'Rating:', rating, '<br/>', 'Review Count:', review_count, '<br/>'))
  })
}


## DEPLOY APP ----------------------------------

shinyApp(ui, server, options=list(height=1080))
