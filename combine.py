import argparse
import numpy as np
import pandas as pd
import os
import glob
import re

parser = argparse.ArgumentParser(description='Combine preprocessed files into one')
parser.add_argument('--files', help='files to combine', type=str, nargs='*')
parser.add_argument('--starts', help='time zero for each sample', type=int, nargs='*')
parser.add_argument('--notidy', help='output in tidy format (default=False)', \
                    default=False)
parser.add_argument('--outfile', help='filename for combined CSV file', \
                    default='combined.csv')
args = parser.parse_args()

if len(args.files) > len(args.starts):
    print('Not enough start times specified')
    exit()
if len(args.files) < len(args.starts):
    print('Not enough files specified')
    exit()

def freqs(df):
    freq = list()
    freq.append(df['Sampling_Freq'])

def find_start(file, start):
    diff = file['TIME'] - start
    return(diff.abs().idxmin())

def normalize(file, idx):
    file['TIMErel'] = file['TIME'] - file.at[idx, 'TIME']

def make_tidy(file):
    file = pd.melt()

# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    samples = [re.findall('^[\\S]+', file)[0] for file in args.files]

    combined = pd.DataFrame()
    for i in range(len(args.files)):
        df = pd.read_csv(args.files[i])
        start = find_start(df, args.starts[i])
        normalize(df, start)
        df['sample'] = samples[i]
        df = df[['TIMErel', 'sample', 'norm']]
        combined = pd.concat([combined, df])

    combined.to_csv(args.outfile, index=False)
