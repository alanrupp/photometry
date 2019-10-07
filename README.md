# Photometry
Tools for processing and analyzing fiber photometry data.

## Setup
Go to [Anaconda](https://www.anaconda.com/distribution/) to download and install the Python 3.7 version for your operating system.

Then download this directory using the clone or download button in the upper right. You'll need to unzip the directory to the location where you want to keep the program. Alternatively, you can use `git` to clone the repo with `$ git clone https://github.com/alanrupp/photometry`.

## Preprocessing
`preprocess.py` downsamples the dataset to a chosen sampling frequency. It also normalizes the 470 data to the 405 signal, allows data filtering based on time and visual inspection of the raw data. Outputs a CSV with the 405-corrected data.

Example:
`$ python [path/to/photometry]/preprocessing.py --s405 G584_091519_405.csv --s470 G584_091519_470.csv --freq 50 --inspect`

## Combining
`combine.py` combines multiple samples so their times are equivalent. This allows multiple samples with injections or treatments to be combined into a single file with comparable time values for easier downstream analysis. Just supply the files and the treatment start times (such as time in the recording when an animal was injected)

Example:
`$ python [path/to/photometry]/combine.py --files G584.csv F354.csv --starts 54 68`

## Plotting
The main way to plot data is to use the Shiny app. The source code is in `R/app`. The functional app can be found [here](https://shiny.med.umich.edu/apps/ruppa/photometry).

Alternatively, you can use the command line:
`plot.py` plots the data. Just supply the file from `combine.py` and select the plot type. There are options to change the plot features, for example: output file name (`-filename`), file dimensions (`-height`, `-width`), or plot axis limits (`-xmin`, `-xmax`). Run `python plot.py -h` for more options.

Example:
`$ python [path/to/photometry]/plot.py combined.csv "lineplot"`
