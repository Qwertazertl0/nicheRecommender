library(shiny)
library(leaflet)
library(shinythemes)
library(leaflet.extras)
install.packages("RgoogleMaps")
library(RgoogleMaps)

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

## UI ----------------------------------

ui <- fluidPage(
  theme = shinytheme("united"),
  navbarPage("nicheRecommender", tabPanel("Map"), tabPanel("Data"), tabPanel("Plots")),
  leafletOutput("mapPlot"), # leaflet output for plotting points
  p(), 
  actionButton("recalc", "New points"), 
  mainPanel(
    plotOutput(outputId = "lineplot", height = "300px"),
    textOutput(outputId = "desc"),
    tags$a(href = "https://www.google.com/finance/domestic_trends", 
           "Source: Google Domestic Trends", target = "_blank")), fluidRow(column(3,
         h4("Tell us where you want to go."),
         br(),
         checkboxInput('Location'),
         checkboxInput('Categories'))))

## SERVER ----------------------------------

server <- function(input, output, session){
  dat <- read_csv('C:\\Users\\Mariam\\Documents\\yelp_dataset\\yelp_dataset~\\coordinates.csv')
  subsetData <- reactive({
    new_data <- dat[altitu]
  })
  points <- eventReactive(input$recalc, {cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)}, ignoreNULL = FALSE)
  
  output$mymap <- renderLeaflet({
    leaflet(width=400, height=1080) %>% 
      addProviderTiles(providers$Stamen.TonerLite, options = providerTileOptions(noWrap = TRUE)) %>%
      addMarkers(data = points()) %>%
    addTiles() %>%
    addFullscreenControl()
    })}
    
## DEPLOY APP ----------------------------------

shinyApp(ui, server, options=list(height=1080))
