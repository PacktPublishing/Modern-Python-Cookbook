"""Python Cookbook

Chapter 8, recipe 2.
"""
from pprint import pprint

log_rows = \
[['date', 'engine on', 'fuel height'],
 ['', 'engine off', 'fuel height'],
 ['', 'Other notes', ''],
 ['10/25/13', '08:24:00 AM', '29'],
 ['', '01:15:00 PM', '27'],
 ['', "calm seas -- anchor solomon's island", ''],
 ['10/26/13', '09:12:00 AM', '27'],
 ['', '06:25:00 PM', '22'],
 ['', "choppy -- anchor in jackson's creek", '']]

def row_merge(source_iter):
    group = []
    for row in source_iter:
        if len(row[0]) != 0:
            if group:
                yield group
            group = row.copy()
        else:
            group.extend(row)
    if group:
        yield group

def skip_header_1(rows):
    row_iter = iter(rows)
    next(row_iter)
    return row_iter

def skip_header_date(rows):
    for row in rows:
        if row[0] == 'date': continue
        yield row

import datetime
def start_datetime(row):
    travel_date = datetime.datetime.strptime(row[0], "%m/%d/%y").date()
    start_time = datetime.datetime.strptime(row[1], "%I:%M:%S %p").time()
    start_datetime = datetime.datetime.combine(travel_date, start_time)
    new_row = row+[start_datetime]
    return new_row

def end_datetime(row):
    travel_date = datetime.datetime.strptime(row[0], "%m/%d/%y").date()
    end_time = datetime.datetime.strptime(row[4], "%I:%M:%S %p").time()
    end_datetime = datetime.datetime.combine(travel_date, end_time)
    new_row = row+[end_datetime]
    return new_row

def duration(row):
    travel_hours = round((row[10]-row[9]).total_seconds()/60/60, 1)
    new_row = row+[travel_hours]
    return new_row

def date_conversion(source):
    tail_gen = skip_header_date(source)
    start_gen = (start_datetime(row) for row in tail_gen)
    end_gen = (end_datetime(row) for row in start_gen)
    duration_gen = (duration(row) for row in end_gen)
    return duration_gen

from types import SimpleNamespace

def make_namespace(merge_iter):
    for row in merge_iter:
        ns = SimpleNamespace(
            date = row[0],
            start_time = row[1],
            start_fuel_height = row[2],
            end_time = row[4],
            end_fuel_height = row[5],
            other_notes = row[7]
        )
        yield ns


__test__ = {
    'row_merge': '''
>>> pprint(list(row_merge(log_rows)))
[['date',
  'engine on',
  'fuel height',
  '',
  'engine off',
  'fuel height',
  '',
  'Other notes',
  ''],
 ['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  ''],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '']]
''',

    'skip_header_1': '''
>>> rm = row_merge(log_rows)
>>> tail = skip_header_1(rm)
>>> pprint(list(tail))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  ''],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '']]
''',

    'skip_header_date': '''
>>> rm = row_merge(log_rows)
>>> tail = skip_header_date(rm)
>>> pprint(list(tail))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  ''],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '']]
''',

    'start_time': '''
>>> rm = row_merge(log_rows)
>>> tail = skip_header_date(rm)
>>> st = (start_datetime(row) for row in tail)
>>> pprint(list(st))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  '',
  datetime.datetime(2013, 10, 25, 8, 24)],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '',
  datetime.datetime(2013, 10, 26, 9, 12)]]
''',

    'start_time, end_time': '''
>>> rm = row_merge(log_rows)
>>> tail = skip_header_date(rm)
>>> st = (start_datetime(row) for row in tail)
>>> et = (end_datetime(row) for row in st)
>>> pprint(list(et))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  '',
  datetime.datetime(2013, 10, 25, 8, 24),
  datetime.datetime(2013, 10, 25, 13, 15)],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '',
  datetime.datetime(2013, 10, 26, 9, 12),
  datetime.datetime(2013, 10, 26, 18, 25)]]
''',

    'start_time, end_time, duration': '''
>>> rm = row_merge(log_rows)
>>> tail = skip_header_date(rm)
>>> st = (start_datetime(row) for row in tail)
>>> et = (end_datetime(row) for row in st)
>>> d = (duration(row) for row in et)
>>> pprint(list(d))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  '',
  datetime.datetime(2013, 10, 25, 8, 24),
  datetime.datetime(2013, 10, 25, 13, 15),
  4.8],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '',
  datetime.datetime(2013, 10, 26, 9, 12),
  datetime.datetime(2013, 10, 26, 18, 25),
  9.2]]
''',

    'date_conversion': '''
>>> converted = date_conversion(row_merge(log_rows))
>>> pprint(list(converted))
[['10/25/13',
  '08:24:00 AM',
  '29',
  '',
  '01:15:00 PM',
  '27',
  '',
  "calm seas -- anchor solomon's island",
  '',
  datetime.datetime(2013, 10, 25, 8, 24),
  datetime.datetime(2013, 10, 25, 13, 15),
  4.8],
 ['10/26/13',
  '09:12:00 AM',
  '27',
  '',
  '06:25:00 PM',
  '22',
  '',
  "choppy -- anchor in jackson's creek",
  '',
  datetime.datetime(2013, 10, 26, 9, 12),
  datetime.datetime(2013, 10, 26, 18, 25),
  9.2]]
''',

    'namespace': '''
>>> pprint(list(make_namespace(row_merge(log_rows)))) # doctest: +NORMALIZE_WHITESPACE
[namespace(date='date', end_fuel_height='fuel height',
    end_time='engine off', other_notes='Other notes',
    start_fuel_height='fuel height', start_time='engine on'),
 namespace(date='10/25/13', end_fuel_height='27',
    end_time='01:15:00 PM', other_notes="calm seas -- anchor solomon's island",
    start_fuel_height='29', start_time='08:24:00 AM'),
 namespace(date='10/26/13', end_fuel_height='22',
    end_time='06:25:00 PM', other_notes="choppy -- anchor in jackson's creek",
    start_fuel_height='27', start_time='09:12:00 AM')]
''',
}


if __name__ == "__main__":
    import doctest
    doctest.testmod()
