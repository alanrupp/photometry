#!/usr/bin/python

'''
Plot photometry data
'''

def read_file(file):
    df = pd.read_csv(file)
    if 'norm' not in df.columns:
        df = df.melt(id_vars='TIMErel', var_name='sample', value_name='norm')
    return df

def add_group_info(df, group_file):
    groups = pd.read_csv(group_file)
    df = df.join(groups.set_index('sample'), on='sample')
    return df

def round_time(df):
    freq = 1/((df['TIMErel'].max()-df['TIMErel'].min())/\
              df.groupby('sample')['TIMErel'].count()[0])
    freq = int(round(freq, 0))
    decimals = len(str(1/freq).split('.')[1])
    df['TIMErel'] = df['TIMErel'].apply(lambda x: round(x, decimals))
    return df

def plot(df, plottype, fname, grouping_var=None):
    print(f"Plotting {plottype} and saving as {fname}. Be patient, this takes time.")
    plt.axhline(y=0, color='black')
    plt.axvline(x=0, color='black')
    if plottype == 'lineplot':
        sns.lineplot(x='TIMErel', y='norm', hue=grouping_var, data=df)
        plt.ylabel('\u0394F/F')
    elif plottype == 'heatmap':
        df = df.pivot(index='TIMErel', columns='sample', values='norm')
        sns.heatmap(df.transpose(), cmap="PiYG", cbar_kws={'label': '\u0394F/F'})
    plt.xlabel('Time (s)')
    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.savefig(fname, dpi=600, pad_inches=0)

# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    import argparse
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    from matplotlib.ticker import StrMethodFormatter
    import seaborn as sns

    # parse arguments
    parser = argparse.ArgumentParser(description='Plot data')
    parser.add_argument('file', help='data file from combine.py', type=str)
    parser.add_argument('plottype', help='plot type: "lineplot" or "heatmap"',
                        type=str)
    parser.add_argument('-xmin', help='x-axis min (example: -xmin -10',
                        default=None)
    parser.add_argument('-xmax', help='x-axis max (example: -xmax 100)',
                        default=None)
    parser.add_argument('-width', help='figure height in inches (example: -width 5)',
                        default=6)
    parser.add_argument('-height', help='figure height in inches (example: -height 5)',
                        default=4)
    parser.add_argument('-filename', help='file name (example: -filename heatmap.png)',
                        default='plot.png')
    parser.add_argument('-groups', help='grouping file (*.csv)', default=None)
    args = parser.parse_args()

    # configure plot universals
    plt.rcParams["figure.figsize"] = [args.width, args.height]
    plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'Unica', 'Imago',
                                       'Rail Alphabet', 'Tahoma', 'DejaVu Sans']
    plt.rcParams['font.family'] = "sans-serif"
    grouping_var=None

    # read in data
    df = read_file(args.file)

    # filter data by plotting axis min and max
    if args.xmin is not None:
        df = df[df['TIMErel'] >= int(args.xmin)]
    if args.xmax is not None:
        df = df[df['TIMErel'] <= int(args.xmax)]

    # round data for easier viewing during plotting
    df = round_time(df)

    # add group info is supplied
    if args.groups is not None:
        df = add_group_info(df, args.groups)
        grouping_var='group'

    # plot
    plot(df, args.plottype, args.filename, grouping_var)
