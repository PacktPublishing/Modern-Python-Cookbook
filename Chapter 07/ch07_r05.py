"""Python Cookbook

Chapter 7, recipe 5.
"""

from collections import defaultdict

from typing import *
def summarize(data) -> Mapping[str, List]:
    module_details = defaultdict(list)
    for event in data:
        module_details[event[2]].append(event)
    return module_details

class ModuleEvents(dict):
    def add_event(self, event):
        if event[2] not in self:
            self[event[2]] = list()
        self[event[2]].append(event)

__test__ = {
    'simple': '''
>>> data = [
...    ('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'),
...    ('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging'),
...    ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')
... ]

>>> from collections import defaultdict
>>> module_details = defaultdict(list)
>>> for row in data:
...     module_details[row[2]].append(row)

>>> sorted(module_details.items()) # doctest: +NORMALIZE_WHITESPACE
[('module1', [('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'), ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')]), ('module2', [('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging')])]
''',

    'function': '''
>>> data = [
...    ('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'),
...    ('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging'),
...    ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')
... ]
>>> module_details= summarize(data)
>>> sorted(module_details.items()) # doctest: +NORMALIZE_WHITESPACE
[('module1', [('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'), ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')]), ('module2', [('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging')])]
''',

    'class': '''
>>> data = [
...    ('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'),
...    ('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging'),
...    ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')
... ]
>>> module_details = ModuleEvents()
>>> for row in data:
...     module_details.add_event(row)
>>> sorted(module_details.items()) # doctest: +NORMALIZE_WHITESPACE
[('module1', [('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'), ('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')]), ('module2', [('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging')])]
''',
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
