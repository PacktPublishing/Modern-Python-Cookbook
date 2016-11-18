"""Python Cookbook

Chapter 4, recipe 6
"""
import random
from fractions import Fraction
from statistics import mean

def arrival1(n=8):
    """
    >>> random.seed(1)
    >>> for n, r in enumerate(arrival1()):
    ...     if n == 8: break
    ...     print(r)
    2
    1
    4
    1
    7
    7
    7
    6
    """
    while True:
        yield random.randrange(n)

def arrival2(n=8):
    """
    >>> random.seed(1)
    >>> for n, r in enumerate(arrival2()):
    ...     if n == 8: break
    ...     print(r)
    1
    0
    1
    1
    2
    2
    2
    2
    """
    p = 0
    while True:
        step = random.choice([-1,0,+1])
        p += step
        yield abs(p) % n

def samples(limit, generator):
    """
    >>> random.seed(1)
    >>> for v in samples(8, arrival1()):
    ...     print(v)
    2
    1
    4
    1
    7
    7
    7
    6
    >>> random.seed(1)
    >>> for v in samples(8, arrival2()):
    ...     print(v)
    1
    0
    1
    1
    2
    2
    2
    2
    """
    for n, value in enumerate(generator):
        if n == limit: break
        yield value

def expected(n=8):
    """
    >>> expected(6)
    Fraction(147, 10)
    """
    return n * sum(Fraction(1,(i+1)) for i in range(n))

def coupon_collector(n, data):
    """
    >>> samples = [0, 1, 2, 3, 0, 0, 1, 1, 2, 2, 3, 3]
    >>> list(coupon_collector(4, samples))
    [4, 7]
    """
    count, collection = 0, set()
    for item in data:
        count += 1
        #collection = collection|{item}
        collection.add(item)
        if len(collection) == n:
            yield count
            count, collection = 0, set()

def summary(n, limit, arrival_function):
    expected_time = float(expected(n))

    data = samples(limit, arrival_function(n))
    wait_times = list(coupon_collector(n, data))
    average_time = mean(wait_times)
    print("Coupon collection, n={n}"
        .format_map(vars()))
    print("Arrivals per '{arrival_function.__name__}'"
        .format_map(vars()))
    print("Expected = {expected_time:.2f}"
        .format_map(vars()))
    print("Actual {average_time:.2f}"
        .format_map(vars()))

__test__ = {
    'arrival1': '''
>>> random.seed(1)
>>> summary( 8, 1000, arrival1 )
Coupon collection, n=8
Arrivals per 'arrival1'
Expected = 21.74
Actual 20.81
''',

    'arrival2': '''
>>> random.seed(1)
>>> summary( 8, 1000, arrival2 )
Coupon collection, n=8
Arrivals per 'arrival2'
Expected = 21.74
Actual 39.68
'''
}
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    random.seed(1)
    summary( 8, 1000, arrival1 )

    random.seed(1)
    summary( 8, 1000, arrival2 )
