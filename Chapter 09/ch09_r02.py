"""Python Cookbook

Chapter 9, recipe 2.
"""

import csv
from pathlib import Path
from pprint import pprint

def raw():
    data_path = Path('waypoints.csv')
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            pprint(row)

import datetime
def clean_row(source_row):
    source_row['lat_n']= float(source_row['lat'])
    source_row['lon_n']= float(source_row['lon'])
    source_row['ts_date']= datetime.datetime.strptime(source_row['date'],'%Y-%m-%d').date()
    source_row['ts_time']= datetime.datetime.strptime(source_row['time'],'%H:%M:%S').time()
    source_row['timestamp']= datetime.datetime.combine(source_row['ts_date'], source_row['ts_time'])
    return source_row

def cleanse(reader):
    for row in reader:
        yield clean_row(row)

def clean():
    data_path = Path('waypoints.csv')
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        clean_data_reader = cleanse(data_reader)
        for row in clean_data_reader:
            pprint(row)

__test__ = {
    'raw': '''
>>> raw()
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lon': '-79.9338333333333',
 'time': '09:15:00'}
{'date': '2012-11-28',
 'lat': '31.6714833333333',
 'lon': '-80.93325',
 'time': '00:00:00'}
{'date': '2012-11-28',
 'lat': '30.7171666666667',
 'lon': '-81.5525',
 'time': '11:35:00'}
''',

    'clean': '''
>>> clean()
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lat_n': 32.8321666666667,
 'lon': '-79.9338333333333',
 'lon_n': -79.9338333333333,
 'time': '09:15:00',
 'timestamp': datetime.datetime(2012, 11, 27, 9, 15),
 'ts_date': datetime.date(2012, 11, 27),
 'ts_time': datetime.time(9, 15)}
{'date': '2012-11-28',
 'lat': '31.6714833333333',
 'lat_n': 31.6714833333333,
 'lon': '-80.93325',
 'lon_n': -80.93325,
 'time': '00:00:00',
 'timestamp': datetime.datetime(2012, 11, 28, 0, 0),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(0, 0)}
{'date': '2012-11-28',
 'lat': '30.7171666666667',
 'lat_n': 30.7171666666667,
 'lon': '-81.5525',
 'lon_n': -81.5525,
 'time': '11:35:00',
 'timestamp': datetime.datetime(2012, 11, 28, 11, 35),
 'ts_date': datetime.date(2012, 11, 28),
 'ts_time': datetime.time(11, 35)}
''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
