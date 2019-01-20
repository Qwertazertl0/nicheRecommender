library(shiny)
library(leaflet)
library(shinythemes)
library(leaflet.extras)
library(tidyverse)
library(reticulate)

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

# use_python("C:\\Users\\Mariam\\AppData\\Local\\Programs\\Python\\Python37\\python3.exe")
# source_python("C:\\Users\\steph\\Dropbox\\nicheRecommender\\data.py")


## UI ----------------------------------

ui <- fluidPage(
  navbarPage("nicheRecommender", tabPanel("Map"), tabPanel("Data"), tabPanel("Plots")),
  theme = shinytheme("united"),
  leafletOutput("mymap", height = "95vh"),
  p(), textInput("text", label = h3("Enter your city:"), value = ""),
  actionButton("go", "Go"),
  hr(), fluidRow(column(3, verbatimTextOutput("value")))  )

#, get_data("text")

## SERVER ----------------------------------

server <- function(input, output, session) {
  
  observeEvent( input$go,{
    x <- (input$text)
    print(x)
  })
  
  dat <- read_csv('C:\\Users\\steph\\Dropbox\\nicheRecommender\\results.csv')
  colnames(dat) = c("name", "rating", "review_count", "latitude", "longitude")
  
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
