'''
Smaller utility functions
'''

import math

__all__ = [
    'formatNumber',
    'numberFormatter'
]

def formatNumber(num: float, precision: int|None = None, removeTrailingZeroes = False) -> str:
    '''
    Format a number for SVG output.

    Precision supported:
    - None: to use python default (shortest round trip)
    - int: number of digits after decimal point (must be >= 0)

    Trailing zeroes may be removed as well.
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
    elif isinstance(precision,bool) or not isinstance(precision,int) or precision < 0:
        raise ValueError(f'precision must be an int >= 0')
    else:
        result = f'{num:.{precision}f}'

    # handle trailing zeroes
    if removeTrailingZeroes and '.' in result:
        result = result.rstrip('0').rstrip('.')

    return result

def numberFormatter(precision: int|None = None, removeTrailingZeroes = False):
    '''
    Return a function that formats a number using formatNumber with chosen precision and
    removeTrailingZeroes setting.
    '''
    def formatter(n: float):
        return formatNumber(n,precision,removeTrailingZeroes)
    return formatter
