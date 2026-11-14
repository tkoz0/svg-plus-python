'''
Tests for helper functions.
'''

from svgpp2.helpers import formatNumber, numberFormatter, sincosRad, sincosDeg
from svgpp2.helpers import _checkFloat, _checkTol, _checkTolAndScale

import math
import pytest

class TestCheckFloats:

    def testTypeError(self):
        for value in (True,False,'','0','3.6','-5.8'):
            with pytest.raises(TypeError):
                _checkFloat(value) # type:ignore

    def testValueError(self):
        for value in (math.inf,-math.inf,math.nan):
            with pytest.raises(ValueError):
                _checkFloat(value)

    def testValid(self):
        for value in (0,-5,1.1,-6.0):
            assert _checkFloat(value) == value

    # pathological size numbers
    def testOverflowError(self):
        for value in (10**400,-10**500):
            with pytest.raises(OverflowError):
                _checkFloat(value)

class TestCheckTol:

    def testTypeError(self):
        for tol in ('a','False','True',False,True,'0.1',''):
            with pytest.raises(TypeError):
                _checkTol(tol) # type:ignore

    def testValueError(self):
        for tol in (-1,-2.0,math.inf,math.nan,-math.inf,-42,-1e-6):
            with pytest.raises(ValueError):
                _checkTol(tol)

    def testValid(self):
        for tol in (0.0,1e-300,1e-30,1e-15,1e-9,1e-6,1e-3,1.0,1e3,1e6,-0.0,0,1,1000):
            assert _checkTol(tol) == tol

class TestCheckTolAndScale:

    def testTypeError(self):
        for tol,scale in (
            (False,'a'),
            ('b',True),
            (True,True),
            ('0','0'),
            ('','')
        ):
            with pytest.raises(TypeError):
                _checkTolAndScale(tol,scale) # type:ignore

    def testValueError(self):
        for tol,scale in (
            (-0.1,0.1),
            (0.1,-0.1),
            (-1,1),
            (1,-1),
            (math.nan,1e-9),
            (1e-9,-math.inf),
            (math.inf,math.inf)
        ):
            with pytest.raises(ValueError):
                _checkTolAndScale(tol,scale)

    def testValid(self):
        for tol,scale in (
            (0.0,0.0),
            (0,0),
            (1,0.3),
            (1e-9,42),
            (1e-300,1e300),
            (1e-9,1e-9),
            (1e-12,1e-9),
            (0.0,1e-6),
            (1e-12,0),
            (1,0.1)
        ):
            assert _checkTolAndScale(tol,scale) == (tol,scale)

class TestFormatNumber:

    def testNumTypeError(self):
        for num in ('',True,False,'-5.5','0','1.0'):
            with pytest.raises(TypeError):
                formatNumber(num) # type:ignore

    def testNumValueError(self):
        for num in (math.inf,-math.inf,math.nan):
            with pytest.raises(ValueError):
                formatNumber(num)

    def testPrecTypeError(self):
        for prec in (True,False,'','1',0.1):
            with pytest.raises(TypeError):
                formatNumber(0.0,prec) # type:ignore

    def testPrecValueError(self):
        for prec in (-1,-2):
            with pytest.raises(ValueError):
                formatNumber(0.0,prec)

    def testRemoveZeroesTypeError(self):
        for removeZeroes in (2,3,-1.1,1.0,'','1','True','False'):
            with pytest.raises(TypeError):
                formatNumber(0.0,removeTrailingZeroes=removeZeroes) # type:ignore

    def testDefault(self):
        # default uses str(num) except -0.0 converts to +0.0
        assert formatNumber(0.0) == '0.0'
        assert formatNumber(-0.0) == '0.0'
        assert formatNumber(3.14) == '3.14'
        assert formatNumber(-0.01) == '-0.01'
        assert formatNumber(0.00009) == '9e-05'
        assert formatNumber(0.0001) == '0.0001'
        assert formatNumber(999.999) == '999.999'
        assert formatNumber(3.141592653589793) == '3.141592653589793'
        assert formatNumber(-0.000001) == '-1e-06'
        assert formatNumber(-1e-12) == '-1e-12'
        assert formatNumber(9e15) == '9000000000000000.0'
        assert formatNumber(1e16) == '1e+16'
        assert formatNumber(7) == '7.0'
        assert formatNumber(-42) == '-42.0'
        assert formatNumber(1e307) == '1e+307'
        assert formatNumber(1e-307) == '1e-307'

    def testDefaultRemoveTrailing(self):
        for num,result in (
            (0.0,'0'),
            (-0.0,'0'),
            (-9,'-9'),
            (-9.0,'-9'),
            (42.0,'42'),
            (10.0,'10'),
            (-100,'-100'),
            (4.2,'4.2'),
            (-8.1,'-8.1'),
            (3.1416,'3.1416'),
            (-42.42,'-42.42')
        ):
            assert formatNumber(num,removeTrailingZeroes=True) == result

    def testPrecision(self):
        assert formatNumber(5.0,0) == '5'
        assert formatNumber(6.1,0) == '6'
        assert formatNumber(6.9,0) == '7'
        assert formatNumber(0.4,0) == '0'
        assert formatNumber(-0.4,0) == '0'
        assert formatNumber(1.5,0) == '2'
        assert formatNumber(2.5,0) == '2'
        assert formatNumber(42,0) == '42'
        assert formatNumber(-5.89,1) == '-5.9'
        assert formatNumber(-5.99,1) == '-6.0'
        assert formatNumber(42.42,1) == '42.4'
        assert formatNumber(18,1) == '18.0'
        assert formatNumber(1.333,2) == '1.33'
        assert formatNumber(1.667,2) == '1.67'
        assert formatNumber(-0.003,2) == '0.00'
        assert formatNumber(0.007,2) == '0.01'
        assert formatNumber(0.0001,2) == '0.00'
        assert formatNumber(2.71828,3) == '2.718'
        assert formatNumber(-1.05946,3) == '-1.059'
        assert formatNumber(1010.7179,3) == '1010.718'
        assert formatNumber(-996.1604,3) == '-996.160'
        assert formatNumber(0.0001,3) == '0.000'

    def testPrecisionRemoveTrailing(self):
        assert formatNumber(5,1,True) == '5'
        assert formatNumber(89,1,True) == '89'
        assert formatNumber(-62.0,2,True) == '-62'
        assert formatNumber(-62.13,2,True) == '-62.13'
        assert formatNumber(-62.503,2,True) == '-62.5'
        assert formatNumber(123.4,3,True) == '123.4'
        assert formatNumber(123.456,3,True) == '123.456'
        assert formatNumber(123,3,True) == '123'

    def testNegativeZero(self):
        assert formatNumber(-0.0) == '0.0'
        assert formatNumber(-0.4,0) == '0'
        assert formatNumber(-0.04,1) == '0.0'
        assert formatNumber(-0.003,2) == '0.00'
        assert formatNumber(-0.0002,3) == '0.000'
        assert formatNumber(-0.00001,4) == '0.0000'

    def testRemoveTrailing(self):
        # zero and negative zero
        assert formatNumber(0.0,None,True) == '0'
        assert formatNumber(-0.0,None,True) == '0'
        assert formatNumber(-0.4,0,True) == '0'
        assert formatNumber(-0.04,1,True) == '0'
        assert formatNumber(-0.003,2,True) == '0'
        assert formatNumber(-0.0002,3,True) == '0'
        assert formatNumber(-0.00001,4,True) == '0'
        # some actual numbers
        assert formatNumber(1.17,5,True) == '1.17'
        assert formatNumber(8.713,5,True) == '8.713'
        assert formatNumber(-1.6,4,True) == '-1.6'
        assert formatNumber(-2.718,4,True) == '-2.718'

