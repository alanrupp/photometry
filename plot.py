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

def plot(file, type):
    df = pd.read_csv(file)
    if args.plottype == 'line':
        df = df.melt()
        sns.lineplot(x='TIMErel', y='norm', hue='sample', data=df)
        plt.xlabel('Time (s)')
        plt.ylabel('deltaF/F')
        plt.show()

    if args.plottype == 'heatmap':
        sns.heatmap(df.set_index('TIMErel').transpose())
        plt.show()

# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    plot(args.file, args.plottype)
