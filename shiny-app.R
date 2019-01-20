library(shiny)
library(leaflet)
library(shinythemes)
library(leaflet.extras)
library(tidyverse)
library(reticulate)

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

use_python("C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\python.exe")
source_python('data.py')


## UI ----------------------------------

ui <- fluidPage(
  navbarPage("nicheRecommender", tabPanel("Map"), tabPanel("Data"), tabPanel("Plots")),
  theme = shinytheme("united"),
  leafletOutput("mymap", height = "95vh"),
  p(), textInput("text", label = h3("Enter your city:"), value = "Enter text..."), 
  actionButton("go", "Go"),
  hr(), fluidRow(column(3, verbatimTextOutput("value"))))



## SERVER ----------------------------------

server <- function(input, output, session) {
  observeEvent(input$go, {
    print("Doing something")
    x <- (input$text)
    result <- get_data(x)
    print(result)
    
    
    dat <- read_csv('C:\\Users\\Max\\Documents\\GitHub\\nicheRecommender\\results.csv')
    colnames(dat) = c("name", "rating", "review_count", "latitude", "longitude")
    output$mymap <- renderLeaflet({
      leaflet(data = dat) %>%
        addProviderTiles(providers$Stamen.TonerLite, options = providerTileOptions(noWrap = TRUE)) %>%
        addCircleMarkers(~longitude, ~latitude, clusterOptions = markerClusterOptions()
                         , group="CLUSTER", popup= ~paste('<b><font color="Black">','Restaurant Data','</font></b><br/>', 
                                                          'Name:', name, '<br/>', 'Rating:', rating, '<br/>', 'Review Count:', review_count, '<br/>'))
    })
  })
  
}


## DEPLOY APP ----------------------------------

shinyApp(ui, server, options=list(height=1080))
