# Photometry
Tools for processing and analyzing fiber photometry data

## Preprocessing
`preprocess.py` downsamples the dataset to a chosen sampling frequency. It also normalizes the 470 data to the 405 signal, allows data filtering based on time and visual inspection of the raw data. Outputs a CSV with the 405-corrected data.

Example:
`python [path/to/photometry]/preprocessing.py --s405 G584_091519_405.csv --s470 G584_091519_470.csv --freq 50 --inspect`

## Combining
`combine.py` combines multiple samples so their times are equivalent. This allows multiple samples with injections or treatments to be combined into a single file with comparable time values for easier downstream analysis.

Example:
`python [path/to/photometry]/combine.py --files G584.csv F354.csv --starts 54 68`

## Plotting
`plot.py` plots the results from `combine.py` as either seaborn lineplot or seaborn heatmap.

Example:
`python [path/to/photometry]/plot.py combined.csv "line"`
