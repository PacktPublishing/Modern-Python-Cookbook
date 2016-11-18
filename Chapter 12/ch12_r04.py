"""Python Cookbook

Chapter 12, recipe 4.
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

    query = {'hand': 5}

    full_url = urllib.parse.ParseResult(
        scheme="http",
        netloc="127.0.0.1:5000",
        path="/dealer" + "/hand/",
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

    with urllib.request.urlopen(request) as response:
        print(response.status)
        print(response.headers)
        print(json.loads(response.read().decode("utf-8")))


    swagger_request = urllib.request.Request(
        url = 'http://127.0.0.1:5000/dealer/swagger.json',
        method = "GET",
        headers = {
            'Accept': 'application/json',
        }
    )

    from pprint import pprint
    with urllib.request.urlopen(swagger_request) as response:
        swagger = json.loads(response.read().decode("utf-8"))
        print(swagger)
