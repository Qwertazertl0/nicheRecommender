library(shiny)
library(leaflet)
library(shinythemes)
library(leaflet.extras)

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
  points <- eventReactive(input$recalc, {cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)}, ignoreNULL = FALSE)
  output$mymap <- renderLeaflet({
    leaflet() %>%
      addProviderTiles(providers$Stamen.TonerLite, options = providerTileOptions(noWrap = TRUE)) %>%
      addMarkers(data = points())
  })
}
  
## DEPLOY APP ----------------------------------
  
shinyApp(ui, server, options=list(height=1080))
