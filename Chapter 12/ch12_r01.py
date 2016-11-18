"""Python Cookbook

Chapter 12, recipe 1.
"""
import random
import json

class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit):
        self.rank = int(rank)
        self.suit = suit
    def __repr__(self):
        return "Card(rank={self.rank!r}, suit={self.suit!r})".format(self=self)
    def to_json(self):
        return {"__class__": "Card", 'rank': self.rank, 'suit': self.suit}

class Deck:
    SUITS = (
        '\N{black spade suit}',
        '\N{white heart suit}',
        '\N{white diamond suit}',
        '\N{black club suit}',
    )
    '''
    Create deck or shoe.

    >>> random.seed(2)
    >>> deck = Deck()
    >>> cards = deck.deal(5)
    >>> cards  # doctest: +NORMALIZE_WHITESPACE
    [Card(rank=4, suit='♣'), Card(rank=8, suit='♡'),
     Card(rank=3, suit='♡'), Card(rank=6, suit='♡'),
     Card(rank=2, suit='♠')]
    >>> json_cards = list(card.to_json() for card in deck.deal(5))
    >>> print(json.dumps(json_cards, indent=2, sort_keys=True))
    [
      {
        "__class__": "Card",
        "rank": 2,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 13,
        "suit": "\u2663"
      },
      {
        "__class__": "Card",
        "rank": 7,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 6,
        "suit": "\u2662"
      },
      {
        "__class__": "Card",
        "rank": 7,
        "suit": "\u2660"
      }
    ]
    '''
    def __init__(self, n=1):
        self.n = n
        self.create_deck(self.n)
    def create_deck(self, n=1):
        self.cards = [
            Card(r,s) for r in range(1,14) for s in self.SUITS for _ in range(n)
        ]
        random.shuffle(self.cards)
        self.offset = 0
    def deal(self, hand_size=5):
        if self.offset + hand_size > len(self.cards):
            self.create_deck(self.n)
        hand = self.cards[self.offset:self.offset+hand_size]
        self.offset += hand_size
        return hand

from http import HTTPStatus

import os
random.seed(os.environ.get('DEAL_APP_SEED'))
deck = Deck()
def deal_cards(environ, start_response):
    global deck
    hand_size = int(environ.get('HAND_SIZE', 5))
    cards = deck.deal(hand_size)
    status = "{status.value} {status.phrase}".format(status=HTTPStatus.OK)
    headers = [('Content-Type', 'application/json;charset=utf-8')]
    start_response(status, headers)
    json_cards = list(card.to_json() for card in cards)
    return [json.dumps(json_cards, indent=2).encode('utf-8')]

class DealCards:
    def __init__(self, hand_size=5, seed=None):
        self.hand_size = hand_size
        random.seed(seed)
        self.deck = deck_factory()
        self.offset = 0
    def __call__(self, environ, start_response):
        if self.offset + self.hand_size >= len(self.deck):
            self.deck = deck_factory()
            self.offset = 0
        cards = self.deck[self.offset:self.offset+self.hand_size]
        self.offset += self.hand_size
        status = "{status.value} {status.phrase}".format(status=HTTPStatus.OK)
        headers = [('Content-Type', 'application/json;charset=utf-8')]
        start_response(status, headers)
        json_cards = list(card.to_json() for card in cards)
        return [json.dumps(json_cards, indent=2).encode('utf-8')]

from urllib.parse import parse_qs
class JSON_Filter:
    def __init__(self, json_app):
        self.json_app = json_app
    def __call__(self, environ, start_response):
        if 'HTTP_ACCEPT' in environ:
            if 'json' in environ['HTTP_ACCEPT']:
                environ['$format'] = 'json'
                return self.json_app(environ, start_response)
        decoded_query = parse_qs(environ['QUERY_STRING'])
        if '$format' in decoded_query:
            if decoded_query['$format'][0].lower() == 'json':
                environ['$format'] = 'json'
                return self.json_app(environ, start_response)
        status = "{status.value} {status.phrase}".format(status=HTTPStatus.BAD_REQUEST)
        headers = [('Content-Type', 'text/plain;charset=utf-8')]
        start_response(status, headers)
        return ["Request doesn't include ?$format=json or Accept header".encode('utf-8')]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    from wsgiref.simple_server import make_server
    #dealer = DealCards()
    json_wrapper = JSON_Filter(deal_cards)

    httpd = make_server('', 8080, json_wrapper)
    httpd.serve_forever()
