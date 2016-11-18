"""Python Cookbook

Chapter 6, recipe 8
"""
from collections import deque

class Leg:
    """
    >>> leg_1 = Leg()
    >>> leg_1.rate = 6.0 # knots
    >>> leg_1.distance = 35.6 # nautical miles
    >>> ("option 1 {leg.distance:.1f}nm"
    ... " at {leg.rate:.2f}kt"
    ... " = {leg.time:.2f}hr".format(leg=leg_1))
    'option 1 35.6nm at 6.00kt = 5.93hr'

    leg_1.distance = 38.2
    >>> ("option 2 {leg.distance:.1f}nm"
    ... " at {leg.rate:.2f}kt"
    ... " = {leg.time:.2f}hr".format(leg=leg_1))
    'option 2 35.6nm at 6.00kt = 5.93hr'

    leg_1.time= 7
    >>> ("option 3 {leg.distance:.1f}nm"
    ... " at {leg.rate:.2f}kt"
    ... " = {leg.time:.2f}hr".format(leg=leg_1))
    'option 3 35.6nm at 6.00kt = 5.93hr'

    """
    def __init__(self, rate=None, time=None, distance=None):
        self._changes= deque(maxlen=2)
        self._rate= rate
        if rate: self._calculate('rate')
        self._time= time
        if time: self._calculate('time')
        self._distance= distance
        if distance: self._calculate('distance')

    def _calculate(self, change):
        if change not in self._changes:
            self._changes.append(change)
        compute = {'rate', 'time', 'distance'} - set(self._changes)
        if compute == {'distance'}:
            self._distance = self._time * self._rate
        elif compute == {'time'}:
            self._time = self._distance / self._rate
        elif compute == {'rate'}:
            self._rate = self._distance / self._time

    @property
    def rate(self):
        return self._rate
    @rate.setter
    def rate(self, value):
        self._rate = value
        self._calculate('rate')

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time = value
        self._calculate('time')

    @property
    def distance(self):
        return self._distance
    @distance.setter
    def distance(self, value):
        self._distance = value
        self._calculate('distance')

class Leg_Alt:
    """
    >>> leg_2 = Leg_Alt(rate=6, distance=35.6)
    >>> round(leg_2.rate,1)
    6
    >>> round(leg_2.time,1)
    5.9
    >>> round(leg_2.distance,1)
    35.6

    >>> ("option 1 {leg.distance:.1f}nm"
    ... " at {leg.rate:.2f}kt"
    ... " = {leg.time:.2f}hr".format(leg=leg_2))
    'option 1 35.6nm at 6.00kt = 5.93hr'

    """
    def __init__(self, rate=None, time=None, distance=None):
        self._changes= deque(maxlen=2)
        self._rate= rate
        if rate: self._calculate('rate')
        self._time= time
        if time: self._calculate('time')
        self._distance= distance
        if distance: self._calculate('distance')

    def calc_distance(self):
        self._distance = self._time * self._rate
    def calc_time(self):
        self._time = self._distance / self._rate
    def calc_rate(self):
        self._rate = self._distance / self._time

    def _calculate(self, change):
        if change not in self._changes:
            self._changes.append(change)
        compute = {'rate', 'time', 'distance'} - set(self._changes)
        if len(compute) == 1:
            name = compute.pop()
            method = getattr(self, 'calc_'+name)
            method()

    @property
    def rate(self):
        return self._rate
    @rate.setter
    def rate(self, value):
        self._rate = value
        self._calculate('rate')

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time = value
        self._calculate('time')

    @property
    def distance(self):
        return self._distance
    @distance.setter
    def distance(self, value):
        self._distance = value
        self._calculate('distance')

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    leg_1 = Leg()
    leg_1.rate = 6.0 # knots
    leg_1.distance = 35.6 # nautical miles
    # print( vars(leg_1) )
    print("option 1 {leg.distance:.1f}nm at {leg.rate:.2f}kt = {leg.time:.2f}hr".
        format(leg=leg_1))
    leg_1.distance = 38.2
    print("option 2 {leg.distance:.1f}nm at {leg.rate:.2f}kt = {leg.time:.2f}hr".
        format(leg=leg_1))
    leg_1.time= 7
    print("option 3 {leg.distance:.1f}nm at {leg.rate:.2f}kt = {leg.time:.2f}hr".
        format(leg=leg_1))

    leg_2 = Leg_Alt(rate=6, distance=35.6)
    print(leg_2.rate, leg_2.time, leg_2.distance)
    print("option 1 {leg.distance:.1f}nm at {leg.rate:.2f}kt = {leg.time:.2f}hr".
        format(leg=leg_2))
