import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
import argparse

parser = argparse.ArgumentParser(description='Preprocess photometry data')
parser.add_argument('--s405', help='405 file', type=str)
parser.add_argument('--s470', help='470 file', type=str)
parser.add_argument('--freq', help='sampling frequency for output (Hz)', type=float)
parser.add_argument('--outfile', help='specify output CSV file name')
parser.add_argument('--inspect', help='visually inspect data for filtering', \
                    action='store_true')
parser.add_argument('--time_start', help='time after which data is reliable',
                    default=0)
args = parser.parse_args()

# user input the location of the files
if not args.s405:
    print('\nEnter 405 filename')
    exit()
else:
    s405 = pd.read_csv(args.s405)
if not args.s470:
    print('\nEnter 470 filename')
    exit()
else:
    s470 = pd.read_csv(args.s470)

# check that files are equivalent
if s405.BLOCK[0] != s470.BLOCK[0]:
    print('Error: Files are not equivalent')
    exit()

# extract info from file
if 'TANK' in s470.columns:
    tank = s470.TANK[0]
if 'BLOCK' in s470.columns:
    block = s470.BLOCK[0]
if 'EVENT' in s470.columns:
    event = s470.EVENT[0]
if 'CHAN' in s470.columns:
    chan = s470.CHAN[0]
if 'Sampling_Freq' in s470.columns:
    freq = s470.Sampling_Freq[0]
if 'NumOfPoints' in s470.columns:
    pts = s470.NumOfPoints[0]
column_order = s470.columns

# adjust sampling frequncy
adj_freq = freq / pts
print("\nData loaded! \nRaw data frequency: " + str(round(freq, 2)) + ' Hz')

if freq < args.freq:
    print('Error! Chosen frequency is higher than sampling frequency')
    exit()
elif (args.freq > adj_freq) and (args.freq < freq):
    print('\nDownsampling data to ' + str(args.freq) + ' Hz')
    print('Note: this will be slow. For faster downsampling choose frequency < ' +\
           str(round(adj_freq, 2)) + 'Hz')
    d470 = s470[[col for col in s470.columns if 'D' in col]]
    d470 = np.array(d470).flatten()
    d405 = s405[[col for col in s405.columns if 'D' in col]]
    d405 = np.array(d405).flatten()
    total_pts = len(d470)
    time_ = np.linspace(min(s470.TIME), max(s470.TIME), total_pts)
    bins = pd.cut(time_, bins=len(d470)*args.freq/freq)
    s405 = pd.DataFrame({'TIME': time_, 'D0': d405})\
               .groupby(bins)['TIME', 'D0'].mean()
    s470 = pd.DataFrame({'TIME': time_, 'D0': d470})\
               .groupby(bins)['TIME', 'D0'].mean()
elif args.freq < adj_freq:
    print('\nDownsampling data to ' + str(args.freq) + ' Hz')
    bins = pd.cut(s470['TIME'], bins=len(s470)*args.freq/adj_freq)
    s405 = s405.groupby(bins)['TIME', 'D0'].mean()
    s470 = s470.groupby(bins)['TIME', 'D0'].mean()

# inspect raw data to remove points at beginning
if args.inspect:
    print('\nPlotting data for inspection')
    # downsample to 1 Hz for plotting speed
    plot_freq = 1
    bins = pd.cut(s470['TIME'], bins=len(s470)*plot_freq/args.freq)
    s405_plot = s405.groupby(bins)['TIME', 'D0'].mean()
    s470_plot = s470.groupby(bins)['TIME', 'D0'].mean()
    plt.subplot(1,2,1)
    plt.plot(s405_plot.TIME, s405_plot.D0, '-')
    plt.title("405 raw data")
    plt.subplot(1,2,2)
    plt.plot(s470_plot.TIME, s470_plot.D0, '-')
    plt.title("470 raw data")
    plt.show()

    time_filter = int(input("Start time of valid data: ") or 0)
else:
    time_filter = int(args.time_start)

s405 = s405[s405.TIME >= time_filter]
s470 = s470[s470.TIME >= time_filter]
print('\nFiltering complete')


# - linear regression to 405 data ---------------------------------------------
print('\nRegressing out 405 background')
from sklearn.linear_model import LinearRegression
lm = LinearRegression().fit(X=np.array(s405.D0).reshape(-1,1), y=s470.D0)
s405_scaled = lm.predict(np.array(s405.D0).reshape(-1,1))

# normalize 470 data to scaled 405
s470['norm'] = (s470['D0']-s405_scaled)/s405_scaled
# plotting normalized data (this might be slow for high sample frequencies)
plt.plot(s470.TIME, s470.norm, '-')
plt.axhline(0, color='black')
plt.title("470 normalized")
plt.xlabel('Time (s)')
plt.ylabel('Signal (normalized)')
plt.show()

# - write data to XLSX --------------------------------------------------------
print('\nWriting output to CSV file: ' + args.outfile)
columns_to_keep = list()
if 'TANK' in column_order:
    s470['TANK'] = tank
    columns_to_keep.append('TANK')
if 'BLOCK' in column_order:
    s470['BLOCK'] = block
    columns_to_keep.append('BLOCK')
if 'EVENT' in column_order:
    s470['EVENT'] = event
    columns_to_keep.append('EVENT')
if 'CHAN' in column_order:
    s470['CHAN'] = chan
    columns_to_keep.append('CHAN')
s470['Sampling_Freq'] = args.freq
for item in ['Sampling_Freq', 'TIME', 'D0', 'norm']:
    columns_to_keep.append(item)
s470 = s470[columns_to_keep]
if not args.outfile:
    sample = re.findall('^[A-Za-z0-9]+', file)[0]
    s470.to_csv(f"{sample}.csv", index=False)
else:
    s470.to_csv(args.outfile, index=False)
