"""Python Cookbook

Chapter 12, recipe 5 -- server.
"""
import random
from ch12_r01 import Card, Deck
from flask import Flask, jsonify, request, abort, url_for
from http import HTTPStatus
import logging
import sys

dealer = Flask('dealer')
dealer.DEBUG=True

specification = {
    'swagger': '2.0',
    'info': {
        'title': '''Python Cookbook\nChapter 12, recipe 5.''',
        'version': '1.0'
    },
    'schemes': ['http'],
    'host': '127.0.0.1:5000',
    'basePath': '/dealer',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'paths': {
        '/decks/{id}/hands': {
            'get': {
                'parameters': [
                    {
                        'name': 'id',
                        'in': 'path',
                        'type': 'integer'
                    },
                    {
                        'name': 'cards',
                        'in': 'query',
                        'type': 'integer',
                        'default': 13,
                        'description': '''number of cards in each hand'''
                    },
                    {
                        'name': '$top',
                        'in': 'query',
                        'type': 'integer',
                        'default': 1,
                        'description': '''number of hands to deal'''
                    },
                    {
                        'name': '$skip',
                        'in': 'query',
                        'type': 'integer',
                        'default': 0,
                        'description': '''number of hands to skip before starting to deal'''
                    }
                ],
                'responses': {
                    '200': {
                        'description': '''One hand of cards for each `hand` value in the query string'''
                    },
                    '400': {
                        'description': '''Request doesn't accept a JSON response'''
                    },
                    '404': {
                        'description': '''ID not found.'''
                    }
                }
            }
        },
        '/decks': {
            'post': {
                'parameters': [
                    {
                        'name': 'size',
                        'in': 'query',
                        'type': 'integer',
                        'default': 1,
                        'description': '''number of decks to build and shuffle'''
                    }
                ],
                'responses': {
                    '200': {
                        'description': '''Create and shuffle a deck. Returns a unique deck id.''',
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'id': {'type': 'string'}
                            }
                        }
                    },
                    '400': {
                        'description': '''Request doesn't accept a JSON response'''
                    }
                }
            }
        }
    }
}


import os
random.seed(os.environ.get('DEAL_APP_SEED'))
decks = {}

@dealer.before_request
def check_json():
    if request.path == '/dealer/swagger.json':
        return
    if 'json' in request.headers.get('Accept', '*/*'):
        return
    if 'json' == request.args.get('$format', 'html'):
        return
    return abort(HTTPStatus.BAD_REQUEST)

from flask import make_response
import json
@dealer.route('/dealer/swagger.json')
def swagger3():
    response = make_response(json.dumps(specification, indent=2).encode('utf-8'))
    response.headers['Content-Type'] = 'application/json'
    return response

import urllib.parse
import uuid
@dealer.route('/dealer/decks', methods=['POST'])
def make_deck():
    id = str(uuid.uuid1())
    decks[id]= Deck()
    response_json = jsonify(
        status='ok',
        id=id
    )
    response = make_response(response_json, HTTPStatus.CREATED)
    response.headers['Location'] = url_for('get_deck', id=str(id))
    return response

@dealer.route('/dealer/decks/<id>', methods=['GET'])
def get_deck(id):
    if id not in decks:
        dealer.logger.debug(id)
        dealer.logger.debug(list(decks.keys()))
        abort(HTTPStatus.NOT_FOUND)
    response = jsonify([c.to_json() for c in decks[id].cards])
    return response

from werkzeug.exceptions import BadRequest

@dealer.route('/dealer/decks/<id>/hands', methods=['GET'])
def get_hands(id):
    if id not in decks:
        dealer.logger.debug(id)
        return make_response( 'ID {} not found'.format(id), HTTPStatus.NOT_FOUND)
    try:
        cards = int(request.args.get('cards',13))
        top = int(request.args.get('$top',1))
        skip = int(request.args.get('$skip',0))
        assert skip*cards+top*cards <= len(decks[id].cards), "$skip, $top, and cards larger than the deck"
    except ValueError as ex:
        return BadRequest(repr(ex))
    subset = decks[id].cards[skip*cards:(skip+top)*cards]
    hands = [subset[h*cards:(h+1)*cards] for h in range(top)]
    response = jsonify(
        [
            {'hand':i, 'cards':[card.to_json() for card in hand]}
             for i, hand in enumerate(hands)
        ]
    )
    return response

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    dealer.run(use_reloader=True, threaded=False)
