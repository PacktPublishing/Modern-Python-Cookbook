"""Python Cookbook

Chapter 3, Recipe 7
"""

import timeit
import doctest

def prod(int_iter):
    p= 1
    for i in int_iter:
        p *= i
    return p

def fact_s(n):
    """
    >>> fact_s(5)
    120
    """
    return prod(range(1, n+1))

def fact_o(n):
    """
    >>> fact_o(5)
    120
    """
    p= 1
    for i in range(2, n+1):
        p *= i
    return p

def fact_w(n):
    """
    >>> fact_w(5)
    120
    """
    p = n
    while n != 1:
        n = n-1
        p *= n
    return p

from functools import lru_cache

@lru_cache(128)
def fibo_r(n):
    """
    >>> fibo_r(0)
    1
    >>> fibo_r(1)
    1
    >>> fibo_r(2)
    2
    >>> fibo_r(3)
    3
    >>> fibo_r(4)
    5
    >>> fibo_r(7)
    21
    """
    if n < 2:
        return 1
    else:
        return fibo_r(n-1) + fibo_r(n-2)

def fibo_iter():
    a = 1
    b = 1
    yield a
    while True:
        yield b
        a, b = b, a+b

def fibo_i(n):
    """
    >>> fibo_i(0)
    1
    >>> fibo_i(1)
    1
    >>> fibo_i(2)
    2
    >>> fibo_i(3)
    3
    >>> fibo_i(4)
    5
    >>> fibo_i(7)
    21
    """
    for i, f_i in enumerate(fibo_iter()):
        if i == n: break
    return f_i

def factorial():
    simple = timeit.timeit('fact_s(52)',
'''
from ch03_r07 import fact_s
''')

    optimized = timeit.timeit('fact_o(52)',
'''
from ch03_r07 import fact_o
''')

    while_statement = timeit.timeit('fact_w(52)',
'''
from ch03_r07 import fact_w
'''
    )

    print( "Simple    {simple:.4f}".format_map(vars()))
    print( "Optimized {optimized:.4f}".format_map(vars()))
    print( "While     {while_statement:.4f}".format_map(vars()))

def fibonacci():
    cached = timeit.timeit('fibo_r(20)',
'''
from ch03_r07 import fibo_r
''')

    iterative = timeit.timeit('fibo_i(20)',
'''
from ch03_r07 import fibo_i
'''
    )

    print( "Cached     {cached:.4f}".format_map(vars()))
    print( "Interative {iterative:.4f}".format_map(vars()))

if __name__ == "__main__":
    # Be sure they all work before getting performance numbers
    fail_count, test_count  = doctest.testmod()
    assert fail_count == 0, "Not all tests passed"

    factorial()
    fibonacci()
