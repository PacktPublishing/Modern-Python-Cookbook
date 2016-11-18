"""Python Cookbook

Chapter 11, recipe 6.
"""

import unittest

import datetime
import json
from pathlib import Path

def save_data(some_payload):
    now_date = datetime.datetime.utcnow()
    now_text = now_date.strftime('extract_%Y%m%d%H%M%S')
    file_path = Path(now_text).with_suffix('.json')
    with file_path.open('w') as target_file:
        json.dump(some_payload, target_file, indent=2)

class GIVEN_data_WHEN_save_data_THEN_file(unittest.TestCase):
    def setUp(self):
        self.data = {'primes': [2, 3, 5, 7, 11, 13, 17, 19]}
        self.mock_datetime = Mock(
            datetime = Mock(
                utcnow = Mock(
                    return_value = datetime.datetime(2017, 7, 4, 1, 2, 3)
                )
            )
        )
        self.expected_name = 'extract_20170704010203.json'
        self.expected_path = Path(self.expected_name)
        if self.expected_path.exists():
            self.expected_path.unlink()

    def runTest(self):
        with patch('__main__.datetime', self.mock_datetime):
            save_data(self.data)
        with self.expected_path.open() as result_file:
            result_data = json.load(result_file)
        self.assertDictEqual(self.data, result_data)

        self.mock_datetime.datetime.utcnow.assert_called_once_with()
        self.assertFalse( self.mock_datetime.datetime.called )


if __name__ == "__main__":
    from unittest.mock import *
    unittest.main(exit=False)
