# Define UI for application that plots photometry data
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Photometry data"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      fileInput("fname", "File:"),
      tags$hr(),
      selectizeInput("plottype", "Plot type:", 
                     choices = list(line = "line", heatmap = "tile")),
      fluidRow(column(width = 6, numericInput("xmin", "Min time (s)", -10)),
               column(width = 6, numericInput("xmax", "Max time (s)", NA))
      ),
      fluidRow(column(width = 6, numericInput("ymin", "Min dF/F", NA, step = 0.01)),
               column(width = 6, numericInput("ymax", "Max dF/F", NA, step = 0.01))
      )
    ),
    
    # Show plot and save
    mainPanel(
      fluidRow(
        plotOutput("plot")
      ),
      fluidRow(
        column(width = 2, numericInput("width", "Width", 6)),
        column(width = 2, numericInput("height", "Height", 4)),
        column(width = 2, downloadButton("save_plot", "Save"))
        )
    )
  )
))
