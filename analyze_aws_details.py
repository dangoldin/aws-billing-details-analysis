#!/usr/bin/env python

import sys, os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Analyzer():
    def __init__(self, fp, od):
        self.fp = fp
        self.od = od

    def get_opsworks_layers(self):
        return [l.replace('user:opsworks:layer:','') for l in list(self.d.columns.values) if 'user:opsworks:layer:' in l]

    def run(self):
        self.load_file()
        self.add_layer()
        self.add_usage_type_group()
        self.add_instance_type()
        self.plot()

    def load_file(self):
        dtype_cols = {
            'UsageQuantity' : 'float64',
            'Rate' : 'float64',
            'Cost' : 'float64',
        }
        self.d = pd.read_csv(self.fp, dtype=dtype_cols, low_memory=False)

    def add_layer(self):
        d = self.d

        d['layer'] = ''
        for layer in self.get_opsworks_layers():
            d.layer[ d['user:opsworks:layer:' + layer].notnull() ] = layer

    def add_usage_type_group(self):
        d = self.d
        # Get rid of the nan
        all_usage_types = list(x for x in d['UsageType'].unique() if type(x) == str)
        d['usage_type_group'] = ''

        # Simple group assignment using substring
        usage_groups = ['DataTransfer', 'Requests', 'In-Bytes', 'Out-Bytes', 'BoxUsage']
        for usage_type in all_usage_types:
            for usage_group in usage_groups:
                if usage_group in usage_type:
                    d.usage_type_group[ d['UsageType'] == usage_type ] = usage_group
                continue

    def add_instance_type(self):
        d = self.d
        # Extract from usage type which will be like "APS1-BoxUsage:c4.large"
        all_usage_types = list(x for x in d['UsageType'].unique() if type(x) == str)
        d['instance_type'] = ''

        for usage_type in all_usage_types:
            if 'BoxUsage' in usage_type:
                instance_type = usage_type.split(':')[-1]
                d.instance_type[ d['UsageType'] == usage_type ] = instance_type

    def plot(self):
        od = self.od
        d = self.d
        dpi = 200

        if not os.path.exists(od):
            os.makedirs(od)

        # Various plots
        plt.figure()
        d.groupby('layer')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_layer.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('ProductName')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_product_name.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('instance_type')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_instance_type.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_usage_type.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0)[:25].plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_usage_type_top_25.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('usage_type_group')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_usage_type_group.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('user:Name')['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_user_name.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby('user:Name')['Cost'].sum().sort_values(ascending=0)[:25].plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_user_name_top_25.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby(['layer', 'UsageType'])['Cost'].sum().sort_values(ascending=0)[:50].plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_layer_usage_type_top_50.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        d.groupby(['layer', 'usage_type_group'])['Cost'].sum().sort_values(ascending=0).plot(kind='bar', sort_columns=True)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_layer_usage_type_group.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        top_usage_types = list(d.groupby('UsageType')['Cost'].sum().sort_values(ascending=0)[:20].keys())
        d_filtered = d[d['UsageType'].isin(top_usage_types)]
        by_layer_usage = d_filtered.groupby(['layer', 'UsageType'])['Cost'].agg({'Cost': np.sum}).reset_index().sort_values('Cost', ascending=0)[:500]
        by_layer_usage_pivoted = by_layer_usage.pivot(index='layer', columns='UsageType', values='Cost')
        sns.heatmap(by_layer_usage_pivoted)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_layer_usage_type_top_heatmap.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

        plt.figure()
        by_layer_usage_type_group = d_filtered.groupby(['layer', 'usage_type_group'])['Cost'].agg({'Cost': np.sum}).reset_index().sort_values('Cost', ascending=0)[:500]
        by_layer_usage_type_group_pivoted = by_layer_usage_type_group.pivot(index='layer', columns='usage_type_group', values='Cost')
        sns.heatmap(by_layer_usage_type_group_pivoted)
        plt.tight_layout()
        plt.savefig(os.path.join(od, 'by_layer_usage_type_group_heatmap.png'), figsize=(2000/dpi, 2000/dpi), dpi=dpi)

if __name__ == '__main__':
    # File to analyze
    fp = sys.argv[1]
    # Out directory
    if len(sys.argv) == 3:
        od = sys.argv[2]
    else:
        od = 'out'

    a = Analyzer(fp, od)
    a.run()
