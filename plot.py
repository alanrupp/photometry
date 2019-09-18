#!/usr/bin/python

'''
Plot photometry data
'''

def read_file(file):
    df = pd.read_csv(file)
    if 'norm' not in df.columns:
        df = df.melt(id_vars='TIMErel', var_name='sample', value_name='norm')
    return df

def plot(df, plottype):
    if plottype == 'line':
        sns.lineplot(x='TIMErel', y='norm', hue='sample', data=df)
        plt.xlabel('Time (s)')
        plt.ylabel('deltaF/F')
        plt.show()
    if plottype == 'heatmap':
        df['TIMErel'] = df['TIMErel'].apply(lambda x: round(x, 2))
        df = df.pivot(index='TIMErel', columns='sample', values='norm')
        sns.heatmap(df.transpose(), cmap="PiYG")
        plt.xlabel('Time (s)')
        plt.ylabel('deltaF/F')
        plt.show()

# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    import argparse
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import seaborn as sns

    parser = argparse.ArgumentParser(description='Plot data')
    parser.add_argument('file', help='data file from combine.py', type=str)
    parser.add_argument('plottype', help='plot type', type=str)
    parser.add_argument('--treatment', help='treatment name', type=str)
    args = parser.parse_args()

    df = read_file(args.file)
    plot(df, args.plottype)
