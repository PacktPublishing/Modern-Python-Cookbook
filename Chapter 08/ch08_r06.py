"""Python Cookbook

Chapter 8, recipe 6.
"""
from ch08_r02 import row_merge, log_rows
import datetime
from types import SimpleNamespace

def make_namespace(row):
    ns = SimpleNamespace(
        date = row[0],
        start_time = row[1],
        start_fuel_height = row[2],
        end_time = row[4],
        end_fuel_height = row[5],
        other_notes = row[7]
    )
    return ns

def timestamp(date_text, time_text):
    date = datetime.datetime.strptime(date_text, "%m/%d/%y").date()
    time = datetime.datetime.strptime(time_text, "%I:%M:%S %p").time()
    timestamp = datetime.datetime.combine(date, time)
    return timestamp

def start_datetime(row_ns):
    row_ns.start_timestamp = timestamp(row_ns.date, row_ns.start_time)
    return row_ns

def end_datetime(row_ns):
    row_ns.end_timestamp = timestamp(row_ns.date, row_ns.end_time)
    return row_ns

def duration(row_ns):
    travel_time = row_ns.end_timestamp - row_ns.start_timestamp
    row_ns.travel_hours = round(travel_time.total_seconds()/60/60, 1)
    return row_ns

def fuel_use(row_ns):
    end_height = float(row_ns.end_fuel_height)
    start_height = float(row_ns.start_fuel_height)
    row_ns.fuel_change = start_height - end_height
    return row_ns

def fuel_per_hour(row_ns):
    row_ns.fuel_per_hour = row_ns.fuel_change/row_ns.travel_hours
    return row_ns

def remove_date(row_ns):
    return not(row_ns.date == 'date')

def clean_data(source):
    namespace_iter = map(make_namespace, source)
    fitered_source = filter(remove_date, namespace_iter)
    start_iter = map(start_datetime, fitered_source)
    end_iter = map(end_datetime, start_iter)
    delta_iter = map(duration, end_iter)
    fuel_iter = map(fuel_use, delta_iter)
    per_hour_iter = map(fuel_per_hour, fuel_iter)
    return per_hour_iter

def total_fuel(iterable):
    """
    >>> round(total_fuel(clean_data(row_merge(log_rows))), 3)
    7.0
    """
    return sum(row.fuel_change for row in iterable)

from statistics import mean
def avg_fuel_per_hour(iterable):
    """
    >>> round(avg_fuel_per_hour(clean_data(row_merge(log_rows))), 3)
    0.48
    """
    return mean(row.fuel_per_hour for row in iterable)

from statistics import stdev
def stdev_fuel_per_hour(iterable):
    """
    >>> round(stdev_fuel_per_hour(clean_data(row_merge(log_rows))), 4)
    0.0897
    """
    return stdev(row.fuel_per_hour for row in iterable)

def summary():
    """
    >>> summary()
    Fuel use 0.48 ±0.18
    """
    data = tuple(clean_data(row_merge(log_rows)))
    m = avg_fuel_per_hour(data)
    s = 2*stdev_fuel_per_hour(data)

    print("Fuel use {m:.2f} ±{s:.2f}".format(m=m, s=s))

def summary_t():
    """
    >>> summary_t()
    Fuel use 0.48 ±0.18
    """
    from itertools import tee
    data1, data2 = tee(clean_data(row_merge(log_rows)), 2)
    m = avg_fuel_per_hour(data1)
    s = 2*stdev_fuel_per_hour(data2)
    print("Fuel use {m:.2f} ±{s:.2f}".format(m=m, s=s))

from pprint import pprint
def details(iterable):
    """
    >>> details(clean_data(row_merge(log_rows))) # doctest: +NORMALIZE_WHITESPACE
    namespace(date='10/25/13', end_fuel_height='27', end_time='01:15:00 PM',
    end_timestamp=datetime.datetime(2013, 10, 25, 13, 15),
    fuel_change=2.0,
    fuel_per_hour=0.4166666666666667,
    other_notes="calm seas -- anchor solomon's island",
    start_fuel_height='29', start_time='08:24:00 AM',
    start_timestamp=datetime.datetime(2013, 10, 25, 8, 24),
    travel_hours=4.8)
    namespace(date='10/26/13', end_fuel_height='22', end_time='06:25:00 PM',
    end_timestamp=datetime.datetime(2013, 10, 26, 18, 25),
    fuel_change=5.0,
    fuel_per_hour=0.5434782608695653,
    other_notes="choppy -- anchor in jackson's creek",
    start_fuel_height='27', start_time='09:12:00 AM',
    start_timestamp=datetime.datetime(2013, 10, 26, 9, 12),
    travel_hours=9.2)
    """
    for row in iterable:
        pprint(row)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
