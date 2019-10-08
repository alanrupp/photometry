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
  save_fn <- function(df, plottype, grouped = FALSE) {
    return_plot(df, input$plottype, 
                  xmin = input$xmin, xmax = input$xmax,
                  ymin = input$ymin, ymax = input$ymax,
                grouped = grouped)
  }
  output$save_plot <- downloadHandler(
    filename = "plot.png",
    content = function(file) {
      ggsave(file, plot = save_fn(filedata(), input$plottype), 
             dpi = 600, units = "in",
             width = input$width, height = input$height)
    }
  )
  
  # - Group info --------------------------------------------------------------
  counter <- reactiveValues(n = 0)
  
  observeEvent(input$add_btn, {counter$n <- counter$n + 1})
  observeEvent(input$rm_btn, {
    if (counter$n > 0) counter$n <- counter$n - 1
  })
  
  groupUI <- reactive({
    df <- filedata()
    mice <- colnames(df)[colnames(df) != "TIMErel"]
    if (counter$n > 0) {
      map(seq(counter$n), 
          ~ fluidRow(
            column(width = 6, 
                   textInput(paste0("group", .x), paste("Group", .x))
                   ),
            column(width = 6, 
                   selectizeInput(paste0("mice", .x), "Mice", choices = mice,
                                  multiple = TRUE)
                   )
            )
      )
    }
  })
  
  output$groupInfo <- renderUI({ groupUI() })
  
  # - Group data --------------------------------------------------------------
  observeEvent(input$avg, {
    df <- filedata()
    if (!"sample" %in% colnames(df)) {
      df <- gather(df, -TIMErel, key = "sample", value = "value")
    }
    if (counter$n > 0) {
      group_ids <- map_chr(seq(counter$n), ~ paste0("group", .x))
      group_names <- map_chr(group_ids, ~ input[[.x]])
      groups <- map(seq(counter$n), ~ input[[paste0("mice", .x)]])
      names(groups) <- group_names
      groups <- unlist(groups) %>% as.data.frame() %>%
        rownames_to_column("Group") %>%
        rename("sample" = ".") %>%
        mutate(Group = str_remove(Group, "[0-9]$"))
      df <- left_join(df, groups, by = "sample")
      df <- summarize_groups(df)
      
      # - Plot and save
      output$plot <- renderPlot(
        return_plot(df, input$plottype, 
                    xmin = input$xmin, xmax = input$xmax,
                    ymin = input$ymin, ymax = input$ymax,
                    grouped = TRUE)
      )
      output$save_plot <- downloadHandler(
        filename = "plot.png",
        content = function(file) {
          ggsave(file, plot = save_fn(df, input$plottype, grouped = TRUE), 
                 dpi = 600, units = "in",
                 width = input$width, height = input$height)
        }
      )
    } 
  })
  
})