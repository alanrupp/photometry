#!/usr/bin/python

'''
Plot photometry data
'''

def read_file(file):
    df = pd.read_csv(file)
    if 'norm' not in df.columns:
        df = df.melt(id_vars='TIMErel', var_name='sample', value_name='norm')
    return df

def summarize(df, group_file):
    groups = pd.read_csv(group_file)
    df = df.join(groups.set_index('sample'), on='sample')
    df = df.groupby(['TIMErel','group'])['norm'].mean().reset_index()
    return df

def plot(df, plottype, fname, grouping_var=None):
    if plottype == 'line':
        sns.lineplot(x='TIMErel', y='norm', hue=grouping_var, data=df)
        plt.xlabel('Time (s)')
        plt.ylabel('deltaF/F')
        plt.show()
    if plottype == 'heatmap':
        df = df.pivot(index='TIMErel', columns='sample', values='norm')
        sns.heatmap(df.transpose(), cmap="PiYG")
        plt.xlabel('Time (s)')
        plt.ylabel('deltaF/F')
    plt.savefig(fname)

# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    import argparse
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import seaborn as sns

    parser = argparse.ArgumentParser(description='Plot data')
    parser.add_argument('file', help='data file from combine.py', type=str)
    parser.add_argument('plottype', help='plot type: "line" or "heatmap"', type=str)
    parser.add_argument('-xlim', help='x-axis limits, passed as 2 numbers (example: -xlim -10 100)')
    parser.add_argument('-plotsize', help='figure size in inches (example: -figsize 4 3)',
                        default=[6, 4])
    parser.add_argument('-plotname', help='figure name (example: heatmap.png)',
                        default='plot.png')
    parser.add_argument('-groups', help='groups file', default=None)
    args = parser.parse_args()

    # configure plot
    plt.rcParams["figure.figsize"] = [args.plotsize[0], args.plotsize[1]]
    plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'Tahoma', 'DejaVu Sans']
    plt.rcParams['font.family'] = "sans-serif"

    # read in data and plot
    df = read_file(args.file)
    if args.groups is not None:
        df = summarize(df, args.groups)
        plot(df, args.plottype, args.plotname, 'group', args.plotname)
    else:
        plot(df, args.plottype, args.plotname)
