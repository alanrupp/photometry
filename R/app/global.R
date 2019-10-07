library(shiny)
library(tidyverse)
options(bitmapType = "cairo")

plot_settings <- list(
  theme_classic(),
  xlab("Time (s)"),
  geom_vline(aes(xintercept = 0))
)

return_plot <- function(df, plottype = "line", 
                        xmin = input$xmin, xmax = input$xmax,
                        ymin = input$ymin, ymax = input$ymax) {
  df <- gather(df, -TIMErel, key = "sample", value = "value")
  
  p <- ggplot(df, aes(x = TIMErel)) +
    ylab(sprintf("\u0394F/F")) +
    scale_x_continuous(limits = c(xmin, xmax), expand = c(0, 0))

  if (plottype == "line") {
    p <- p + 
      geom_line(aes(y = value, color = sample)) +
      geom_hline(aes(yintercept = 0)) +
      ylab(sprintf("\u0394F/F")) +
      scale_y_continuous(expand = c(0, 0), limits = c(ymin, ymax)) +
      plot_settings
  } else if (plottype == "tile") {
    p <- p +
      geom_tile(aes(y = sample, fill = value)) +
      scale_fill_gradient2(low = "#d0587e", mid = "white", high = "#009392",
                           name = sprintf("\u0394F/F"),
                           na.value = "white",
                           limits = c(ymin, ymax)) +
      scale_y_discrete(expand = c(0, 0)) +
      ylab(NULL) +
      plot_settings
  }
  return(p)
}

tileplot <- function(df, xmin, xmax) {
  df <- gather(df, -TIMErel, key = "sample", value = "value")
  p <- ggplot(df, aes(x = TIMErel, y = sample)) +
    geom_tile(aes(fill = value)) +
    scale_fill_gradient2(low = "#d0587e", mid = "white", high = "#009392",
                         name = sprintf("\u0394F/F"),
                         na.value = "white") +
    plot_settings +
    ylab(NULL) +
    scale_y_discrete(expand = c(0, 0)) +
    scale_x_continuous(limits = c(xmin, xmax), expand = c(0, 0))
  return(p)
}