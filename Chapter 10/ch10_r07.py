"""Python Cookbook

Chapter 10, recipe 7.
"""

from pathlib import Path
import json
from collections import OrderedDict

if __name__ == "__main__":
    source_path = Path('anscombe.json')
    data = json.loads(source_path.read_text(),
        object_pairs_hook=OrderedDict)


import statistics

def absdev(data, median=None):
    if median is None:
        median = statistics.median(data)
    return (
        abs(x-median) for x in data
    )

def median_absdev(data, median=None):
    if median is None:
        median = statistics.median(data)
    return statistics.median(absdev(data, median=median))

def z_mod(data):
    median = statistics.median(data)
    mad = median_absdev(data, median)
    return (
        0.6745*(x - median)/mad for x in data
    )


import itertools

def pass_outliers(data):
    return itertools.compress(data, (z >= 3.5 for z in z_mod(data)))

def reject_outliers(data):
    return itertools.compress(data, (z < 3.5 for z in z_mod(data)))

from pprint import pprint
# for series in data:
#     pprint(series)

if __name__ == "__main__":

    for series_name in 'I', 'II', 'III', 'IV':
        print(series_name)
        series_data = [series['data'] for series in data if series['series'] == series_name][0]
        for variable_name in 'x', 'y':
            variable = [float(item[variable_name]) for item in series_data]
            print(variable_name, variable, end=' ')
            try:
                print( "outliers", list(pass_outliers(variable)))
            except ZeroDivisionError:
                print( "Data Appears Linear")
        print()
