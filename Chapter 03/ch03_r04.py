"""Python Cookbook

Chapter 3, recipe 4
"""
from typing import *
#from fractions import Fraction
from decimal import Decimal

Number = Union[int, float, complex, Decimal]

def temperature(*,
    f_temp: Optional[Number]=None,
    c_temp: Optional[Number]=None) -> Mapping[str, Number]:

    if c_temp is None and f_temp is not None:
        c_temp = 5*(f_temp-32)/9
    elif f_temp is None and c_temp is not None:
        f_temp = 32+9*c_temp/5
    else:
        raise Exception( "Logic Design Problem" )
    result = {'c_temp': c_temp,
        'f_temp': f_temp} # type: Dict[str, Number]
    return result


def temperature_bad(*,
    f_temp: Optional[Number]=None,
    c_temp: Optional[Number]=None) -> Number:

    if c_temp is None and f_temp is not None:
        c_temp = 5*(f_temp-32)/9
    elif f_temp is None and c_temp is not None:
        f_temp = 32+9*c_temp/5
    else:
        raise Exception( "Logic Design Problem" )
    result = {'c_temp': c_temp,
        'f_temp': f_temp} # type: Dict[str, Number]
    return result
