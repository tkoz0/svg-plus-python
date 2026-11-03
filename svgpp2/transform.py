'''
2D transformation objects for convenience and SVG serialization

Design notes:
- all are immutable and convertible to Affine2
'''

from .affine import Affine2
from .helpers import numberFormatter
from .vec import Vec2

import math

__all__ = [
    'TransformBase',
    'TransformTranslate',
    'TransformRotate',
    'TransformScale',
    'TransformSkewX',
    'TransformSkewY',
    'TransformAffine'
]

# Note: in SVG transform strings, the transformations are applied right to left.
# For example, "scale(5) rotate(10)" does the rotation first then the scale.
# This matches math/matrix order and nesting the transforms in the tree.

class TransformBase:
    '''
    Base for SVG transformations.
    '''

    # Note: if we add __slots__ here then subclasses need to use it:
    # __slots__ = (*TransformBase.__slots__, myArg1, myArg2, ...)
    __slots__ = ()

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        '''
        Convert the transform to a string representation for SVG usage.
        The default number formatter uses python's round trip float to str.
        Custom formatters can be given as a function of float to str.
        '''
        raise NotImplementedError('subclasses should implement toSvgString()')

    def toAffine2(self) -> Affine2:
        '''
        Convert the transform to an Affine2 object.
        '''
        raise NotImplementedError('subclasses should implement toAffine2()')

    def isIdentity(self, tol=1e-9) -> bool:
        '''
        True if the transformation is (within a tolerance) the identity transform.
        '''
        affine = self.toAffine2()
        return (Vec2.areNearlyEqual(affine.origin,Vec2(0,0),0.0,tol)
            and Vec2.areNearlyEqual(affine.xAxis,Vec2(1,0),tol)
            and Vec2.areNearlyEqual(affine.yAxis,Vec2(0,1),tol))

    def __setattr__(self,name,value):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __delattr__(self,name):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __bool__(self):
        raise TypeError(f'{type(self).__name__} is not convertible to bool, '
            f'consider using isIdentity()')

    def __repr__(self) -> str:
        raise NotImplementedError('subclasses should implement __repr__()')

    def __eq__(self,other):
        if isinstance(other,TransformBase):
            return self.toAffine2() == other.toAffine2()
        return NotImplemented

    def __ne__(self,other):
        eqResult = self == other
        return eqResult if eqResult is NotImplemented else not eqResult

    def __hash__(self) -> int:
        return hash(self.toAffine2())

class TransformTranslate(TransformBase):
    '''
    Translation transformation, for SVG.
    Constructor args are passed to Vec2.
    '''
    offset: Vec2
    __slots__ = ('offset')

    def __init__(self, ox = None, oy = None):
        object.__setattr__(self,'offset',Vec2(ox,oy))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        ox,oy = self.offset
        return f'translate({numFmt(ox)} {numFmt(oy)})'

    def toAffine2(self) -> Affine2:
        return Affine2.translate(self.offset)

    def __repr__(self) -> str:
        return f'TransformTranslate({self.offset!r})'

class TransformRotate(TransformBase):
    '''
    Rotation transformation, optionally around a center point, for SVG.
    The angle is in degrees. The center point is passed to Vec2.
    '''
    angleDeg: float
    center: None|Vec2
    __slots__ = ('angleDeg','center')

    def __init__(self, angleDeg = 0.0, cx = None, cy = None):
        object.__setattr__(self,'angleDeg',float(angleDeg))
        if cx is None and cy is None:
            object.__setattr__(self,'center',None)
        else:
            object.__setattr__(self,'center',Vec2(cx,cy))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        if self.center is None:
            return f'rotate({numFmt(self.angleDeg)})'
        else:
            cx,cy = self.center
            return f'rotate({numFmt(self.angleDeg)} {numFmt(cx)} {numFmt(cy)})'

    def toAffine2(self) -> Affine2:
        if self.center is None:
            return Affine2.rotateDeg(self.angleDeg)
        else:
            return (Affine2.translate(self.center)
                .compose(Affine2.rotateDeg(self.angleDeg))
                .compose(Affine2.translate(-self.center)))

    def __repr__(self) -> str:
        if self.center is None:
            return f'TransformRotate({self.angleDeg!r})'
        else:
            return f'TransformRotate({self.angleDeg!r},{self.center!r})'

class TransformScale(TransformBase):
    '''
    Scale transformation, for SVG.
    Use 1 arg for uniform scale and 2 for non uniform.
    '''
    sx: float
    sy: float|None
    __slots__ = ('sx','sy')

    def __init__(self, sx = 1.0, sy = None):
        if sy is None:
            object.__setattr__(self,'sx',float(sx))
            object.__setattr__(self,'sy',None)
        else:
            object.__setattr__(self,'sx',float(sx))
            object.__setattr__(self,'sy',float(sy))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        if self.sy is None:
            return f'scale({numFmt(self.sx)})'
        else:
            return f'scale({numFmt(self.sx)} {numFmt(self.sy)})'

    def toAffine2(self) -> Affine2:
        return Affine2.scale(self.sx,self.sy)

    def __repr__(self) -> str:
        if self.sy is None:
            return f'TransformScale({self.sx!r})'
        else:
            return f'TransformScale({self.sx!r},{self.sy!r})'

class TransformSkewX(TransformBase):
    '''
    X axis skew transformation, for SVG.
    The angle is in degrees.
    '''
    angleDeg: float
    __slots__ = ('angleDeg')

    def __init__(self, angleDeg = 0.0):
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        return f'skewX({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        return Affine2(yAxis=Vec2(math.tan(math.radians(self.angleDeg)),1.0))

    def __repr__(self) -> str:
        return f'TransformSkewX({self.angleDeg!r})'

class TransformSkewY(TransformBase):
    '''
    Y axis skew transformation, for SVG.
    The angle is in degrees.
    '''
    angleDeg: float
    __slots__ = ('angleDeg')

    def __init__(self, angleDeg = 0.0):
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        return f'skewY({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        return Affine2(xAxis=Vec2(1.0,math.tan(math.radians(self.angleDeg))))

    def __repr__(self) -> str:
        return f'TransformSkewY({self.angleDeg!r})'

class TransformAffine(TransformBase):
    '''
    General affine transformation, for SVG.
    '''
    affine: Affine2
    __slots__ = ('affine')

    def __init__(self, affine):
        object.__setattr__(self,'affine',Affine2(affine))

    @staticmethod
    def fromVectors(xAxis,yAxis,origin) -> 'TransformAffine':
        '''
        Construct a TransformAffine with the 3 vectors as in the Affine2 constructor.
        '''
        return TransformAffine(Affine2(xAxis,yAxis,origin))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        a,c = self.affine.xAxis
        b,d = self.affine.yAxis
        e,f = self.affine.origin
        return (f'matrix({numFmt(a)} {numFmt(b)} {numFmt(c)} {numFmt(d)} {numFmt(e)} {numFmt(f)})')

    def toAffine2(self) -> Affine2:
        return self.affine

    def __repr__(self) -> str:
        return f'TransformAffine({self.affine!r})'
