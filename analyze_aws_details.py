#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_file(fp):
    dtype_cols = {
        'UsageQuantity' : 'float64',
        'Rate' : 'float64',
        'Cost' : 'float64',
    }
    return pd.read_csv(fp, dtype=dtype_cols, low_memory=False)

def get_opsworks_layers(d):
    return [l.replace('user:opsworks:layer:','') for l in list(d.columns.values) if 'user:opsworks:layer:' in l]

def add_layer(d):
    opsworks_layers = get_opsworks_layers(d)

    d['layer'] = ''
    for layer in opsworks_layers:
        d.layer[ d['user:opsworks:layer:' + layer].notnull() ] = layer
    return d

def plot(d):
    dpi = 200

    # Various plots
    plt.figure()
    d.groupby('layer')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_layer.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby('ProductName')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_product_name.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_usage_type.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0)[:25].plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_usage_type_top_25.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby('user:Name')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_user_name.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby('user:Name')['Cost'].sum().sort_values(ascending=0)[:25].plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_user_name_top_25.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    d.groupby(['layer', 'UsageType'])['Cost'].sum().sort_values(ascending=0)[:50].plot(kind='bar', sort_columns=True)
    plt.tight_layout()
    plt.savefig('by_layer_usage_type_top_50.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

    plt.figure()
    top_usage_types = list(d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0)[:20].keys())
    d_filtered = d[d['UsageType'].isin(top_usage_types)]
    by_layer_usage = d_filtered.groupby(['layer', 'UsageType'])['Cost'].agg({'Cost': np.sum}).reset_index().sort_values('Cost', ascending=0)[:500]
    by_layer_usage_pivoted = by_layer_usage.pivot(index='layer', columns='UsageType', values='Cost')
    sns.heatmap(by_layer_usage_pivoted)
    plt.tight_layout()
    plt.savefig('by_layer_usage_type_top_heatmap.png', figsize=(2000/dpi, 2000/dpi), dpi=dpi)

if __name__ == '__main__':
    fp = sys.argv[1]

    d = load_file(fp)
    d = add_layer(d)
    plot(d)
