"""Python Cookbook

Chapter 5, recipe 2
"""

from datetime import date, datetime

def get_date1():
    year = int(input("year: "))
    month = int(input("month [1-12]: "))
    day = int(input("day [1-31]: "))
    result = date(year, month, day)
    return result

def get_date2():
    raw_date_str = input("date [yyyy-mm-dd]: ")
    input_date = datetime.strptime(raw_date_str, '%Y-%m-%d').date()
    return input_date

def get_date_list(get_date=get_date1):
    d1 = get_date()
    more = input("Another? ").lower()
    results = [d1]
    while more.startswith("y"):
        d2 = get_date()
        results.append(d2)
        more = input("Another? ").lower()
    return results

import unittest

class GIVEN_get_date1_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input= Mock(side_effect=['2016', '4', '29'])
    def runTest(self):
        with patch('__main__.__builtins__.input', self.mock_input):
            d = get_date1()
        self.assertEqual(d, date(2016, 4, 29))
        self.mock_input.assert_has_calls(
            [call('year: '), call('month [1-12]: '), call('day [1-31]: ')]
            )

class GIVEN_get_date2_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input= Mock(side_effect=['2016-4-29'])
    def runTest(self):
        with patch('__main__.__builtins__.input', self.mock_input):
            d = get_date2()
        self.assertEqual(d, date(2016, 4, 29))
        self.mock_input.assert_has_calls(
            [call('date [yyyy-mm-dd]: ')]
            )

class GIVEN_get_date_list_WHEN_valid_THEN_date(unittest.TestCase):
    def setUp(self):
        self.mock_input= Mock(side_effect=['2016-4-29', 'y', '2016-5-2', 'n'])
    def runTest(self):
        with patch('__main__.__builtins__.input', self.mock_input):
            d = get_date_list(get_date2)
        self.assertEqual(d, [date(2016, 4, 29), date(2016, 5, 2)])
        self.mock_input.assert_has_calls(
            [call('date [yyyy-mm-dd]: ')]
            )

if __name__ == "__main__":
    import doctest
    # doctest.testmod(verbose=1)

    from unittest.mock import Mock, patch, call
    unittest.main(exit=False)
