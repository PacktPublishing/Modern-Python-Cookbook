"""Python Cookbook

Chapter 11, recipe 1 and 2.
"""

from math import factorial
def binom(n: int, k: int) -> int:
    '''Computes the binomial coefficient.
    This shows how many combinations of
    *n* things taken in groups of size *k*.

    :param n: size of the universe
    :param k: size of each subset

    :returns: the number of combinations

    >>> binom(52, 5)
    2598960
    >>> binom(52, 0)
    1
    >>> binom(52, 52)
    1
    '''
    return factorial(n) // (factorial(k) * factorial(n-k))

__test__ = {

'GIVEN_binom_WHEN_wrong_relationship_THEN_error': '''
    >>> binom(5, 52)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.GIVEN_binom_WHEN_wrong_relationship_THEN_error[0]>", line 1, in <module>
        binom(5, 52)
      File "/Users/slott/Documents/Writing/Python Cookbook/code/ch11_r01.py", line 24, in binom
        return factorial(n) // (factorial(k) * factorial(n-k))
    ValueError: factorial() not defined for negative values
''',

'GIVEN_binom_WHEN_negative_THEN_exception': '''
    >>> binom(52, -5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: factorial() not defined for negative values
''',

'GIVEN_binom_WHEN_string_THEN_exception': '''
    >>> binom('a', 'b') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.binom negative[0]>", line 1, in <module>
        binom(52, -5)
      File "/Users/slott/Documents/Writing/Python Cookbook/code/ch11_r01.py", line 24, in binom
        return factorial(n) // (factorial(k) * factorial(n-k))
    TypeError: an integer is required (got type str)
''',
}

from statistics import median
from collections import Counter

class Summary:
    '''Computes summary statistics.

    >>> s = Summary()
    >>> s.add(8)
    >>> s.add(9)
    >>> s.add(9)
    >>> round(s.mean, 2)
    8.67
    >>> s.median
    9
    >>> print(str(s))
    mean = 8.67
    median = 9
    '''

    def __init__(self):
        self.counts = Counter()

    def __str__(self):
        return "mean = {:.2f}\nmedian = {:d}".format(self.mean, self.median)

    def add(self, value):
        '''Adds a value to be summarized.

        :param value: Adds a new value to the collection.
        '''
        self.counts[value] += 1

    @property
    def count(self):
        s0 = sum(f for v,f in self.counts.items())

    @property
    def mean(self):
        '''Returns the mean of the collection.
        '''
        s0 = sum(f for v,f in self.counts.items())
        s1 = sum(v*f for v,f in self.counts.items())
        return s1/s0

    @property
    def median(self):
        '''Returns the median of the collection.
        '''
        return median(self.counts.elements())

    @property
    def mode(self):
        '''Returns the items in the collection in decreasing
        order by frequency.
        '''
        return self.counts.most_common()

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)
