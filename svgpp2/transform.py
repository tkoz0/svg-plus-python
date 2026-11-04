'''
2D transformation objects for convenience and SVG serialization

Design notes:
- all are immutable and convertible to Affine2
'''

from .affine import Affine2
from .helpers import numberFormatter
from .vec import Vec2

from abc import ABC, abstractmethod
import math

__all__ = [
    'TransformBase',
    'TransformTranslate',
    'TransformRotate',
    'TransformScale',
    'TransformSkewX',
    'TransformSkewY',
    'TransformMatrix'
]

# Note: in SVG transform strings, the transformations are applied right to left.
# For example, "scale(5) rotate(10)" does the rotation first then the scale.
# This matches math/matrix order and nesting the transforms in the tree.

class TransformBase(ABC):
    '''
    Base for SVG transformations.
    '''

    # Note: if we add __slots__ here then subclasses need to use it:
    # __slots__ = (*TransformBase.__slots__, myArg1, myArg2, ...)
    __slots__ = ()

    @abstractmethod
    def toSvgString(self, numFmt = numberFormatter()) -> str:
        '''
        Convert the transform to a string representation for SVG usage.
        The default number formatter uses python's round trip float to str.
        Custom formatters can be given as a function of float to str.
        '''
        raise NotImplementedError('subclasses should implement toSvgString()')

    @abstractmethod
    def toAffine2(self) -> Affine2:
        '''
        Convert the transform to an Affine2 object.
        '''
        raise NotImplementedError('subclasses should implement toAffine2()')

    @staticmethod
    @abstractmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformBase':
        '''
        Convert an affine transformation to a transformation object.
        Raise ValueError if the provided affine transformation is not the
        correct type of transformation within the tolerance.

        If coordinates are at very large or very small scales, then scale
        dependent quantities do not work robustly. In these cases, scale
        can be adjusted to give these quantities a reasonable check.
        '''
        raise NotImplementedError('subclasses should implement fromAffine2()')

    def isIdentity(self, tol = 1e-9, scale = 1.0) -> bool:
        '''
        True if the transformation is (within a tolerance) the identity transform.

        If coordinates are at very large or very small scales, then scale
        dependent quantities do not work robustly. In these cases, scale
        can be adjusted to give these quantities a reasonable check.
        '''
        affine = self.toAffine2()
        return (Vec2.areNearlyEqual(affine.origin,Vec2(0,0),0.0,tol*scale)
            and Vec2.areNearlyEqual(affine.xAxis,Vec2(1,0),0.0,tol)
            and Vec2.areNearlyEqual(affine.yAxis,Vec2(0,1),0.0,tol))

    def __setattr__(self,name,value):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __delattr__(self,name):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __bool__(self):
        raise TypeError(f'{type(self).__name__} is not convertible to bool, '
            f'consider using isIdentity()')

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
    __slots__ = ('offset',)

    def __init__(self, ox = None, oy = None):
        '''
        Initialize a translation. The arguments are passed to Vec2 so it is
        compatible with floats, Vec2, or tuple/list pairs.
        '''
        object.__setattr__(self,'offset',Vec2(ox,oy))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        ox,oy = self.offset
        return f'translate({numFmt(ox)} {numFmt(oy)})'

    def toAffine2(self) -> Affine2:
        return Affine2.translate(self.offset)

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformTranslate':
        affine = Affine2(affine)
        if (not Vec2.areNearlyEqual(affine.xAxis,Vec2(1,0),0.0,tol)
            or not Vec2.areNearlyEqual(affine.yAxis,Vec2(0,1),0.0,tol)):
            raise ValueError(f'Not a translation (linear part is not identity): {affine!r}')
        return TransformTranslate(affine.origin)

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
        '''
        Initialize a rotation. The angle is in degrees.
        If a center is provided, it is included with the serialization,
        otherwise only the rotation angle is included.
        '''
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

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformRotate':
        '''
        If the rotation angle is near zero and the origin is nonzero, the center
        cannot be uniquely determimned and this raises ValueError.
        '''
        affine = Affine2(affine)
        # if R is the rotation matrix and c is the center, then applied to x:
        # x' = Rx - Rc + c, so we have the rotation matrix and need c next
        if not math.isclose(affine.xAxis.magnitudeSquared(),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (x axis is not unit length): {affine!r}')
        if not math.isclose(affine.yAxis.magnitudeSquared(),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (y axis is not unit length): {affine!r}')
        if not Vec2.areOrthogonal(affine.xAxis,affine.yAxis,tol):
            raise ValueError(f'Not a rotation (axes are not orthogonal): {affine!r}')
        # compute determinant from cross product
        if not math.isclose(Vec2.cross(affine.xAxis,affine.yAxis),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (includes a reflection, det = -1): {affine!r}')
        # xAxis is (cos(theta),sin(theta)) so we can use its plane angle
        angleDeg = affine.xAxis.angleDeg()
        # origin 0 means it is purely a rotation
        if Vec2.areNearlyEqual(affine.origin,Vec2(),0.0,tol*scale):
            return TransformRotate(angleDeg)
        # now we need the matrix inverse to solve (-Rc+Ic)=(-R+I)c=o
        # (where R is the matrix part, I is identity, c is center, o is affine.origin)
        # the matrix I-R is
        # [ 1-cos(theta)    sin(theta) ]
        # [  -sin(theta)  1-cos(theta) ]
        px,py = affine.xAxis # cos(theta) and sin(theta)
        a,b = 1.0-px, py
        c,d = -py, 1.0-px
        det = Vec2.cross(Vec2(a,b),Vec2(c,d))
        if abs(det) < tol*tol: # near 0, det = 2(1-cos(theta)) ~= theta^2
            raise ValueError(f'Not a rotation (angle too close to 0 to find center): {affine!r}')
        aI,bI = d/det, -b/det
        cI,dI = -c/det, a/det
        # use inverse to find center point
        ox,oy = affine.origin
        cx = aI*ox + bI*oy
        cy = cI*ox + dI*oy
        return TransformRotate(angleDeg,cx,cy)

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
        '''
        Initialize a scaling. If one arg is provided, the scale is applied
        equally in both axes. If both are provided, axis scales may differ.
        '''
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

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformScale':
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),0.0,tol*scale):
            raise ValueError(f'Not a scale (origin is nonzero): {affine!r}')
        # make sure vectors are axis aligned, negative allowed, zero allowed
        if affine.xAxis.isZero():
            sx = 0.0 # zero x scale
        else:
            # nonzero x scale
            xDir = affine.xAxis.normalize()
            if Vec2.areNearlyEqual(xDir,Vec2(1.0,0.0),0.0,tol):
                sx = affine.xAxis.magnitude()
            elif Vec2.areNearlyEqual(xDir,Vec2(-1.0,0.0),0.0,tol):
                sx = -affine.xAxis.magnitude()
            else:
                raise ValueError(f'Not a scale (x vector is not axis aligned): {affine!r}')
        if affine.yAxis.isZero():
            sy = 0.0 # zero y scale
        else:
            # nonzero y scale
            yDir = affine.yAxis.normalize()
            if Vec2.areNearlyEqual(yDir,Vec2(0.0,1.0),0.0,tol):
                sy = affine.yAxis.magnitude()
            elif Vec2.areNearlyEqual(yDir,Vec2(0.0,-1.0),0.0,tol):
                sy = -affine.yAxis.magnitude()
            else:
                raise ValueError(f'Not a scale (y vector is not axis aligned): {affine!r}')
        if math.isclose(sx,sy,rel_tol=tol,abs_tol=0.0):
            return TransformScale(0.5*(sx+sy))
        else:
            return TransformScale(sx,sy)

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
    __slots__ = ('angleDeg',)

    def __init__(self, angleDeg = 0.0):
        '''
        Initialize an X skew. The angle is in degrees.
        '''
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        return f'skewX({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        return Affine2(yAxis=Vec2(math.tan(math.radians(self.angleDeg)),1.0))

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformSkewX':
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),0.0,tol*scale):
            raise ValueError(f'Not a skewX (origin is nonzero): {affine!r}')
        if not Vec2.areNearlyEqual(affine.xAxis,Vec2(1.0,0.0),0.0,tol):
            raise ValueError(f'Not a skewX (xAxis is not (1,0)): {affine!r}')
        if not math.isclose(affine.yAxis.y,1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a skewX (yAxis.y is not 1): {affine!r}')
        angleRad = math.atan(affine.yAxis.x)
        return TransformSkewX(math.degrees(angleRad))

    def __repr__(self) -> str:
        return f'TransformSkewX({self.angleDeg!r})'

class TransformSkewY(TransformBase):
    '''
    Y axis skew transformation, for SVG.
    The angle is in degrees.
    '''
    angleDeg: float
    __slots__ = ('angleDeg',)

    def __init__(self, angleDeg = 0.0):
        '''
        Initialize a Y skew. The angle is in degrees.
        '''
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        return f'skewY({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        return Affine2(xAxis=Vec2(1.0,math.tan(math.radians(self.angleDeg))))

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformSkewY':
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),0.0,tol*scale):
            raise ValueError(f'Not a skewY (origin is nonzero): {affine!r}')
        if not Vec2.areNearlyEqual(affine.yAxis,Vec2(0.0,1.0),0.0,tol):
            raise ValueError(f'Not a skewY (yAxis is not (0,1)): {affine!r}')
        if not math.isclose(affine.xAxis.x,1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a skewY (xAxis.x is not 1): {affine!r}')
        angleRad = math.atan(affine.xAxis.y)
        return TransformSkewY(math.degrees(angleRad))

    def __repr__(self) -> str:
        return f'TransformSkewY({self.angleDeg!r})'

class TransformMatrix(TransformBase):
    '''
    General affine transformation, for SVG.
    '''
    affine: Affine2
    __slots__ = ('affine',)

    def __init__(self, affine):
        '''
        Initialize a matrix transformation from an affine transformation.
        '''
        object.__setattr__(self,'affine',Affine2(affine))

    @staticmethod
    def fromVectors(xAxis,yAxis,origin) -> 'TransformMatrix':
        '''
        Construct a TransformMatrix with the 3 vectors as in the Affine2 constructor.
        '''
        return TransformMatrix(Affine2(xAxis,yAxis,origin))

    @staticmethod
    def fromParams(a,b,c,d,e,f) -> 'TransformMatrix':
        '''
        Construct a TransformMatrix using the 6 parameters in the SVG order.
        '''
        return TransformMatrix(Affine2(Vec2(a,b),Vec2(c,d),Vec2(e,f)))

    def toSvgString(self, numFmt = numberFormatter()) -> str:
        a,b = self.affine.xAxis
        c,d = self.affine.yAxis
        e,f = self.affine.origin
        return (f'matrix({numFmt(a)} {numFmt(b)} {numFmt(c)} {numFmt(d)} {numFmt(e)} {numFmt(f)})')

    def toAffine2(self) -> Affine2:
        return self.affine

    @staticmethod
    def fromAffine2(affine, tol = 1e-9, scale = 1.0) -> 'TransformMatrix':
        '''
        Since TransformMatrix can handle any affine transformation, this does
        not raise an exception unlike the other transformations.
        '''
        return TransformMatrix(affine)

    def __repr__(self) -> str:
        return f'TransformMatrix({self.affine!r})'
