"""Python Cookbook

Chapter 8, recipe 8.
"""
from pprint import pprint


text_1 = '''\
10	8.04
8	6.95
13	7.58
9	8.81
11	8.33
14	9.96
6	7.24
4	4.26
12	10.84
7	4.82
5	5.68
'''

text_2 = '''\
10	9.14
8	8.14
13	8.74
9	8.77
11	9.26
14	8.1
6	6.13
4	3.1
12	9.13
7	7.26
5	4.74
'''

text_parse = lambda text: (r.split() for r in text.splitlines())

from types import SimpleNamespace
row_build = lambda rows: (SimpleNamespace(x=float(x), y=float(y)) for x,y in rows)

data_1 = list(row_build(text_parse(text_1)))
data_2 = list(row_build(text_parse(text_2)))

def standardize(mean, stdev, x):
    return (x-mean)/stdev

import statistics
mean_x = statistics.mean(item.x for item in data_1)
stdev_x = statistics.stdev(item.x for item in data_1)

from functools import partial
z_1 = partial(standardize, mean_x, stdev_x)

z_2 = lambda x: standardize(mean_x, stdev_x, x)

z_3 = lambda x, m=mean_x, s=stdev_x: standardize(m, s, x)

def prepare_z(data):
    mean_x = statistics.mean(item.x for item in data_1)
    stdev_x = statistics.stdev(item.x for item in data_1)
    return partial(standardize, mean_x, stdev_x)

z_4 = prepare_z(data_1)


__test__ = {
    'parse': '''
>>> pprint(list(text_parse(text_1)))
[['10', '8.04'],
 ['8', '6.95'],
 ['13', '7.58'],
 ['9', '8.81'],
 ['11', '8.33'],
 ['14', '9.96'],
 ['6', '7.24'],
 ['4', '4.26'],
 ['12', '10.84'],
 ['7', '4.82'],
 ['5', '5.68']]
''',

    'parse and cleanse': '''
>>> pprint(list(row_build(text_parse(text_1))))
[namespace(x=10.0, y=8.04),
 namespace(x=8.0, y=6.95),
 namespace(x=13.0, y=7.58),
 namespace(x=9.0, y=8.81),
 namespace(x=11.0, y=8.33),
 namespace(x=14.0, y=9.96),
 namespace(x=6.0, y=7.24),
 namespace(x=4.0, y=4.26),
 namespace(x=12.0, y=10.84),
 namespace(x=7.0, y=4.82),
 namespace(x=5.0, y=5.68)]
''',

    'standardize': '''
>>> for row in data_1:
...     z_x = standardize(mean_x, stdev_x, row.x)
...     print(row, round(z_x,2))
namespace(x=10.0, y=8.04) 0.3
namespace(x=8.0, y=6.95) -0.3
namespace(x=13.0, y=7.58) 1.21
namespace(x=9.0, y=8.81) 0.0
namespace(x=11.0, y=8.33) 0.6
namespace(x=14.0, y=9.96) 1.51
namespace(x=6.0, y=7.24) -0.9
namespace(x=4.0, y=4.26) -1.51
namespace(x=12.0, y=10.84) 0.9
namespace(x=7.0, y=4.82) -0.6
namespace(x=5.0, y=5.68) -1.21
''',

    'z_1': '''
>>> for row in data_1:
...     print(row, round(z_1(row.x), 2))
namespace(x=10.0, y=8.04) 0.3
namespace(x=8.0, y=6.95) -0.3
namespace(x=13.0, y=7.58) 1.21
namespace(x=9.0, y=8.81) 0.0
namespace(x=11.0, y=8.33) 0.6
namespace(x=14.0, y=9.96) 1.51
namespace(x=6.0, y=7.24) -0.9
namespace(x=4.0, y=4.26) -1.51
namespace(x=12.0, y=10.84) 0.9
namespace(x=7.0, y=4.82) -0.6
namespace(x=5.0, y=5.68) -1.21
''',

    'z_2': '''
>>> for row in data_1:
...     print(row, round(z_2(row.x), 2))
namespace(x=10.0, y=8.04) 0.3
namespace(x=8.0, y=6.95) -0.3
namespace(x=13.0, y=7.58) 1.21
namespace(x=9.0, y=8.81) 0.0
namespace(x=11.0, y=8.33) 0.6
namespace(x=14.0, y=9.96) 1.51
namespace(x=6.0, y=7.24) -0.9
namespace(x=4.0, y=4.26) -1.51
namespace(x=12.0, y=10.84) 0.9
namespace(x=7.0, y=4.82) -0.6
namespace(x=5.0, y=5.68) -1.21
''',

    'z_3': '''
>>> for row in data_1:
...     print(row, round(z_3(row.x), 2))
namespace(x=10.0, y=8.04) 0.3
namespace(x=8.0, y=6.95) -0.3
namespace(x=13.0, y=7.58) 1.21
namespace(x=9.0, y=8.81) 0.0
namespace(x=11.0, y=8.33) 0.6
namespace(x=14.0, y=9.96) 1.51
namespace(x=6.0, y=7.24) -0.9
namespace(x=4.0, y=4.26) -1.51
namespace(x=12.0, y=10.84) 0.9
namespace(x=7.0, y=4.82) -0.6
namespace(x=5.0, y=5.68) -1.21
''',

    'z_4': '''
>>> for row in data_1:
...     print(row, round(z_4(row.x), 2))
namespace(x=10.0, y=8.04) 0.3
namespace(x=8.0, y=6.95) -0.3
namespace(x=13.0, y=7.58) 1.21
namespace(x=9.0, y=8.81) 0.0
namespace(x=11.0, y=8.33) 0.6
namespace(x=14.0, y=9.96) 1.51
namespace(x=6.0, y=7.24) -0.9
namespace(x=4.0, y=4.26) -1.51
namespace(x=12.0, y=10.84) 0.9
namespace(x=7.0, y=4.82) -0.6
namespace(x=5.0, y=5.68) -1.21
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
