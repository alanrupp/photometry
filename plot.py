import argparse
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Plot data')
parser.add_argument('file', help='data file from combine.py', type=str)
parser.add_argument('plottype', help='plot type', type=str,\
                    options=['line','heatmap'])
parser.add_argument('--treatment', help='treatment name', type=str)
args = parser.parse_args()

df = pd.read_csv(args.file)

if args.plottype == 'line':
    sns.lineplot(x='TIMErel', y='norm', hue='sample', data=df)
    plt.xlabel('Time (s)')
    plt.ylabel('deltaF/F')
    plt.show()

if args.plottype == 'heatmap':
    df = df.spread(index='sample', columns='TIMErel', values='norm')
    sns.heatmap(df)
    plt.show()
