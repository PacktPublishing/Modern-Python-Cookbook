"""Python Cookbook

Chapter 7, recipe 2
"""
import logging

SUITS = '\u2660\u2661\u2662\u2663'
Spades, Hearts, Diamonds, Clubs = SUITS

class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit):
        super().__init__()
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        return "{rank:2d} {suit}".format(
            rank=self.rank, suit=self.suit
        )

class AceCard(Card):
    def __repr__(self):
        return " A {suit}".format(
            rank=self.rank, suit=self.suit
        )

class FaceCard(Card):
    def __repr__(self):
        names = {11: 'J', 12: 'Q', 13: 'K'}
        return " {name} {suit}".format(
            rank=self.rank, suit=self.suit,
            name=names[self.rank]
        )

class CribbagePoints:
    def points(self):
        return self.rank

class CribbageFacePoints(CribbagePoints):
    def points(self):
        return 10

class CribbageAce(AceCard, CribbagePoints):
    pass

class CribbageCard(Card, CribbagePoints):
    pass

class CribbageFace(FaceCard, CribbageFacePoints):
    pass

def make_card(rank, suit):
    if rank == 1: return CribbageAce(rank, suit)
    if 2 <= rank < 11: return CribbageCard(rank, suit)
    if 11 <= rank: return CribbageFace(rank, suit)

class Logged:
    """Add a logger. Must be first in the superclass list."""
    def __init__(self, *args, **kw):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(*args, **kw)
    def points(self):
        p = super().points()
        self.logger.debug("points {0}".format(p))
        return p

class LoggedCribbageAce(Logged, AceCard, CribbagePoints):
    pass

class LoggedCribbageCard(Logged, Card, CribbagePoints):
    pass

class LoggedCribbageFace(Logged, FaceCard, CribbageFacePoints):
    pass

def make_logged_card(rank, suit):
    if rank == 1: return LoggedCribbageAce(rank, suit)
    if 2 <= rank < 11: return LoggedCribbageCard(rank, suit)
    if 11 <= rank: return LoggedCribbageFace(rank, suit)

__test__ = {
    'make_card': '''
>>> import random
>>> random.seed(1)
>>> deck = [make_card(rank+1, suit) for rank in range(13) for suit in SUITS]
>>> random.shuffle(deck)
>>> len(deck)
52
>>> deck[:5]
[ K ♡,  3 ♡, 10 ♡,  6 ♢,  A ♢]
>>> sum(c.points() for c in deck[:5])
30

>>> c = deck[5]
>>> c
10 ♢
>>> c.__class__.__name__
'CribbageCard'
>>> c.__class__.mro() # doctest: +NORMALIZE_WHITESPACE
[<class '__main__.CribbageCard'>, <class '__main__.Card'>,
<class '__main__.CribbagePoints'>, <class 'object'>]
''',

    'make_logged_card': '''
>>> import random
>>> random.seed(1)
>>> deck = [make_logged_card(rank+1, suit) for rank in range(13) for suit in SUITS]
>>> random.shuffle(deck)
>>> len(deck)
52
>>> deck[:5]
[ K ♡,  3 ♡, 10 ♡,  6 ♢,  A ♢]
>>> sum(c.points() for c in deck[:5])
30

>>> c = deck[5]
>>> c.logger.name
'LoggedCribbageCard'
>>> c.__class__.mro() # doctest: +NORMALIZE_WHITESPACE
[<class '__main__.LoggedCribbageCard'>, <class '__main__.Logged'>,
<class '__main__.Card'>, <class '__main__.CribbagePoints'>, <class 'object'>]
'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
