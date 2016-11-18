"""Python Cookbook

Chapter 11, recipe 8. Test Module.
"""
import unittest
import doctest
import json

import ch11_r08_load

class GIVEN_ElasticClient_WHEN_load_eventlog_THEN_request(unittest.TestCase):

    def create_response(self):
        self.database_id = hex(hash(self.mock_urlopen.call_args[0][0].data))[2:]
        self.location = '/v0/eventlog/{id}'.format(id=self.database_id)
        response_headers = [
            ('Location', self.location),
            ('ETag', self.database_id),
            ('Content-Type', 'application/json'),
        ]
        return Mock(
            status = 201,
            getheaders = Mock(return_value=response_headers)
        )

    def setUp(self):
        # The context manager object itself.
        self.mock_context = Mock(
            __exit__ = Mock(return_value=None),
            __enter__ = Mock(
                side_effect = self.create_response
            ),
        )

        # The urlopen() function that returns a context.
        self.mock_urlopen = Mock(
            return_value = self.mock_context,
        )

        # The test document.
        self.document = {
            "timestamp": "2016-06-15T17:57:54.715",
            "levelname": "INFO",
            "module": "ch09_r10",
            "message": "Sample Message One"
        }

    def runTest(self):

        with patch('ch11_r08_load.urllib.request.urlopen', self.mock_urlopen):
            client = ch11_r08_load.ElasticClient('Aladdin', 'OpenSesame')
            response = client.load_eventlog(self.document)
        self.assertEqual(self.location, response)

        call_request = self.mock_urlopen.call_args[0][0]
        # print(vars(call_request))

        self.assertEqual('https://api.orchestrate.io/v0/eventlog', call_request.full_url)
        self.assertDictEqual(
            {'Accept': 'application/json',
             'Authorization': 'Basic QWxhZGRpbjpPcGVuU2VzYW1l',
             'Content-type': 'application/json'}, call_request.headers)
        self.assertEqual('POST', call_request.method)
        self.assertEqual(json.dumps(self.document).encode('utf-8'), call_request.data)
        # print(self.mock_context.mock_calls)
        self.mock_context.__enter__.assert_called_once_with()
        self.mock_context.__exit__.assert_called_once_with(None, None, None)

def load_tests(loader, standard_tests, pattern):
    dt = doctest.DocTestSuite(ch11_r08_load)
    standard_tests.addTests(dt)
    return standard_tests

if __name__ == "__main__":
    from unittest.mock import *
    unittest.main(exit=False)
