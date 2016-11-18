"""Python Cookbook

Chapter 10, recipe 3.
"""

from math import sqrt


def correlation(data):

    sumxy = sum(i['x']*i['y'] for i in data)
    sumx = sum(i['x'] for i in data)
    sumy = sum(i['y'] for i in data)
    sumx2 = sum(i['x']**2 for i in data)
    sumy2 = sum(i['y']**2 for i in data)
    n = sum(1 for i in data)

    r = (n*sumxy - sumx*sumy) / (sqrt(n*sumx2-sumx**2)*sqrt(n*sumy2-sumy**2))
    return r

def corr2(data):
    sumx = sumy = sumxy = sumx2 = sumy2 = n = 0
    for item in data:
        x, y = item['x'], item['y']
        n += 1
        sumx += x
        sumy += y
        sumxy += x * y
        sumx2 += x**2
        sumy2 += y**2

    r = (n*sumxy - sumx*sumy) / (sqrt(n*sumx2-sumx**2)*sqrt(n*sumy2-sumy**2))
    return r

from pathlib import Path
import json
from collections import OrderedDict


if __name__ == "__main__":
    source_path = Path('anscombe.json')
    data = json.loads(source_path.read_text(),
        object_pairs_hook=OrderedDict)

    __test__ = {
        'correlation': '''
    >>> for series in data:
    ...    r = correlation(series['data'])
    ...    print(series['series'], 'r=', round(r, 2))
    I r= 0.82
    II r= 0.82
    III r= 0.82
    IV r= 0.82

    ''',

        'corr2': '''
    >>> for series in data:
    ...    r = corr2(series['data'])
    ...    print(series['series'], 'r=', round(r, 2))
    I r= 0.82
    II r= 0.82
    III r= 0.82
    IV r= 0.82

    '''
    }

    import doctest
    doctest.testmod()
