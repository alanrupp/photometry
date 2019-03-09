import argparse
import numpy as np
import pandas as pd
import re

parser = argparse.ArgumentParser(description='Combine preprocessed files into one')
parser.add_argument('--files', help='files to combine', type=str, nargs='*')
parser.add_argument('--starts', help='time zero for each sample', type=int, nargs='*')
parser.add_argument('--outfile', help='filename for combined CSV file', \
                    default='combined.csv')
args = parser.parse_args()

# make sure there are enough start times and files
def check_concodance(files, starts):
    if len(files) > len(starts):
        print('Not enough start times specified')
        exit()
    if len(files) < len(starts):
        print('Not enough files specified')
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

# reduce the dataset so all samples have the same number of points
def keep_equal_points(df):
    less_than = df.groupby('sample')['TIMErel'].agg(lambda x: sum(x < 0))
    more_than = df.groupby('sample')['TIMErel'].agg(lambda x: sum(x > 0))
    if len(set(less_than)) > 1:
        less_than = less_than - min(less_than)
        for i in less_than:
            if int(less_than[i]) != 0:
                to_drop = df[df['sample'] == less_than.index[i]]['TIMErel'].nlargest(int(less_than[i])).index
                df = df.drop(to_drop)
    if len(set(more_than)) > 1:
        more_than = more_than - min(more_than)
        for i in range(len(more_than)):
            if int(more_than[i]) != 0:
                to_drop = df[df['sample'] == more_than.index[i]]['TIMErel'].nlargest(int(more_than[i])).index
                df = df.drop(to_drop)
    return(df)

def spread(df):
    # check that there are equal points in each sample
    pts = df.groupby('sample')['TIMErel'].count()
    if len(set(pts)) > 1:
        df = keep_equal_points(df)
    # match times for each sample
    n_pts = int(df.groupby('sample')['TIMErel'].count().unique())
    n_samples = len(df['sample'].unique())
    time = df['TIMErel'].iloc[:n_pts]
    time = time.tolist() * 3
    df['TIMErel'] = time
    # spread data
    df = df.pivot(index='TIMErel', columns='sample', values='norm')
    return(df)


# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    check_concodance(args.files, args.starts)
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

    combined = spread(combined)

    # write to csv
    combined.to_csv(args.outfile)
