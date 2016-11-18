"""Python Cookbook

Chapter 6, recipe 6
"""
import math

class StatsList(list):
    """
    >>> subset1 = StatsList([10, 8, 13, 9, 11])
    >>> data = StatsList([14, 6, 4, 12, 7, 5])
    >>> data.extend(subset1)
    >>> data
    [14, 6, 4, 12, 7, 5, 10, 8, 13, 9, 11]
    >>> round(data.mean(), 1)
    9.0
    >>> round(data.variance(), 1)
    11.0
    """
    def sum(self):
        return sum(v for v in self)

    def count(self):
        return sum(1 for v in self)

    def sum2(self):
        return sum(v**2 for v in self)

    def mean(self):
        return self.sum() / self.count()

    def variance(self):
        return (self.sum2() - self.sum()**2/self.count())/(self.count()-1)

    def stddev(self):
        return math.sqrt(self.variance())

if __name__ == "__main__":
    import doctest
    doctest.testmod()
