"""
 {
    "swagger": "2.0",
    "info": {
      "title": "Python Cookbook\\nChapter 12, recipe 2.",
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

import os
random.seed(os.environ.get('DEAL_APP_SEED'))
deck = Deck()

@dealer.before_request
def check_json():
    if 'json' in request.headers.get('Accept', '*/*'):
        return
    if 'json' == request.args.get('$format', 'html'):
        return
    return abort(HTTPStatus.BAD_REQUEST)

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

if __name__ == "__main__":
    dealer.run(use_reloader=True, threaded=False)
