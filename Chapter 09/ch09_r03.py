"""Python Cookbook

Chapter 9, recipe 3.
"""

import re
from pathlib import Path
from pprint import pprint

pattern_text = (r'\[(?P<date>\d+-\d+-\d+ \d+:\d+:\d+,\d+)\]'
    '\s+(?P<level>\w+)'
    '\s+in\s+(?P<module>[\w_\.]+):'
    '\s+(?P<message>.*)')
pattern = re.compile(pattern_text)

def log_parser(source_line):
    match = pattern.match(source_line)
    if match is None:
        raise ValueError(
            "Unexpected input {0!r}".format(source_line))
    return match.groupdict()

def raw():
    data_path = Path('sample.log')
    with data_path.open() as data_file:
        data_reader = map(log_parser, data_file)
        for row in data_reader:
            pprint(row)

def copy():
    import csv
    data_path = Path('sample.log')
    target_path = data_path.with_suffix('.csv')
    with target_path.open('w', newline='') as target_file:
        writer = csv.DictWriter(
            target_file,
            ['date', 'level', 'module', 'message']
            )
        writer.writeheader()

        with data_path.open() as data_file:
            reader = map(log_parser, data_file)
            writer.writerows(reader)


__test__ = {
    'raw': '''
>>> raw()
{'date': '2016-05-08 11:08:18,651',
 'level': 'INFO',
 'message': 'Sample Message One',
 'module': 'ch09_r09'}
{'date': '2016-05-08 11:08:18,651',
 'level': 'DEBUG',
 'message': 'Debugging',
 'module': 'ch09_r09'}
{'date': '2016-05-08 11:08:18,652',
 'level': 'WARNING',
 'message': 'Something might have gone wrong',
 'module': 'ch09_r09'}

''',
}
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    copy()
