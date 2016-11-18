"""Python Cookbook

Chapter 5, recipe 4
"""
from ch03_r05 import haversine, MI, NM, KM

import argparse
import sys

def point_type(string):
    """
    >>> point_type('36.12, -86.67')
    (36.12, -86.67)
    >>> point_type('36.12, 76.abc') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/doctest.py", line 1318, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.point_type[1]>", line 1, in <module>
        point_type('36.12, 76.abc') #doctest: +IGNORE_EXCEPTION_DETAIL
      File "/Users/slott/Documents/Writing/Python Cookbook/code/ch05_r04.py", line 23, in point_type
        raise argparse.ArgumentTypeError from ex
    argparse.ArgumentTypeError
    """
    try:
        lat_str, lon_str = string.split(',')
        lat = float(lat_str)
        lon = float(lon_str)
        return lat, lon
    except Exception as ex:
        raise argparse.ArgumentTypeError from ex

def get_options(argv):
    """
    >>> opts= get_options(['-r', 'KM', '36.12,-86.67', '33.94,-118.4'])
    >>> opts.r
    'KM'
    >>> opts.p1
    (36.12, -86.67)
    >>> opts.p2
    (33.94, -118.4)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store',
            choices=('NM', 'MI', 'KM'), default='NM')
    parser.add_argument('p1', action='store', type=point_type)
    parser.add_argument('p2', action='store', type=point_type)
    options = parser.parse_args(argv)
    return options

from ch03_r05 import haversine, MI, NM, KM
def display(lat1, lon1, lat2, lon2, r):
    """
    >>> display(36.12, -86.67, 33.94, -118.4, 'NM')
    From 36.12,-86.67 to 33.94,-118.4 in NM = 1558.53
    """
    r_float = {'NM': NM, 'KM': KM, 'MI': MI}[r]
    d = haversine( lat1, lon1, lat2, lon2, r_float )
    print( "From {lat1},{lon1} to {lat2},{lon2}"
          " in {r} = {d:.2f}".format_map(vars()))

def main():
    options = get_options(sys.argv[1:])
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, options.r)

def test():
    import doctest
    doctest.testmod(verbose=1);

if __name__ == "__main__":
    test()
    #main()
