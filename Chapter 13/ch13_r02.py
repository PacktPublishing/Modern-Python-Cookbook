"""Python Cookbook

Chapter 13, recipe 2.
"""

import yaml

def load_config_file(config_file) -> dict:
    '''Loads a configuration mapping object with contents
    of a given file.

    :param config_file: File-like object that can be read.
    :returns: mapping with configuration parameter values
    '''
    document = yaml.load(config_file)
    return document

demo_text = '''
query:
  mz:
    - ANZ532
    - AMZ117
    - AMZ080
url:
  scheme: http
  netloc: forecast.weather.gov
  path: shmrn.php
description: >
  Weather forecast for Offshore including the Bahamas
'''


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        return "{rank} {suit}".format_map(vars(self))

card_text = '''
!!python/object/apply:__main__.Card
kwds:
    rank: 7
    suit: ♣︎
'''

import collections
od_text = '''
!!python/object/apply:collections.OrderedDict
args:
    -   !!omap
        -   key1: string value
        -   numerator: 355
        -   denominator: 113
'''


__test__ = {
    'load_config_file':
'''
>>> from pprint import pprint
>>> pprint(load_config_file(demo_text))
{'description': 'Weather forecast for Offshore including the Bahamas\\n',
 'query': {'mz': ['ANZ532', 'AMZ117', 'AMZ080']},
 'url': {'netloc': 'forecast.weather.gov',
         'path': 'shmrn.php',
         'scheme': 'http'}}
''',

    'load_card':
'''
>>> yaml.load(card_text)
7 ♣︎
''',

    'load_OrderedDict':
'''
>>> yaml.load(od_text)
OrderedDict([('key1', 'string value'), ('numerator', 355), ('denominator', 113)])

'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
