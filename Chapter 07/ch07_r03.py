"""Python Cookbook

Chapter 7, recipe 3
"""
import random

class Dice1:
    def __init__(self, seed=None):
        self._rng = random.Random(seed)
        self.roll()
    def roll(self):
        self.dice = (self._rng.randint(1,6),
            self._rng.randint(1,6))
        return self.dice

class Die:
    def __init__(self, rng):
        self._rng= rng
    def roll(self):
        return self._rng.randint(1, 6)

class Dice2:
    def __init__(self, seed=None):
        self._rng = random.Random(seed)
        self._dice = [Die(self._rng) for _ in range(2)]
        self.roll()
    def roll(self):
        self.dice = tuple(d.roll() for d in self._dice)
        return self.dice

def roller(dice_class, seed=None, *, samples=10):
    dice = dice_class(seed)
    for _ in range(samples):
        yield dice.roll()

__test__ = {
    'roller': '''
>>> from ch07_r03 import roller, Dice1, Dice2
>>> list(roller(Dice1, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]
>>> list(roller(Dice2, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]
'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
