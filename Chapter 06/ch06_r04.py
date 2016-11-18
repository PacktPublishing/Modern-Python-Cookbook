"""Python Cookbook

Chapter 6, recipe 3 and 4
"""
import random

from collections import namedtuple
Card = namedtuple('Card', ('rank', 'suit'))

class Hand:
    """
    >>> h = Hand(1)
    >>> h.deal( Card(1,'\N{white heart suit}'))
    >>> h.deal( Card(10, '\N{black club suit}'))
    >>> h
    Hand(1, [Card(rank=1, suit='♡'), Card(rank=10, suit='♣')])
    >>> h.total = 11 #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/doctest.py", line 1318, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.Hand[4]>", line 1, in <module>
        h.total = 11 #doctest: +IGNORE_EXCEPTION_DETAIL
    AttributeError: 'Hand' object has no attribute 'total'
    """

    __slots__ = ('hand', 'bet')

    def __init__(self, bet, hand=None):
        self.hand= hand or []
        self.bet= bet

    def deal(self, card):
        self.hand.append(card)

    def __repr__(self):
        return "{class_}({0}, {1})".format(
            self.bet, self.hand,
            class_= self.__class__.__name__,
        )

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

    SUITS = (
        '\N{black spade suit}',
        '\N{white heart suit}',
        '\N{white diamond suit}',
        '\N{black club suit}',
    )
    deck = [
        Card(r,s) for r in range(1,14) for s in SUITS
    ]
    random.seed(2)
    random.shuffle(deck)
    dealer = iter(deck)

    h = Hand(2)
    h.deal(next(dealer))
    h.deal(next(dealer))
    print(h)
