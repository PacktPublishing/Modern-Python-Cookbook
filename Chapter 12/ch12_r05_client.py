"""Python Cookbook

Chapter 12, recipe 5 -- client.
"""

import urllib.request
import urllib.parse
import json

if __name__ == "__main__":

    try:
        from swagger_spec_validator import validate_spec_url
        validate_spec_url('http://127.0.0.1:5000/dealer/swagger.json')
        print("swagger.json is valid")
    except ImportError as ex:
        pass

    # 1. Get the OpenAPI specification.

    swagger_request = urllib.request.Request(
        url = 'http://127.0.0.1:5000/dealer/swagger.json',
        method = "GET",
        headers = {
            'Accept': 'application/json',
        }
    )

    from pprint import pprint
    with urllib.request.urlopen('http://127.0.0.1:5000/dealer/swagger.json') as response:
        swagger = json.loads(response.read().decode("utf-8"))
        print(swagger)

    # 2. Post to create a deck.

    full_url = urllib.parse.ParseResult(
        scheme="http",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/decks",
        params=None,
        query=None,
        fragment=None
    )

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "POST",
        headers = {
            'Accept': 'application/json',
        }
    )

    with urllib.request.urlopen(request) as response:
        # print(response.status)
        assert response.status == 201
        print(response.headers)
        document = json.loads(response.read().decode("utf-8"))

    print(document)
    assert document['status'] == 'ok'
    id = document['id']

    # 3. GET to see the deck (a debugging request.)

    full_url = urllib.parse.ParseResult(
        scheme="http",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/decks/{id}".format(id=id),
        params=None,
        query=None,
        fragment=None
    )

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "GET",
        headers = {
            'Accept': 'application/json',
        }
    )

    with urllib.request.urlopen(request) as response:
        assert response.status == 200
        # print(response.headers)
        # print(json.loads(response.read().decode("utf-8")))
        pass

    # 4. GET to see some Hands.

    query = {'$top': 4, 'cards': 13}

    full_url = urllib.parse.ParseResult(
        scheme="http",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/decks/{id}/hands".format(id=id),
        params=None,
        query=urllib.parse.urlencode(query),
        fragment=None
    )

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "GET",
        headers = {
            'Accept': 'application/json',
        }
    )

    from urllib.error import HTTPError
    try:
        with urllib.request.urlopen(request) as response:
            print(response.status)
            print(response.headers)
            print(json.loads(response.read().decode("utf-8")))
    except HTTPError as ex:
        print(ex.status)
        print(ex.read())
