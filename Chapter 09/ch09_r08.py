"""Python Cookbook

Chapter 9, recipe 8.
"""

from types import SimpleNamespace
from pathlib import Path
import csv


waypoints_path = Path('waypoints.csv')

if __name__ == "__main__":

    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.DictReader(waypoints_file)
        ns_reader = (SimpleNamespace(**row) for row in raw_reader)
        for row in ns_reader:
            print(row)

import datetime
make_date = lambda txt: datetime.datetime.strptime(txt, '%Y-%m-%d').date()
make_time = lambda txt: datetime.datetime.strptime(txt, '%H:%M:%S').time()
make_timestamp = lambda date, time: datetime.datetime.combine(
            make_date(date),
            make_time(time)
        )

def make_row(source):
    return SimpleNamespace(
        lat = float(source['lat']),
        lon = float(source['lon']),
        timestamp = make_timestamp(source['date'], source['time'])
    )

if __name__ == "__main__":

    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.DictReader(waypoints_file)
        ns_reader = (make_row(row) for row in raw_reader)
        for row in ns_reader:
            print(row)
