"""Python Cookbook

Chapter 8, recipe 9.
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

from typing import *

def get(text: str) -> Iterator[List[str]]:
    for line in text.splitlines():
        if len(line) == 0:
            continue
        yield line.split()

from collections import namedtuple

DataPair = namedtuple('DataPair', ['x', 'y'])

# Alternative

DataPair = NamedTuple('DataPair', [
        ('x', float),
        ('y', float)
    ]
)

def cleanse(iterable: Iterable[List[str]]) -> Iterator[DataPair]:
    for text_items in iterable:
        try:
            x_amount = float(text_items[0])
            y_amount = float(text_items[1])
            yield DataPair(x_amount, y_amount)
        except Exception as ex:
            print(ex, repr(text_items))

RankYDataPair = namedtuple('RankYDataPair', ['y_rank', 'pair'])

PairIter = Iterable[DataPair]
RankPairIter = Iterator[RankYDataPair]

def rank_by_y(iterable:PairIter) -> RankPairIter:
    all_data = sorted(iterable, key=lambda pair:pair.y)
    for y_rank, pair in enumerate(all_data, start=1):
        yield RankYDataPair(y_rank, pair)

from types import SimpleNamespace
def cleanse_ns(iterable):
    for text_items in iterable:
        try:
            x_amount = float(text_items[0])
            y_amount = float(text_items[1])
            yield SimpleNamespace(x=x_amount, y=y_amount)
        except Exception as ex:
            print(ex, repr(text_items))

def rank_by_y_ns(iterable):
    all_data = sorted(iterable, key=lambda pair:pair.y)
    for y_rank, pair in enumerate(all_data, start=1):
        pair.y_rank = y_rank
        yield pair

def timing():
    import timeit
    tuple_runtime = timeit.timeit(
        '''list(rank_by_y(cleanse(get(text_1))))''',
        '''from ch08_r09 import get, cleanse, rank_by_y, text_1''',
    )
    namespace_runtime = timeit.timeit(
        '''list(rank_by_y_ns(cleanse_ns(get(text_1))))''',
        '''from ch08_r09 import get, cleanse_ns, rank_by_y_ns, text_1''',
    )
    print("{0} {1}".format("tuple", tuple_runtime))
    print("{0} {1}".format("namespace", namespace_runtime))

__test__ = {
    'get': '''
>>> pprint(list(get(text_1)))
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

    'get-cleanse': '''
>>> pprint(list(cleanse(get(text_1))))
[DataPair(x=10.0, y=8.04),
 DataPair(x=8.0, y=6.95),
 DataPair(x=13.0, y=7.58),
 DataPair(x=9.0, y=8.81),
 DataPair(x=11.0, y=8.33),
 DataPair(x=14.0, y=9.96),
 DataPair(x=6.0, y=7.24),
 DataPair(x=4.0, y=4.26),
 DataPair(x=12.0, y=10.84),
 DataPair(x=7.0, y=4.82),
 DataPair(x=5.0, y=5.68)]
''',

    'get-cleanse-rank': '''
>>> data = rank_by_y(cleanse(get(text_1)))
>>> pprint(list(data))
[RankYDataPair(y_rank=1, pair=DataPair(x=4.0, y=4.26)),
 RankYDataPair(y_rank=2, pair=DataPair(x=7.0, y=4.82)),
 RankYDataPair(y_rank=3, pair=DataPair(x=5.0, y=5.68)),
 RankYDataPair(y_rank=4, pair=DataPair(x=8.0, y=6.95)),
 RankYDataPair(y_rank=5, pair=DataPair(x=6.0, y=7.24)),
 RankYDataPair(y_rank=6, pair=DataPair(x=13.0, y=7.58)),
 RankYDataPair(y_rank=7, pair=DataPair(x=10.0, y=8.04)),
 RankYDataPair(y_rank=8, pair=DataPair(x=11.0, y=8.33)),
 RankYDataPair(y_rank=9, pair=DataPair(x=9.0, y=8.81)),
 RankYDataPair(y_rank=10, pair=DataPair(x=14.0, y=9.96)),
 RankYDataPair(y_rank=11, pair=DataPair(x=12.0, y=10.84))]
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    timing()
