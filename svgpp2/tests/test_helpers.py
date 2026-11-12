
from svgpp2.helpers import formatNumber, numberFormatter, sincosRad, sincosDeg
from svgpp2.helpers import _checkFloat, _checkTol, _checkTolAndScale

import math
import pytest

class TestCheckFloats:

    @pytest.mark.parametrize(('num',),[
        (True,),
        (False,),
        ('',),
        ('0',),
        ('3.6',),
        ('-5.8',)
    ])
    def testTypeError(self, num):
        with pytest.raises(TypeError):
            _checkFloat(num)

    @pytest.mark.parametrize(('num',),[
        (math.inf,),
        (-math.inf,),
        (math.nan,)
    ])
    def testValueError(self, num):
        with pytest.raises(ValueError):
            _checkFloat(num)

    @pytest.mark.parametrize(('num',),[
        (0,),
        (-5,),
        (1.1,),
        (-6.0,)
    ])
    def testValid(self, num):
        assert _checkFloat(num) == num

    # pathological size numbers
    @pytest.mark.parametrize(('num',),[
        (10**400,),
        (-10**500,)
    ])
    def testOverflowError(self, num):
        with pytest.raises(OverflowError):
            _checkFloat(num)

class TestCheckTol:

    @pytest.mark.parametrize(('tol',),[
        ('a',),
        ('False',),
        ('True',),
        (False,),
        (True,),
        ('0.1',),
        ('',)
    ])
    def testTypeError(self, tol):
        with pytest.raises(TypeError):
            _checkTol(tol)

    @pytest.mark.parametrize(('tol',),[
        (-1,),
        (-2.0,),
        (math.inf,),
        (math.nan,),
        (-math.inf,),
        (-42,)
    ])
    def testValueError(self, tol):
        with pytest.raises(ValueError):
            _checkTol(tol)

    @pytest.mark.parametrize(('tol',),[
        (0.0,),
        (1e-300,),
        (1e-30,),
        (1e-15,),
        (1e-9,),
        (1e-6,),
        (1e-3,),
        (1.0,),
        (1e3,),
        (1e6,),
        (-0.0,),
        (0,),
        (1,),
        (1000,)
    ])
    def testValid(self, tol):
        assert _checkTol(tol) == tol

class TestCheckTolAndScale:

    @pytest.mark.parametrize(('tol','scale'),[
        (False,'a'),
        ('b',True),
        (True,True),
        ('0','0'),
        ('','')
    ])
    def testTypeError(self, tol, scale):
        with pytest.raises(TypeError):
            _checkTolAndScale(tol,scale)

    @pytest.mark.parametrize(('tol','scale'),[
        (-0.1,0.1),
        (0.1,-0.1),
        (-1,1),
        (1,-1),
        (math.nan,1e-9),
        (1e-9,-math.inf),
        (math.inf,math.inf)
    ])
    def testValueError(self, tol, scale):
        with pytest.raises(ValueError):
            _checkTolAndScale(tol,scale)

    @pytest.mark.parametrize(('tol','scale'),[
        (0.0,0.0),
        (0,0),
        (1,0.3),
        (1e-9,42),
        (1e-300,1e300),
        (1e-9,1e-9),
        (1e-12,1e-3),
        (0.0,1e-6),
        (1e-12,0),
        (1,0.1)
    ])
    def testValid(self, tol, scale):
        assert _checkTolAndScale(tol,scale) == (tol,scale)

class TestFormatNumber:

    @pytest.mark.parametrize(('num',),[
        ('',),
        (True,),
        (False,),
        ('-5.5',),
        ('0',),
        ('1.0',)
    ])
    def testNumTypeError(self, num):
        with pytest.raises(TypeError):
            formatNumber(num)

    @pytest.mark.parametrize(('num',),[
        (math.inf,),
        (-math.inf,),
        (math.nan,)
    ])
    def testNumValueError(self, num):
        with pytest.raises(ValueError):
            formatNumber(num)

    @pytest.mark.parametrize(('prec',),[
        (True,),
        (False,),
        ('',),
        ('1',),
        (0.1,)
    ])
    def testPrecTypeError(self, prec):
        with pytest.raises(TypeError):
            formatNumber(0.0,prec)

    @pytest.mark.parametrize(('prec',),[
        (-1,),
        (-2,)
    ])
    def testPrecValueError(self, prec):
        with pytest.raises(ValueError):
            formatNumber(0.0,prec)

    @pytest.mark.parametrize(('removeZeroes',),[
        (2,),
        (3,),
        (-1.1,),
        (1.0,),
        ('',),
        ('1',)
    ])
    def testRemoveZeroesTypeError(self, removeZeroes):
        with pytest.raises(TypeError):
            formatNumber(0.0,removeTrailingZeroes=removeZeroes)

    @pytest.mark.parametrize(('num','result'),[
        (0.0,'0.0'),
        (-0.0,'0.0'),
        (3.14,'3.14'),
        (-0.01,'-0.01'),
        (0.00009,'9e-05'),
        (0.0001,'0.0001'),
        (999.999,'999.999'),
        (3.141592653589793,'3.141592653589793'),
        (-0.000001,'-1e-06'),
        (-1e-12,'-1e-12'),
        (9e15,'9000000000000000.0'),
        (1e16,'1e+16'),
        (7,'7.0'),
        (-42,'-42.0')
    ])
    def testDefault(self, num, result):
        # default uses str(num) except -0.0 converts to +0.0
        assert formatNumber(num) == result

    @pytest.mark.parametrize(('num','result'),[
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
    ])
    def testDefaultRemoveTrailing(self, num, result):
        assert formatNumber(num,removeTrailingZeroes=True) == result

    @pytest.mark.parametrize(('num','prec','result'),[
        (5.0,0,'5'),
        (6.1,0,'6'),
        (6.9,0,'7'),
        (0.4,0,'0'),
        (-0.4,0,'0'),
        (1.5,0,'2'),
        (2.5,0,'2'),
        (42,0,'42'),
        (-5.89,1,'-5.9'),
        (-5.99,1,'-6.0'),
        (42.42,1,'42.4'),
        (18,1,'18.0'),
        (1.333,2,'1.33'),
        (1.667,2,'1.67'),
        (-0.003,2,'0.00'),
        (0.007,2,'0.01'),
        (0.0001,2,'0.00'),
        (2.71828,3,'2.718'),
        (-1.05946,3,'-1.059'),
        (1010.7179,3,'1010.718'),
        (-996.1604,3,'-996.160'),
        (0.0001,3,'0.000')
    ])
    def testPrecision(self, num, prec, result):
        assert formatNumber(num,prec) == result

    @pytest.mark.parametrize(('num','prec','result'),[
        (5,1,'5'),
        (89,1,'89'),
        (-62.0,2,'-62'),
        (-62.13,2,'-62.13'),
        (-62.503,2,'-62.5'),
        (123.4,3,'123.4'),
        (123.456,3,'123.456'),
        (123,3,'123')
    ])
    def testPrecisionRemoveTrailing(self, num, prec, result):
        assert formatNumber(num,prec,True) == result

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
