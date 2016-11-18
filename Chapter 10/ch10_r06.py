"""Python Cookbook

Chapter 10, recipe 6.
"""

from ch10_r05 import get_data
from pathlib import Path

if __name__ == "__main__":
    source_path = Path('co2_mm_mlo.txt')
    with source_path.open() as source_file:
        all_data = list(get_data(source_file))
    y1959 = [r.interpolated for r in all_data if r.year == 1959]
    y1960 = [r.interpolated for r in all_data if r.year == 1960]
    y2014 = [r.interpolated for r in all_data if r.year == 2014]

from statistics import mean
from collections import Counter
import time

import itertools
def all_combos(s1, s2):
    """Builds sets and then picks elements from sequences for
    all possible combinations of subset values.

    A less naive version of this works on simple sums.
    ::

        universe = sum(pool)
        for combination in itertools.permutations(pool, len(s1))
            m_a = sum(combination)/len(s1)
            m_b = (universe-a)/len(s2)
            delta = m_a - m_b
    """
    start = time.perf_counter()

    T_obs = mean(s1)-mean(s2)
    print( "T_obs = m_1-m_2 = {:.2f}-{:.2f} = {:.2f}".format(
        mean(s1), mean(s2), T_obs)
    )

    below = above = 0
    pool = s1+s2
    universe = set(range(len(pool)))
    for a_inxs in itertools.combinations(universe, len(s1)):
        b_inxs = universe - set(a_inxs)
        #a = list(pool[i] for i in a_inxs)
        #b = list(pool[i] for i in b_inxs)
        m_a = mean(pool[i] for i in a_inxs)
        m_b = mean(pool[i] for i in b_inxs)
        #print( a_inxs, a, m_a )
        #print( b_inxs, b, m_b )
        if m_a-m_b < T_obs:
            below += 1
        else:
            above += 1
    print( "below {:,} {:.1%}, above {:,} {:.1%}".format(
        below, below/(below+above),
        above, above/(below+above)))

    end = time.perf_counter()
    print('time', end-start)

import random
from statistics import mean
from collections import Counter
def randomized(s1, s2, limit=270415):
    start = time.perf_counter()

    T_obs = mean(s2)-mean(s1)
    print( "T_obs = m_2-m_1 = {:.2f}-{:.2f} = {:.2f}".format(
        mean(s2), mean(s1), T_obs)
    )

    counts = Counter()
    universe = s1+s2
    for resample in range(limit):
        random.shuffle(universe)
        a = universe[:len(s2)]
        b = universe[len(s2):]
        delta = int(1000*(mean(a) - mean(b)))
        counts[delta] += 1

    T = int(1000*T_obs)
    below = sum(v for k,v in counts.items() if k < T )
    above = sum(v for k,v in counts.items() if k >= T )

    print( "below {:,} {:.1%}, above {:,} {:.1%}".format(
        below, below/(below+above),
        above, above/(below+above)))

    end = time.perf_counter()
    print('time', end-start)

def test():
    s1 = (1, 2, 3, 4)  # mean = 2.5, stdev = 1.29
    s2 = (2, 2, 3, 4)  # mean = 2.75
    all_combos(s1, s2)

    s3 = (3, 4, 5, 6)  # mean = 4.5
    all_combos(s1, s3)

def demo():
    m_1959 = mean(y1959)
    m_1960 = mean(y1960)
    m_2014 = mean(y2014)
    print("1959 mean {:.2f}".format(m_1959))
    print("1960 mean {:.2f}".format(m_1960))
    print("2014 mean {:.2f}".format(m_2014))

    print("1959 v. 1960")
    all_combos(y1959, y1960)

    print("\n\n1959 v. 2014")
    all_combos(y1959, y2014)

    print("1959 v. 1960")
    randomized(y1959, y1960)

    print("\n\n1959 v. 2014")
    randomized(y1959, y2014)

if __name__ == "__main__":
    test()
