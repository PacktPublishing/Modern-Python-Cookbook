"""Python Cookbook

Chapter 3, Recipe 8
"""
import csv
import pathlib
from math import radians, sin, cos, sqrt, asin
from functools import partial

MI= 3959
NM= 3440
KM= 6373

def haversine( lat_1: float, lon_1: float,
    lat_2: float, lon_2: float, *, R: float ) -> float:
    """Distance between points.

    R is radius, R=MI computes in miles. Default is nautical miles.

    >>> round(haversine(36.12, -86.67, 33.94, -118.40, R=6372.8), 5)
    2887.25995
    """
    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sin(Δ_lat/2)**2 + cos(lat_1)*cos(lat_2)*sin(Δ_lon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

nm_haversine = partial(haversine, R=NM)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    source_path = pathlib.Path("waypoints.csv")
    with source_path.open() as source_file:
        reader= csv.DictReader(source_file)
        start = next(reader)
        for point in reader:
            d = nm_haversine(
                float(start['lat']), float(start['lon']),
                float(point['lat']), float(point['lon'])
                )
            print(start, point, d)
            start= point
