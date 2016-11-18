"""Python Cookbook

Chapter 11, recipe 8, Spike.

Database hosting on orchestrate.io.
This is a technical spike to understand three of the service endpoints.
"""
from ch11_r08_load import log_data_iter

import urllib.request
import base64

service = "https://api.orchestrate.io"
api_key = "REDACTED"

def basic_header(username, password):
    combined_bytes = (username + ':' + password).encode('utf-8')
    encoded_bytes = base64.b64encode(combined_bytes)
    return 'Basic ' + encoded_bytes.decode('ascii')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': basic_header(api_key, '')
}

if __name__ == "__main__":

    #
    # 1. Check the API Key

    request = urllib.request.Request(
        url=service + "/v0/",
        headers=headers,
        method='HEAD'
    )

    from pprint import pprint
    import json
    with urllib.request.urlopen(request) as response:
        print(response.status)
        pprint(response.getheaders())
        body = response.read().decode('utf-8')
        if body:
            print(json.loads(body))

    #
    # 2. Post a new event

    data_document = {
            "timestamp": "2016-06-15T17:57:54.715",
            "levelname": "INFO",
            "module": "ch09_r10",
            "message": "Sample Message One"
        }

    request = urllib.request.Request(
        url=service + '/v0/eventlog',
        headers=headers,
        method='POST',
        data=json.dumps(data_document).encode('utf-8')
    )

    with urllib.request.urlopen(request) as response:
        print(response.status)
        pprint(response.getheaders())
        body = response.read().decode('utf-8')
        if body:
            print(json.loads(body))

    #
    # 3. Query event log

    request = urllib.request.Request(
        url=service + '/v0/eventlog',
        headers=headers,
        method='GET'
    )

    with urllib.request.urlopen(request) as response:
        print(response.status)
        pprint(response.getheaders())
        body = response.read().decode('utf-8')
        if body:
            print(json.loads(body))
