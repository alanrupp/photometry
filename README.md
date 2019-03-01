# Photometry
Tools for processing and analyzing fiber photometry data

## Preprocessing
`preprocess.py` downsamples the dataset to a chosen sampling frequency. It also normalizes the 470 data to the 405 signal, allows data filtering based on time and visual inspection of the raw data. Outputs a CSV with the 405-corrected data.

## Combining
`combine.py` combines multiple samples so their times are equivalent. This allows multiple samples with injections or treatments to be combined into a single file with comparable time values for easier downstream analysis.

## Plotting
`plot.py` plots the results from `combine.py` as either seaborn lineplot or seaborn heatmap.
