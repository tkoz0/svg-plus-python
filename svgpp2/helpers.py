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

def _checkFloat(num: float) -> float:
    '''
    Return nums converted to floats.
    Raises TypeError if not a number convertible to float (includes bool).
    Raises ValueError if it is inf or nan.
    '''
    if isinstance(num,bool) or not isinstance(num,(int,float)):
        raise TypeError(f'expected a number (int or float), not {type(num).__name__}')
    num = float(num)
    if not math.isfinite(num):
        raise ValueError(f'expected a finite number, not {num!r}')
    return num

def _checkTol(tol: float, /) -> float:
    '''
    Return the tolerance converted to float.
    Raises TypeError if not a number convertible to float.
    Raises ValueError if it is inf/nan or negative.
    '''
    if isinstance(tol,bool) or not isinstance(tol,(int,float)):
        raise TypeError(f'tol must be a number (int or float), not {type(tol).__name__}')
    tol = float(tol)
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError(f'tol must be finite and >= 0, tol = {tol!r}')
    return tol

def _checkTolAndScale(tol: float, scale: float, /) -> tuple[float,float]:
    '''
    Checks that tolerance and scale are >= 0.
    Return both tolerance and scale converted to float.
    '''
    if isinstance(tol,bool) or not isinstance(tol,(int,float)):
        raise TypeError(f'tol must be a number (int or float), not {type(tol).__name__}')
    if isinstance(scale,bool) or not isinstance(scale,(int,float)):
        raise TypeError(f'scale must be a number (int or float), not {type(tol).__name__}')
    tol = float(tol)
    scale = float(scale)
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError(f'tolerance must be finite and >= 0, tol = {tol!r}')
    if not math.isfinite(scale) or scale < 0.0:
        raise ValueError(f'scale must be finite and >= 0, scale = {scale!r}')
    return (tol,scale)

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
    if not isinstance(num,(int,float)):
        raise TypeError('num should be a number (int or float)')
    num = float(num)
    if not math.isfinite(num):
        raise ValueError(f'invalid number for SVG: {num}')
    if num == 0.0:
        num = 0.0 # avoid -0.0

    # convert to string
    if precision is None:
        result = str(num)
    elif isinstance(precision,bool) or not isinstance(precision,int):
        raise TypeError(f'precision must be an int, not {type(precision).__name__}')
    elif precision < 0:
        raise ValueError(f'precision must be an int >= 0, not {precision!r}')
    else:
        result = f'{num:.{precision}f}'

    # handle trailing zeroes
    if not isinstance(removeTrailingZeroes,bool):
        raise TypeError(f'removeTrailingZeroes must be a bool')
    if removeTrailingZeroes and '.' in result:
        result = result.rstrip('0').rstrip('.')
    # possible we end up with -0 depending on precision if number is negative
    # normalize all forms: -0, -0.0, -0.00, etc
    if result.startswith('-') and result[1:].replace('.','').replace('0','') == '':
        result = result[1:]

    return result

def numberFormatter(precision: int|None = None, removeTrailingZeroes: bool = False) \
        -> Callable[[float],str]:
    '''
    Return a function that formats a number using formatNumber with chosen precision and
    removeTrailingZeroes setting.
    '''
    # first test that the precision and trailing zeroes option are valid
    formatNumber(0.0,precision,removeTrailingZeroes)
    # then make a function to return
    def formatter(n: float):
        return formatNumber(n,precision,removeTrailingZeroes)
    # setting a name can help with debugging
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
