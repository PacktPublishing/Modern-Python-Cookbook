"""Python Cookbook

Chapter 8, recipe 10.
"""

document = {
    "field": "value1",
    "field2": "value",
    "array": [
        {"array_item_key1": "value"},
        {"array_item_key2": "array_item_value2"}
    ],
    "object": {
        "attribute1": "value",
        "attribute2": "value2"
    }
}


def find_path(value, node, path=[]):
    if isinstance(node, dict):
        for key in sorted(node.keys()):
            yield from find_path(value, node[key], path+[key])
    elif isinstance(node, list):
        for index in range(len(node)):
            yield from find_path(value, node[index], path+[index])
    else:
        if node == value:
            yield path

import math
def factor_list(x):
    limit = int(math.sqrt(x)+1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            return [n] + factor_list(q)
    return [x]

def factor_iter(x):
    limit = int(math.sqrt(x)+1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            yield n
            yield from factor_iter(q)
            return
    yield x

__test__ = {
    'find value1': '''
>>> list(find_path('value1', document))
[['field']]
''',

    'find array_item_value2': '''
>>> list(find_path('array_item_value2', document))
[['array', 1, 'array_item_key2']]
''',

    'find object_value2': '''
>>> list(find_path('value2', document))
[['object', 'attribute2']]
''',

    'find value': '''
>>> list(find_path('value', document))
[['array', 0, 'array_item_key1'], ['field2'], ['object', 'attribute1']]
''',

    'factor_list': '''
>>> factor_list(255255)
[3, 5, 7, 11, 13, 17]
>>> list(factor_iter(255255))
[3, 5, 7, 11, 13, 17]
>>> from collections import Counter
>>> Counter(factor_iter(384))
Counter({2: 7, 3: 1})
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
