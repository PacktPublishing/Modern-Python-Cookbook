"""Python Cookbook

Chapter 4, recipe 8
"""
from ch04_r06 import *

from collections import defaultdict, Counter

def example_1(source):
    histogram = {}
    for item in source:
        if item not in histogram:
            histogram[item]= 0
        histogram[item] += 1
    return histogram

def example_2(source):
    histogram = {}
    for item in source:
        histogram.setdefault(item, 0)
        histogram[item] += 1
    return histogram

def example_3(source):
    histogram = defaultdict(int)
    for item in source:
        histogram[item] += 1
    return histogram

def example_4(source):
    histogram = Counter(source)
    return histogram

def show(histogram):
    """
    >>> random.seed(1)
    >>> data = Counter( int(5+5*random.gauss(0, .3)) for _ in range(100) )
    >>> show( data )
      0 | *
      1 | *
      2 | **********
      3 | *****************************
      4 | *****************************************
      5 | **************************************************
      6 | ***************************
      7 | ********
      8 | *
    """
    limit = max(histogram.values())
    for k in sorted(histogram):
        bar = int(50*histogram[k]/limit)*'*'
        print( "{:3d} | {:s}".format(k, bar) )

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print( "\narrival1" )
    show( example_1(samples(1000, arrival1(8))) )
    print( "\narrival1" )
    show( example_2(samples(1000, arrival1(8))) )
    print( "\narrival1" )
    show( example_3(samples(1000, arrival1(8))) )
    print( "\narrival1" )
    show( example_4(samples(1000, arrival1(8))) )

    print( "\narrival2")
    show( example_1(samples(1000, arrival2(8))) )

    from pprint import pprint
    random.seed(1)
    pprint(example_4(samples(1000, arrival1(8))) )
