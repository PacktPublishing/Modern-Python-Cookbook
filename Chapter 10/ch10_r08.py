"""Python Cookbook

Chapter 10, recipe 8.
"""

from pathlib import Path
import json
from collections import OrderedDict

if __name__ == "__main__":
    source_path = Path('anscombe.json')
    data = json.loads(source_path.read_text(),
        object_pairs_hook=OrderedDict)


import math
class SimpleStats:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.sum = 0
        self.sum_2 = 0
    def cleanse(self, value):
        return float(value)
    def add(self, value):
        value = self.cleanse(value)
        self.count += 1
        self.sum += value
        self.sum_2 += value*value
    @property
    def mean(self):
        return self.sum / self.count
    @property
    def stdev(self):
        return math.sqrt(
            (self.count*self.sum_2-self.sum**2)/(self.count*(self.count-1))
            )

def analyze(series_data):
    x_stats = SimpleStats('x')
    y_stats = SimpleStats('y')
    column_stats = {
        'x': x_stats,
        'y': y_stats
    }

    for item in series_data:
        for column_name in column_stats:
            column_stats[column_name].add(item[column_name])

    return column_stats

if __name__ == "__main__":

    for series_name in 'I', 'II', 'III', 'IV':
        print(series_name)
        series_data = [series['data'] for series in data if series['series'] == series_name][0]
        column_stats = analyze(series_data)
        for column_key in column_stats:
            print(' ', column_key,
                  column_stats[column_key].mean,
                  column_stats[column_key].stdev)
