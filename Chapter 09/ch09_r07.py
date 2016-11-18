"""Python Cookbook

Chapter 9, recipe 7.
"""

from collections import namedtuple
from pathlib import Path
import csv


Waypoint = namedtuple('Waypoint', ['lat', 'lon', 'date', 'time'])

waypoints_path = Path('waypoints.csv')

if __name__ == "__main__":

    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        waypoints_reader = (Waypoint(*row) for row in raw_reader)
        for row in waypoints_reader:
            print(row)


Waypoint_Data = namedtuple('Waypoint_Data', ['lat', 'lon', 'timestamp'])

import datetime
parse_date = lambda txt: datetime.datetime.strptime(txt, '%Y-%m-%d').date()
parse_time = lambda txt: datetime.datetime.strptime(txt, '%H:%M:%S').time()
def convert_waypoint(waypoint):
    return Waypoint_Data(
        lat = float(waypoint.lat),
        lon = float(waypoint.lon),
        timestamp = datetime.datetime.combine(
            parse_date(waypoint.date),
            parse_time(waypoint.time)
        )
    )

if __name__ == "__main__":

    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        skip_header = filter(lambda row: row[0] != 'lat', raw_reader)
        waypoints_reader = (Waypoint(*row) for row in skip_header)
        waypoints_data_reader = (convert_waypoint(wp) for wp in waypoints_reader)

        for row in waypoints_data_reader:
            print(row.lat, row.lon, row.timestamp)

    from itertools import starmap
    with waypoints_path.open() as waypoints_file:
        raw_reader = csv.reader(waypoints_file)
        waypoints_reader = starmap(Waypoint, raw_reader)
        for row in waypoints_reader:
            print(row)
