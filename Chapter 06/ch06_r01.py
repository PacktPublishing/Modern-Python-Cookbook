"""Python Cookbook

Chapter 6, recipe 1
"""
import random

class Dice:

    def __init__(self):
        self.faces = None

    def roll(self):
        self.faces = (random.randint(1,6), random.randint(1,6))

    def total(self):
        return sum(self.faces)

    def hardway(self):
        return self.faces[0] == self.faces[1]

    def easyway(self):
        return self.faces[0] != self.faces[1]

__test__ = {
    'example1': '''
>>> import random
>>> random.seed(1)
>>> d1 = Dice()
>>> d1.roll()
>>> d1.total()
7
>>> d1.faces
(2, 5)

>>> d1.total()
7
''',

    'example2': '''
>>> d2 = Dice()
>>> d2.roll()
>>> d2.total()
4
>>> d2.hardway()
False
>>> d2.faces
(1, 3)
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=2)
