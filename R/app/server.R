# Server actions to plot data
shinyServer(function(input, output) {
  
  # - Read in data ------------------------------------------------------------
  filedata <- reactive({
    infile <- input$fname
    if (is.null(infile)) {
      return(NULL)
    }
    read_csv(infile$datapath)
  })
  
  # - Plot data ---------------------------------------------------------------
  output$plot <- renderPlot(
    return_plot(filedata(), input$plottype, 
                  xmin = input$xmin, xmax = input$xmax,
                  ymin = input$ymin, ymax = input$ymax)
  )
  
  # - Save file ---------------------------------------------------------------
  save_fn <- function(plottype) {
    return_plot(filedata(), input$plottype, 
                  xmin = input$xmin, xmax = input$xmax,
                  ymin = input$ymin, ymax = input$ymax)
  }
  output$save_plot <- downloadHandler(
    filename = "plot.png",
    content = function(file) {
      ggsave(file, plot = save_fn(input$plottype), dpi = 600, units = "in",
             width = input$width, height = input$height)
    }
  )
 
})