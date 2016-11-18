"""Python Cookbook

Chapter 11, recipe 4 and 5.
"""

from ch11_r01 import Summary

import unittest
import random

class GIVEN_Summary_WHEN_1k_samples_THEN_mean(unittest.TestCase):

    def setUp(self):
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)


    def runTest(self):
        for sample in self.data:
            self.summary.add(sample)

        self.assertEqual(500, self.summary.mean)
        self.assertEqual(500, self.summary.median)

class GIVEN_Summary_WHEN_1k_samples_THEN_mean_median(unittest.TestCase):

    def setUp(self):
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)
        for sample in self.data:
            self.summary.add(sample)

    def test_mean(self):
        self.assertEqual(500, self.summary.mean)

    def test_median(self):
        self.assertEqual(500, self.summary.median)

class GIVEN_Summary_WHEN_1k_samples_THEN_mode(unittest.TestCase):

    def setUp(self):
        self.summary = Summary()
        self.data = [500]*97
        # Build 103 more elements each item n occurs n times.
        for i in range(1,43):
            self.data += [i]*i
        random.shuffle(self.data)
        for sample in self.data:
            self.summary.add(sample)

    def test_mode(self):
        top_3 = self.summary.mode[:3]
        self.assertListEqual([(500,97), (42,42), (41,41)], top_3)

import ch11_r01
def load_tests(loader, standard_tests, pattern):
    import doctest
    dt = doctest.DocTestSuite(ch11_r01)
    standard_tests.addTests(dt)
    return standard_tests

if __name__ == "__main__":
    unittest.main(exit=False)
