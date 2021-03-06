library(shiny)
library(tidyr)
library(dplyr)
library(ggplot2)
options(bitmapType = "cairo")

# - Global plot settings ------------------------------------------------------
plot_settings <- list(
  geom_vline(aes(xintercept = 0)),
  xlab("Time (s)"),
  theme_classic(),
  theme(axis.text = element_text(color = "black"))
)

# - Return plot ---------------------------------------------------------------
return_plot <- function(df, plottype = "line", 
                        xmin = NA, xmax = NA, ymin= NA, ymax = NA) {
  if (is.null(df)) {
    return(NULL)
  }
  
  # detect if grouped
  grouped <- ifelse("Group" %in% colnames(df), TRUE, FALSE)
  
  # main plot
  p <- ggplot(df, aes(x = TIMErel)) +
    scale_x_continuous(limits = c(xmin, xmax), expand = c(0, 0))

  # - Line or 
  if (plottype == "line") {
    p <- p + 
      geom_hline(aes(yintercept = 0)) +
      ylab(sprintf("\u0394F/F")) +
      scale_y_continuous(expand = c(0, 0), limits = c(ymin, ymax))
    if (grouped) {
      p <- p + geom_line(aes(y = avg, color = Group)) +
        geom_ribbon(aes(ymin = avg - sem, ymax = avg + sem, fill = Group), 
                    alpha = 0.3, show.legend = FALSE)
    } else {
      p <- p + geom_line(aes(y = value, color = sample))
    }
  } else if (plottype == "tile") {
    p <- p +
      scale_fill_gradient2(low = "#d0587e", mid = "white", high = "#009392",
                           name = sprintf("\u0394F/F"),
                           na.value = "white",
                           limits = c(ymin, ymax)) +
      scale_y_discrete(expand = c(0, 0)) +
      ylab(NULL)
    if (grouped) {
      p <- p + geom_tile(aes(y = Group, fill = avg))
    } else {
      p <- p + geom_tile(aes(y = sample, fill = value))
    }
  }
  p <- p + plot_settings
  return(p)
}

# - Summarize groups ----------------------------------------------------------
summarize_groups <- function(df) {
  df <- group_by(df, Group, TIMErel) 
  df <- summarize(df, "avg" = mean(value, na.rm = TRUE),
                  "sem" = sd(value, na.rm = TRUE) / sqrt(n()))
}

# - Downsample ----------------------------------------------------------------
downsample <- function(df) {
  df <- mutate(df, TIMErel = as.integer(TIMErel))
  df <- group_by(df, sample, TIMErel)
  df <- summarize(df, "value" = mean(value, na.rm = TRUE))
  df <- ungroup(df)
  return(df)
}
