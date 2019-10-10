library(shiny)
library(tidyr)
library(dplyr)
library(ggplot2)

# Server actions to plot data
shinyServer(function(input, output) {
  
  # set up reactive values
  v <- reactiveValues(df = NULL, n = 0, plot = NULL)
  
  # - Read in data ------------------------------------------------------------
  filedata <- reactive({
    infile <- input$fname
    if (is.null(infile)) {
      return(NULL)
    }
    read.csv(infile$datapath, stringsAsFactors = FALSE)
  })
  
  observeEvent(input$fname, {
    isolate({
      v$df <- filedata()
      v$tidy_df <- gather(v$df, -TIMErel, key = "sample", value = "value")
    })
  })
  
  # - Get group info ----------------------------------------------------------
  # generate a new group UI with every push of `+` button
  observeEvent(input$add_btn, {v$n <- v$n + 1})
  observeEvent(input$rm_btn, {
    if (v$n > 0) v$n <- v$n - 1
  })
  
  groupUI <- reactive({
    mice <- colnames(v$df)[colnames(v$df) != "TIMErel"]
    if (v$n > 0) {
      lapply(1:v$n, 
             function(x) fluidRow(
               column(width = 6, 
                      textInput(paste0("group", x), paste("Group", x))
                      ),
               column(width = 6, 
                      selectizeInput(paste0("mice", x), "Mice", choices = mice,
                                     multiple = TRUE)
                      )
               )
             )
      }
    })
  
  output$groupInfo <- renderUI({ groupUI() })
  
  # - Group data --------------------------------------------------------------
  observeEvent(input$avg, {
    validate(
      need(!is.null(v$df), "Upload a dataset")
    )
    if (v$n > 0) {
      group_ids <- sapply(1:v$n, function(x) paste0("group", x))
      group_names <- sapply(group_ids, function(x) input[[x]])
      groups <- lapply(1:v$n, function(x) input[[paste0("mice", x)]])
      names(groups) <- group_names
      groups <- unlist(groups) %>% as.data.frame()
      groups$Group <- rownames(groups)
      colnames(groups) <- c("sample", "Group")
      groups$Group <- gsub("[0-9]$", "", groups$Group)
      v$tidy_df <- left_join(v$tidy_df, groups, by = "sample") 
      v$tidy_df <- summarize_groups(v$tidy_df)
      }
  })
  
  # - Plot data ---------------------------------------------------------------
  observeEvent(input$plot_btn, {
    v$plot <- return_plot(v$tidy_df, input$plottype, 
                          xmin = input$xmin, xmax = input$xmax,
                          ymin = input$ymin, ymax = input$ymax)
    output$plot <- renderPlot(v$plot)
  })
  
  
  # - Save file ---------------------------------------------------------------
  output$save_plot <- downloadHandler(
    filename = "plot.png",
    content = function(file) {
      ggsave(file, plot = v$plot, device = "png",
             width = input$width, height = input$height,
             units = "in", dpi = 600)
    }
  )
  
})