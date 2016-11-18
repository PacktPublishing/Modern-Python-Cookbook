"""Python Cookbook

Chapter 7, recipe 7.
"""

def writer_rule(iterable):
    for item in iterable:
        if 'Lake' in item['writer']:
            continue
        yield item

__test__ = {
    'chapter': '''
>>> from pprint import pprint
>>> source = [
...    {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
...    {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
...    {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
...    {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
...    {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
...    {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
...    {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

Find all items with "Lake" as a writer.

>>> data = source.copy()
>>> for item in data:
...    if 'Lake' in item['writer']:
...        print("remove", item['title'])
remove Stones of Years
remove Mass
remove Battlefield

Naive

>>> data = source.copy()
>>> for index in range(len(data)): # doctest: +IGNORE_EXCEPTION_DETAIL
...    if 'Lake' in data[index]['writer']:
...       del data[index]
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__.__test__.chapter[5]>", line 2, in <module>
    if 'Lake' in data[index]['writer']:
IndexError: list index out of range

Sequential Removal.

while x in list:
    list.remove(x)

>>> def index(data):
...    for i in range(len(data)):
...        if 'Lake' in data[i]['writer']:
...            return i

>>> data = source.copy()
>>> position = index(data)
>>> while position:
...    del data[position] # or data.pop(position)
...    position = index(data)
>>> pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]

# Better Sequential Removal.

>>> data = source.copy()
>>> i = 0
>>> while i != len(data):
...    if 'Lake' in data[i]['writer']:
...        del data[i]
...    else:
...        i += 1
>>> pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]

# Recursive Removal.

def remover(sub_list):
    if len(sub_list) == 0: return []
    head, *tail = sub_list
    if 'Lake' in head['writer']:
        return remover(tail)
    else:
        return [head] + remover(tail)
pprint(remover(source))

# Filtered Copy.

data = [item for item in source if not('Lake' in item['writer'])]
pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]

# Another Filter.

data = list(filter(lambda item: not('Lake' in item['writer']), source))
pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]

# Filter Function.

data = list(writer_rule(source))
pprint(data)
[{'time': '2:43', 'title': 'Eruption', 'writer': ['Emerson']},
 {'time': '1:16', 'title': 'Iconoclast', 'writer': ['Emerson']},
 {'time': '1:49', 'title': 'Manticore', 'writer': ['Emerson']},
 {'time': '3:54', 'title': 'Aquatarkus', 'writer': ['Emerson']}]

'''
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
