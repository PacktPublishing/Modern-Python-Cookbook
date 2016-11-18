"""Python Cookbook

Chapter 5, recipe 6
"""
import os
import sys
import argparse

from ch03_r05 import haversine, MI, NM, KM
from ch05_r04 import point_type, display

def get_options(argv=sys.argv):
    """
    >>> os.environ['UNITS'] = 'NM'
    >>> get_options(['ch05_r06.py', '36.12,-86.67']) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.get_options[1]>", line 1, in <module>
        get_options(['ch05_r06.py', '36.12,-86.67']) # doctest: +IGNORE_EXCEPTION_DETAIL
      File "/Users/slott/Documents/Writing/Python Cookbook/code/ch05_r06.py", line 49, in get_options
        sys.exit("Neither HOME_PORT nor p2 argument provided.")
    SystemExit: Neither HOME_PORT nor p2 argument provided.

    >>> os.environ['UNITS'] = 'NM'
    >>> os.environ['HOME_PORT'] = '36.842952,-76.300171'
    >>> get_options(['ch05_r06.py', '36.12,-86.67'])
    Namespace(p1=(36.12, -86.67), p2=(36.842952, -76.300171), r='NM')

    >>> os.environ['UNITS'] = 'XX'
    >>> os.environ['HOME_PORT'] = '36.842952,-76.300171'
    >>> get_options(['ch05_r06.py', '36.12,-86.67']) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.get_options[5]>", line 1, in <module>
        get_options(['ch05_r06.py', '36.12,-86.67'])
      File "/Users/slott/Documents/Writing/Python Cookbook/code/ch05_r06.py", line 27, in get_options
        sys.exit("Invalid value for UNITS, not KM, NM, or MI")
    SystemExit: Invalid value for UNITS, not KM, NM, or MI
    """
    default_units = os.environ.get('UNITS', 'KM')
    if default_units not in ('KM', 'NM', 'MI'):
        sys.exit("Invalid value for UNITS, not KM, NM, or MI")
    default_home_port = os.environ.get('HOME_PORT')
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', action='store',
        choices=('NM', 'MI', 'KM'), default=default_units)
    parser.add_argument('p1', action='store', type=point_type)
    parser.add_argument('p2', nargs='?', action='store', type=point_type,
        default=default_home_port)
    options = parser.parse_args(argv[1:])

    if options.p2 is None:
        sys.exit("Neither HOME_PORT nor p2 argument provided.")

    return options

def main():
    options = get_options()
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, options.r)

def test():
    import doctest
    doctest.testmod(verbose=1);

if __name__ == "__main__":
    test()
    #main()
