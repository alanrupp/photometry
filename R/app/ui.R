# Define UI for application that plots photometry data
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Photometry data"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      fileInput("fname", "File:"),
      tags$hr(),
      h3("Plot settings"),
      selectizeInput("plottype", "Plot type:", 
                     choices = list(line = "line", heatmap = "tile")),
      fluidRow(column(width = 6, numericInput("xmin", "Min time (s)", -10)),
               column(width = 6, numericInput("xmax", "Max time (s)", NA))
      ),
      fluidRow(column(width = 6, numericInput("ymin", "Min dF/F", NA, step = 0.01)),
               column(width = 6, numericInput("ymax", "Max dF/F", NA, step = 0.01))
      ),
      tags$hr(),
      fluidRow(column(width = 6, h3("Groups")),
               column(width = 2, style = "margin-top: 25px;",
                      textOutput("groupNum")),
               column(width = 2, style = "margin-top: 25px;",
                      actionButton("add_btn", "+")),
               column(width = 2, style = "margin-top: 25px;",
                      actionButton("rm_btn", "-"))
      ),
      uiOutput("groupInfo")
    ),
    
    # Show plot and save
    mainPanel(
      fluidRow(
        plotOutput("plot")
      ),
      fluidRow(
        column(width = 4, numericInput("width", "Width", 6)),
        column(width = 4, numericInput("height", "Height", 4)),
        column(width = 4, style = "margin-top: 25px;",
               downloadButton("save_plot", "Save", width = "100%")
               )
        )
    )
  )
))
