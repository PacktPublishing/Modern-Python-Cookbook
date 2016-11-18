"""Python Cookbook

Chapter 10, recipe 1.
"""

def data_iter(series, variable_name):
    return (item[variable_name] for item in series['data'])

def set_summary(data, function):
    for series in data:
        for variable_name in 'x', 'y':
            samples = data_iter(series, variable_name)
            series[function.__name__+'_'+variable_name] = function(samples)

from pathlib import Path
import json
from collections import OrderedDict

if __name__ == "__main__":
    source_path = Path('anscombe.json')
    data = json.loads(source_path.read_text(),
        object_pairs_hook=OrderedDict)

    import statistics

    for function in (
        statistics.mean, statistics.median, min, max,
        statistics.variance, statistics.stdev):
        set_summary(data, function)

    print(json.dumps(data, indent=2))
