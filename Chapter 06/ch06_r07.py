"""Python Cookbook

Chapter 6, recipe 7
"""
from ch04_r06 import *
from collections import Counter
import math
import statistics

def raw_data(n=8, limit=1000, arrival_function=arrival1):
    """
    >>> random.seed(1)
    >>> data = raw_data(n=2, limit=8, arrival_function=arrival1)
    >>> data
    Counter({2: 1, 3: 1})
    """
    data = samples(limit, arrival_function(n))
    wait_times = Counter(coupon_collector(n, data))
    return wait_times

class LazyCounterStatistics:
    """
    >>> data = Counter( [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5] )
    >>> cs = LazyCounterStatistics(data)
    >>> round(cs.mean,1)
    9.0
    >>> round(cs.stddev**2,1)
    11.0
    """

    def __init__(self, raw_counter:Counter):
        self.raw_counter = raw_counter

    @property
    def sum(self):
        return sum(f*v for v, f in self.raw_counter.items())

    @property
    def count(self):
        return sum(f for v, f in self.raw_counter.items())

    @property
    def sum2(self):
        return sum(f*v**2 for v, f in self.raw_counter.items())

    @property
    def mean(self):
        return self.sum / self.count

    @property
    def variance(self):
        return (self.sum2 - self.sum**2/self.count)/(self.count-1)

    @property
    def stddev(self):
        return math.sqrt(self.variance)

__test__ = {
    'expected': '''
>>> expected(8)
Fraction(761, 35)
''',

    'raw_data': '''
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> round(statistics.mean(data.elements()), 2)
20.81
>>> round(statistics.stdev(data.elements()), 2)
7.02
''',

    'LazyCounterStatistics': '''
>>> import random
>>> random.seed(1)
>>> data = raw_data(8)
>>> stats = LazyCounterStatistics(data)
>>> round(stats.mean, 2)
20.81
>>> round(stats.stddev, 2)
7.02
''',
}

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

    import random
    random.seed(1)
    data = raw_data(8)

    print("expected_time", float(expected(8)))
    print("expected mean", statistics.mean(data.elements()))
    print("expected stddev", statistics.stdev(data.elements()))

    stats = LazyCounterStatistics(data)
    print("Mean: {0:.2f}".format(stats.mean))
    print("Standard Deviation: {0:.3f}".format(stats.stddev))
