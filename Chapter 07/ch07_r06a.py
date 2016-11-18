"""Python Cookbook

Chapter 7, recipe 6a.
"""

from ch07_r02 import AceCard, Card, FaceCard, SUITS

Spades, Hearts, Diamonds, Clubs = SUITS

class SortedCard:
    def __lt__(self, other):
        return (self.rank, self.suit) < (other.rank, other.suit)
    def __le__(self, other):
        return (self.rank, self.suit) <= (other.rank, other.suit)
    def __gt__(self, other):
        return (self.rank, self.suit) > (other.rank, other.suit)
    def __ge__(self, other):
        return (self.rank, self.suit) >= (other.rank, other.suit)
    def __eq__(self, other):
        return (self.rank, self.suit) == (other.rank, other.suit)
    def __ne__(self, other):
        return (self.rank, self.suit) != (other.rank, other.suit)


class PinochlePoints:
    _points = {9: 0, 10:10, 11:2, 12:3, 13:4, 14:11}
    def points(self):
        return self._points[self.rank]


class PinochleAce(AceCard, SortedCard, PinochlePoints):
    pass


class PinochleFace(FaceCard, SortedCard, PinochlePoints):
    pass


class PinochleNumber(Card, SortedCard, PinochlePoints):
    pass


def make_card(rank, suit):
    if rank in (9, 10):
        return PinochleNumber(rank, suit)
    elif rank in (11, 12, 13):
        return PinochleFace(rank, suit)
    else:
        return PinochleAce(rank, suit)


def make_deck():
    return [make_card(r, s) for _ in range(2)
        for r in range(9, 15)
        for s in SUITS]


__test__ = {
    'card': '''
>>> c1 = make_card(9, '♡')
>>> c2 = make_card(10, '♡')
>>> c1 < c2
True
>>> c1 == c1
True
>>> c1 == c2
False
>>> c1 > c2
False
''',

    'deck': '''
>>> deck = make_deck()
>>> len(deck)
48
>>> deck[:8]
[ 9 ♠,  9 ♡,  9 ♢,  9 ♣, 10 ♠, 10 ♡, 10 ♢, 10 ♣]
>>> deck[24:32]
[ 9 ♠,  9 ♡,  9 ♢,  9 ♣, 10 ♠, 10 ♡, 10 ♢, 10 ♣]


>>> import random
>>> random.seed(4)
>>> random.shuffle(deck)
>>> sorted(deck[:12])
[ 9 ♣, 10 ♣,  J ♠,  J ♢,  J ♢,  Q ♠,  Q ♣,  K ♠,  K ♠,  K ♣,  A ♡,  A ♣]
''',

    'card-int': '''
>>> c1 = make_card(9, '♡')
>>> c1 == 9
'''
}


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
