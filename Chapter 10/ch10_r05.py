"""Python Cookbook

Chapter 10, recipe 5.

Raw data source: ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt
"""

from pathlib import Path
import csv
from types import SimpleNamespace
import json


def non_comment_iter(source):
    for line in source:
        if line[0] == '#':
            continue
        yield line

def raw_data_iter(source):
    header = ['year', 'month', 'decimal_date', 'average',
              'interpolated', 'trend', 'days']
    rdr = csv.DictReader(source,
        header, delimiter=' ', skipinitialspace=True)
    return rdr


def cleanse(row):
    return SimpleNamespace(
        year= int(row['year']),
        month= int(row['month']),
        decimal_date= float(row['decimal_date']),
        average= float(row['average']),
        interpolated= float(row['interpolated']),
        trend= float(row['trend']),
        days= int(row['days'])
    )

def get_data(source_file):
    non_comment_data = non_comment_iter(source_file)
    raw_data = raw_data_iter(non_comment_data)

    # print(list(raw_data)[:10])

    cleansed_data = (cleanse(row) for row in raw_data)

    # print(list(cleansed_data)[:10])
    return cleansed_data

from ch10_r03 import correlation
from ch10_r04 import regression
from statistics import mean, median

if __name__ == "__main__":
    source_path = Path('co2_mm_mlo.txt')
    with source_path.open() as source_file:

        co2_ppm = list(row.interpolated for row in get_data(source_file))
        print(len(co2_ppm))
        # print(co2_ppm)

        for tau in range(1,20):
            # print(co2_ppm[:-tau], co2_ppm[tau:])
            data = [{'x':x, 'y':y} for x,y in zip(co2_ppm[:-tau], co2_ppm[tau:])]
            r_tau_0 = correlation(data[:60])
            r_tau_60 = correlation(data[60:120])
            # print(tau, r_tau_0, r_tau_60)
            print("r_{{xx}}(τ={:2d}) = {:6.3f}".format(tau, r_tau_0))

        monthly_mean = [
            {'x': x, 'y': mean(co2_ppm[x:x+12])} for x in range(0,len(co2_ppm),12)
        ]

        # print(monthly_mean)
        alpha, beta = regression(monthly_mean)
        print( 'y=', alpha, '+x*', beta )
        r = correlation(monthly_mean)
        print('r^2=', r**2)

        for d in monthly_mean:
            print(d, "x=", d['x'], "y=", alpha+d['x']*beta)
