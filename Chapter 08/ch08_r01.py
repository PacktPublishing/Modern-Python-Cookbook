"""Python Cookbook

Chapter 8, recipe 1.
"""
from pprint import pprint

import datetime
def parse_date_iter(source):
    for item in source:

        date = datetime.datetime.strptime(
            item[0],
            "%Y-%m-%d %H:%M:%S,%f")
        new_item = (date,)+item[1:]

        yield new_item

def parse_date(item):
    date = datetime.datetime.strptime(
        item[0],
        "%Y-%m-%d %H:%M:%S,%f")
    new_item = (date,)+item[1:]
    return new_item

data = [
    ('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'),
    ('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging'),
    ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')
]

__test__ = {
    'parse_date_iter': '''
>>> for item in parse_date_iter(data):
...     pprint(item)
(datetime.datetime(2016, 4, 24, 11, 5, 1, 462000),
 'INFO',
 'module1',
 'Sample Message One')
(datetime.datetime(2016, 4, 24, 11, 6, 2, 624000),
 'DEBUG',
 'module2',
 'Debugging')
(datetime.datetime(2016, 4, 24, 11, 7, 3, 246000),
 'WARNING',
 'module1',
 'Something might have gone wrong')

>>> details = list(parse_date_iter(data))
>>> len(details)
3

>>> parse_date_iter(data) # doctest: +ELLIPSIS
<generator object parse_date_iter at 0x...>

>>> iter(parse_date_iter(data)) # doctest: +ELLIPSIS
<generator object parse_date_iter at 0x...>

''',

    'parse_date': '''
>>> for item in map(parse_date, data):
...     pprint(item)
(datetime.datetime(2016, 4, 24, 11, 5, 1, 462000),
 'INFO',
 'module1',
 'Sample Message One')
(datetime.datetime(2016, 4, 24, 11, 6, 2, 624000),
 'DEBUG',
 'module2',
 'Debugging')
(datetime.datetime(2016, 4, 24, 11, 7, 3, 246000),
 'WARNING',
 'module1',
 'Something might have gone wrong')
'''
}

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)

