"""Python Cookbook

Chapter 8, recipe 7.
"""
from itertools import takewhile

def find_first(predicate, iterable):
    for item in iterable:
        if predicate(item):
            yield item
            break

import math
def prime(n):
    """
    >>> p = [2, 3, 5, 7, 11, 13, 17, 19]
    >>> tests = (prime(n) == (n in p)
    ... for n in range(2, 21))
    >>> all(tests)
    True
    """
    factors = find_first(
        lambda i: n % i == 0,
        range(2, int(math.sqrt(n)+1)) )
    return len(list(factors)) == 0

def prime_t(n):
    """
    >>> p = [2, 3, 5, 7, 11, 13, 17, 19]
    >>> tests = (prime_t(n) == (n in p)
    ... for n in range(2, 21))
    >>> all(tests)
    True
    """
    tests = set(range(2, int(math.sqrt(n)+1)))
    non_factors = set(takewhile(
        lambda i: n % i != 0,
        tests
    ))
    return tests == non_factors

if __name__ == "__main__":
    import doctest
    doctest.testmod()
