"""
{
    "swagger": "2.0",
    "info": {
      "title": "Python Cookbook\\nChapter 12, recipe 3.",
      "version": "1.0"
    },
    "schemes": "http",
    "host": "127.0.0.1:5000",
    "basePath": "/dealer",
    "consumes": "application/json",
    "produces": "application/json",
    "paths": {
      "/hands": {
          "get": {
              "parameters": [
                 {"name": "cards",
                  "in": "query",
                  "description": "number of cards in each hand",
                  "type": "array", "items": {"type": "integer"},
                  "collectionFormat": "multi",
                  "default": [13, 13, 13, 13]
                 }
              ],
              "responses": {
                  "200": {
                      "description": "one hand of cards for each `hand` value in the query string"
                  }
              }
          }
      },
      "/hand": {
          "get": {
              "parameters": [
                  {"name": "cards", "in": "query", "type": "integer", "default": 5}
              ],
              "responses": {
                  "200": {
                      "description": "One hand of cards with a size given by the `hand` value in the query string"
                  }
              }
          }
      }
    }
}
"""
import random
from ch12_r01 import Card, Deck
from flask import Flask, jsonify, request, abort
from http import HTTPStatus

dealer = Flask('dealer')

specification = {
    'swagger': '2.0',
    'info': {
        'title': '''Python Cookbook\nChapter 12, recipe 3.''',
        'version': '1.0'
    },
    'schemes': ['http'],
    'host': '127.0.0.1:5000',
    'basePath': '/dealer',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'paths': {
        '/hands': {
            'get': {
                'parameters': [
                    {
                        'name': 'cards',
                        'in': 'query',
                        'description': 'number of cards in each hand',
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'collectionFormat': 'multi',
                        'default': [13, 13, 13, 13]
                    }
                ],
                'responses': {
                    '200': {
                        'description': '''One hand of cards for each `hand` value in the query string'''
                    }
                }
            }
        },
        '/hand': {
            'get': {
                'parameters': [
                    {
                        'name': 'cards',
                        'in': 'query',
                        'type': 'integer',
                        'default': 5
                    }
                ],
                'responses': {
                    '200': {
                        'description': '''One hand of cards with a size given by the `hand` value in the query string'''
                    }
                }
            }
        }
    }
}


import os
random.seed(os.environ.get('DEAL_APP_SEED'))
deck = Deck()

@dealer.before_request
def check_json():
    if request.path == '/dealer/swagger.json':
        return
    if 'json' in request.headers.get('Accept', '*/*'):
        return
    if 'json' == request.args.get('$format', 'html'):
        return
    return abort(HTTPStatus.BAD_REQUEST)

from flask import send_file
# @dealer.route('/dealer/swagger.json')
def swagger1():
    response = send_file('swagger.json', mimetype='application/json')
    return response

from flask import make_response
# @dealer.route('/dealer/swagger.json')
def swagger2():
    response = make_response(__doc__.encode('utf-8'))
    response.headers['Content-Type'] = 'application/json'
    return response

from flask import make_response
import json
@dealer.route('/dealer/swagger.json')
def swagger3():
    response = make_response(json.dumps(specification, indent=2).encode('utf-8'))
    response.headers['Content-Type'] = 'application/json'
    return response

@dealer.route('/dealer/hand/')
def deal():
    try:
        hand_size = int(request.args.get('cards', 5))
        assert 1 <= hand_size < 53
    except Exception as ex:
        abort(HTTPStatus.BAD_REQUEST)
    cards = deck.deal(hand_size)
    response = jsonify([card.to_json() for card in cards])
    return response

@dealer.route('/dealer/hands/')
def multi_hand():
    try:
        hand_sizes = request.args.getlist('cards', type=int)
        if len(hand_sizes) == 0:
            hand_sizes = [13,13,13,13]
        assert all(1 <= hand_size < 53 for hand_size in hand_sizes)
        assert sum(hand_sizes) < 53
    except Exception as ex:
        dealer.logger.exception(ex)
        abort(HTTPStatus.BAD_REQUEST)
    hands = [deck.deal(hand_size) for hand_size in hand_sizes]
    response = jsonify(
        [
            {'hand':i, 'cards':[card.to_json() for card in hand]}
             for i, hand in enumerate(hands)
        ]
    )
    return response

if __name__ == "__main__":
    dealer.run(use_reloader=True, threaded=False)
