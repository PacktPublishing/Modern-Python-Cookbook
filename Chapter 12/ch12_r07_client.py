"""Python Cookbook

Chapter 12, recipe 7 -- client.
"""

import urllib.request
import urllib.parse
import json

if __name__ == "__main__":

    # 1. Get the OpenAPI specification.

    swagger_request = urllib.request.Request(
        url = 'https://127.0.0.1:5000/dealer/swagger.json',
        method = "GET",
        headers = {
            'Accept': 'application/json',
        },
    )

    from pprint import pprint
    import ssl
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(swagger_request, context=context) as response:
        swagger = json.loads(response.read().decode("utf-8"))
        pprint(swagger)

    # 2. Post to create a player.

    full_url = urllib.parse.ParseResult(
        scheme="https",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/players",
        params=None,
        query=None,
        fragment=None
    )

    document = {
        'name': 'Hannah Bowers',
        'email': 'h@example.com',
        'year': 1987,
        'twitter': 'https://twitter.com/PacktPub',
        'password': 'OpenSesame'
    }

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "POST",
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
        },
        data = json.dumps(document).encode('utf-8')
    )

    try:
        with urllib.request.urlopen(request, context=context) as response:
            # print(response.status)
            assert response.status == 201
            print(response.headers)
            document = json.loads(response.read().decode("utf-8"))

        print(document)
        assert document['status'] == 'ok'
        id = document['id']
    except urllib.error.HTTPError as ex:
        print(ex.status)
        print(ex.headers)
        print(ex.read())

    # 3. GET to see the players. Requires ``Authorization`` header.

    from pprint import pprint
    import base64

    full_url = urllib.parse.ParseResult(
        scheme="https",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/players",
        params=None,
        query=None,
        fragment=None
    )

    credentials = base64.b64encode(b'75f1bfbda3a8492b74a33ee28326649c:OpenSesame')

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "GET",
        headers = {
            'Accept': 'application/json',
            'Authorization': b"BASIC " + credentials
        }
    )

    with urllib.request.urlopen(request, context=context) as response:
        assert response.status == 200
        # print(response.headers)
        players = json.loads(response.read().decode("utf-8"))

    pprint(players)

    # 4. GET to see a specific player.

    id = '75f1bfbda3a8492b74a33ee28326649c'
    full_url = urllib.parse.ParseResult(
        scheme="https",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/players/{id}".format(id=id),
        params=None,
        query=None,
        fragment=None
    )

    request = urllib.request.Request(
        url = urllib.parse.urlunparse(full_url),
        method = "GET",
        headers = {
            'Accept': 'application/json',
            'Authorization': b"BASIC " + credentials
        }
    )

    from urllib.error import HTTPError
    try:
        with urllib.request.urlopen(request, context=context) as response:
            print(response.status)
            print(response.headers)
            print(json.loads(response.read().decode("utf-8")))
    except HTTPError as ex:
        print(ex.status)
        print(ex.read())
