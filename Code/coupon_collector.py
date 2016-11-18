"""Python Cookbook

See

http://www.brynmawr.edu/math/people/anmyers/PAPERS/SIGEST_Coupons.pdf

and

https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind

and

https://en.wikipedia.org/wiki/Binomial_coefficient
"""

from math import factorial

def expected(n, population=8):
    """
    What is the probability p(n, d) that exactly n boxes of cereal will
    have to be purchased in order to obtain, for the first time,
    a complete collection of at least one of each of the d kinds of souvenir
    coupons?

    ..  math::

        p(n, d) = \frac{d!}{d^n} \lbrace\textstyle{ n-1 \atop d-1 }\rbrace
    """
    return factorial(population)/population**n * stirling2(n-1, population-1)

def binom(n, k):
    """

    ..  math::

        \binom n k = \frac{n!}{k!\,(n-k)!} \quad \text{for }\ 0\leq k\leq n
    """
    return factorial(n)/(factorial(k)*factorial(n-k))

def stirling2(n, k):
    """

    The Stirling numbers of the second kind,
    written S(n,k) or :math:`\lbrace\textstyle{n\atop k}\rbrace`
    count the number of ways to partition a set of n labelled objects
    into k nonempty unlabelled subsets.

    ..  math::

        \lbrace\textstyle{n\atop n}\rbrace = 1  \\

        \lbrace\textstyle{n\atop 1}\rbrace = 1  \\

        \lbrace\textstyle{n\atop k}\rbrace = k \lbrace\textstyle{n-1 \atop k}\rbrace + \lbrace\textstyle{n-1 \atop k-1}\rbrace

    Or

    ..  math::

        \left\{ {n \atop k}\right\} = \frac{1}{k!}\sum_{j=0}^{k} (-1)^{k-j} \binom{k}{j} j^n
    """

    return 1/factorial(k)*sum( (-1 if (k-j)%2 else 1)*binom(k,j)*j**n for j in range(0,k+1) )

if __name__ == "__main__":

    for i in range(8,30):
        print(i, expected(i, 8))


    print(binom(24,12))
