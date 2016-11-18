"""Python Cookbook

Chapter 11, recipe 7.
"""

import unittest

import random
def resample(population, N):
    for i in range(N):
        sample = random.choice(population)
        yield sample

class GIVEN_resample_WHEN_evaluated_THEN_fair(unittest.TestCase):
    def setUp(self):
        self.data = [2, 3, 5, 7, 11, 13, 17, 19]
        self.expected_resample_data = [23, 29, 31, 37, 41, 43, 47, 53]
        self.mock_random = Mock(
            choice = Mock(
                side_effect = self.expected_resample_data
            )
        )

    def runTest(self):
        with patch('__main__.random', self.mock_random):
            resample_data = list(resample(self.data, 8))

        self.assertListEqual(self.expected_resample_data, resample_data)

        self.mock_random.choice.assert_has_calls( 8*[call(self.data)] )


if __name__ == "__main__":
    from unittest.mock import *
    unittest.main(exit=False)
