'''
Smaller utility functions
'''

import math
from typing import Callable

__all__ = [
    'formatNumber',
    'numberFormatter',
    'sincosRad',
    'sincosDeg'
]

def formatNumber(num: float, precision: int|None = None, removeTrailingZeroes: bool = False) -> str:
    '''
    Format a number for SVG output.

    Precision supported:
    - None: to use python default (shortest round trip)
    - int: number of digits after decimal point (must be >= 0)

    Trailing zeroes may be removed as well.

    Note that scientific notation may be used for huge or tiny values. Although
    this library tries to be robust for such scales, SVG diagram scales should
    prefer familiar numbers like 1-100.
    '''
    # validate input num
    if isinstance(num,bool):
        raise TypeError('num should be a number, not a bool')
    num = float(num)
    if math.isinf(num) or math.isnan(num):
        raise ValueError(f'invalid number for SVG: {num}')
    if num == 0.0:
        num = 0.0 # avoid -0.0

    # convert to string
    if precision is None:
        result = str(num)
    elif isinstance(precision,bool):
        raise TypeError('precision cannot be a bool')
    elif not isinstance(precision,int) or precision < 0:
        raise ValueError(f'precision must be an int >= 0')
    else:
        result = f'{num:.{precision}f}'

    # handle trailing zeroes
    if removeTrailingZeroes and '.' in result:
        result = result.rstrip('0').rstrip('.')
    # possible we end up with -0 depending on precision if number is negative
    if result == '-0':
        result = '0'

    return result

def numberFormatter(precision: int|None = None, removeTrailingZeroes: bool = False) \
        -> Callable[[float],str]:
    '''
    Return a function that formats a number using formatNumber with chosen precision and
    removeTrailingZeroes setting.
    '''
    def formatter(n: float):
        return formatNumber(n,precision,removeTrailingZeroes)
    formatter.__name__ = (f'numberFormatter(precision={precision!r},'
        f'removeTrailingZeroes={removeTrailingZeroes!r})')
    return formatter

def sincosRad(angleRad: float) -> tuple[float,float]:
    '''
    Simultaneously compute sine and cosine. Angle is in radians.
    '''
    return (math.sin(angleRad),math.cos(angleRad))

def sincosDeg(angleDeg: float) -> tuple[float,float]:
    '''
    Simultaneously compute sine and cosine. Angle is in degrees.
    '''
    return sincosRad(math.radians(angleDeg))