class TestNumberFormatter:

    def testDefault(self):
        formatter = numberFormatter()
        for num in (0.0,-0.0,1.0,-1.0,5.13,1.7e12,2.6e50,-1e308,-6.126):
            assert formatter(num) == formatNumber(num)

    def testWithPrec(self):
        formatter = numberFormatter(2)
        assert formatter(3.1415926) == '3.14'
        assert formatter(2.718281828) == '2.72'

    def testRemoveTrailing(self):
        formatter = numberFormatter(removeTrailingZeroes=True)
        assert formatter(0.0) == '0'
        assert formatter(-3) == '-3'

    def testExceptions(self):
        for prec in ('',True,False,1.0,-1.0):
            with pytest.raises(TypeError):
                numberFormatter(prec) # type:ignore
        for prec in (-1,-2):
            with pytest.raises(ValueError):
                numberFormatter(prec)
        for removeZeroes in (1,2,1.0,2.0,'','0'):
            with pytest.raises(TypeError):
                numberFormatter(removeTrailingZeroes=removeZeroes) # type:ignore

class TestSinCos:

    # create several arguments
    # this is just convenience for a tuple of (sin(arg),cos(arg))
    # so we can just use math.sin and math.cos directly in the test
    # this is really just a reimplementation of the functions in a way
    positiveArgs = [ 0.1, 0.2, 0.5, 1, 3, 5, *range(10,361,10) ]
    testArgs = [ 0, *(a for a in positiveArgs), *(-a for a in positiveArgs) ]

    def testRad(self):
        for argDeg in TestSinCos.testArgs:
            argRad = math.radians(argDeg)
            assert sincosRad(argRad) == (math.sin(argRad),math.cos(argRad))

    def testDeg(self):
        for argDeg in TestSinCos.testArgs:
            argRad = math.radians(argDeg)
            assert sincosDeg(argDeg) == (math.sin(argRad),math.cos(argRad))

    def testHypot(self):
        # sin^2(theta) + cos^2(theta) == 1
        # tight tolerance is fine for math.sin and math.cos
        for argDeg in TestSinCos.testArgs:
            s,c = sincosDeg(argDeg)
            hypot = math.hypot(s,c)
            assert math.isclose(hypot,1.0,rel_tol=1e-15,abs_tol=1e-15)

    def testEvenOdd(self):
        # sin is odd and cos is even
        for argDeg in TestSinCos.testArgs:
            sp,cp = sincosDeg(argDeg)
            sm,cm = sincosDeg(-argDeg)
            assert sp == -sm
            assert cp == cm

    def testDoubleAngle(self):
        # double angle formulas
        tols = { 'rel_tol': 1e-15, 'abs_tol': 1e-15 }
        for argDeg in TestSinCos.testArgs:
            s,c = sincosDeg(argDeg)
            s2,c2 = sincosDeg(2.0*argDeg)
            assert math.isclose(s2, 2.0*s*c, **tols)
            assert math.isclose(s2, (s+c)*(s+c)-1.0, **tols)
            assert math.isclose(c2, c*c-s*s, **tols)
            assert math.isclose(c2, 2.0*c*c-1.0, **tols)
            assert math.isclose(c2, 1.0-2.0*s*s, **tols)

    def testTripleAngle(self):
        # triple angle formulas
        tols = { 'rel_tol': 1e-14, 'abs_tol': 1e-14 }
        for argDeg in TestSinCos.testArgs:
            s,c = sincosDeg(argDeg)
            s3,c3 = sincosDeg(3.0*argDeg)
            assert math.isclose(s3, 3.0*s-4.0*s*s*s, **tols)
            assert math.isclose(c3, 4.0*c*c*c-3.0*c, **tols)
