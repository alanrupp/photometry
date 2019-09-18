#!/usr/bin/python

'''
Combine multiple files into a single CSV file.
'''

# make sure there are enough start times and files
def check_concordance(files, starts):
    if len(files) > len(starts):
        print('Not enough start times specified')
        exit()
    if len(files) < len(starts):
        print('Not enough files specified')
        exit()

def sampling_check(files):
    freqs = [pd.read_csv(x, nrows=1).Sampling_Freq for x in files]
    samples = [re.findall('[A-Za-z0-9]+(?=\.csv)', file)[0] for file in files]
    df = pd.DataFrame({'samples': samples, 'freqs': freqs})
    if len(set(freqs)) > 1:
        print(f"Different sampling frequencies. Run preprocessing.py again on the samples that are different:\n{df}")
        exit()

# find start time for each mouse
def find_start(df, start):
    diff = df['TIME'] - start
    return(diff.abs().idxmin())

# normalize data by start time
def normalize(file, idx):
    file['TIMErel'] = file['TIME'] - file.at[idx, 'TIME']

# find shortest possible time interval with data from all samples
def find_time_limits(df):
    min_time = df.groupby('sample')['TIMErel'].min().max()
    max_time = df.groupby('sample')['TIMErel'].max().min()
    return(min_time, max_time)

def merge_times(df):
    samples = df['sample'].unique()
    reference = samples[0]
    offset_test = df[df['sample'] == reference].head(3).reset_index()
    def find_offset(df, sample):
        other = df[df['sample'] == sample].head(3)
        timediff = []
        for i, df in other.iterrows():
            timediff.append(df['TIMErel'] - offset_test['TIMErel'])
        closest = [abs(x).idxmin() for x in timediff]
        diffs = closest - np.arange(3)
        return pd.Series(diffs).value_counts().idxmax()
    offsets = [find_offset(df, sample) for sample in samples]
    for i in np.arange(len(samples)):
        df.loc[df['sample'] == samples[i], 'idx'] = np.arange(len(df[df['sample'] == samples[i]])) + offsets[i]
    return df

def spread(df):
    # check that there are equal points in each sample
    pts = df.groupby('sample')['TIMErel'].count()
    def reshape(df):
        min_time = df['TIMErel'].min()
        max_time = df['TIMErel'].max()
        df = df.pivot(index='idx', columns='sample', values='norm')
        new_time = np.arange(min_time, max_time, (max_time-min_time)/len(df))
        df['TIMErel'] = new_time
        return df
    if len(set(pts)) > 1:
        df = merge_times(df)
        df = reshape(df)
    else:
        samples = df['sample'].unique()
        for i in np.arange(len(samples)):
            df.loc[df['sample'] == samples[i], 'idx'] = np.arange(len(df[df['sample'] == samples[i]]))
        df = reshape(df)
    df.set_index('TIMErel', inplace=True)
    return df


# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    import argparse
    import numpy as np
    import pandas as pd
    import re

    parser = argparse.ArgumentParser(description='Combine preprocessed files into one')
    parser.add_argument('--files', help='files to combine', type=str, nargs='*')
    parser.add_argument('--starts', help='time zero for each sample', type=int, nargs='*')
    parser.add_argument('--outfile', help='filename for combined CSV file', \
                        default='combined.csv')
    parser.add_argument('--tidy', help='output in tidy data format',
                        action='store_true')
    args = parser.parse_args()

    check_concordance(args.files, args.starts)
    sampling_check(args.files)
    samples = [re.findall('[A-Za-z0-9]+(?=\.csv)', file)[0] for file in args.files]
    # initialize a dataframe to put the data into
    combined = pd.DataFrame()
    for i in range(len(args.files)):
        df = pd.read_csv(args.files[i])
        start = find_start(df, args.starts[i])
        normalize(df, start)
        df['sample'] = samples[i]
        df = df[['TIMErel', 'sample', 'norm']]
        combined = pd.concat([combined, df])

    combined = combined.reset_index()
    combined.drop('index', axis=1, inplace=True)

    # filter by min and max time
    min_time, max_time = find_time_limits(combined)
    combined = combined[(combined['TIMErel'] >= min_time) & \
                        (combined['TIMErel'] <= max_time)]

    # spread data for easier viewing and export to CSV
    if not args.tidy:
        combined = spread(combined)
        combined.to_csv(args.outfile)
    else:
        combined.to_csv(args.outfile, index=False)
