'''
Affine transformations for basic math calculations

Design notes:
- immutable to be reusable, avoid unexpected changes, and be hashable
- strictly avoids inf/nan and robust for huge/tiny scales
'''

from .helpers import sincosRad
from .vec import Vec2,Vec2LikeType

import math
from typing import Union

__all__ = [
    'Affine2',
    'Affine2LikeType'
]

# Affine2 and related types that express its quantities.
Affine2LikeType = Union['Affine2',tuple,list]

def _checkTol(tol: float, /) -> float:
    '''
    Return the tolerance converted to float.
    Raises TypeError if not convertible to float.
    Raises ValueError if it is inf/nan or negative.
    '''
    tol = float(tol)
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError(f'tolerance must be finite and >= 0, tol = {tol!r}')
    return tol

class Affine2:
    '''
    An immutable 2D affine transformation.

    Transformation equation for p (a 2D point):
        p' = p.x*xAxis + p.y*yAxis + origin
    Note: xAxis and yAxis are the columns of a 2x2 matrix.
    The xAxis and yAxis define a basis for the transformation and a given point
    is transformed by converting its coordinates into this new basis.

    May be constructed from 3 Vec2 objects or a tuple/list of 6 floats.
    '''
    xAxis: Vec2
    yAxis: Vec2
    origin: Vec2
    __slots__ = ('xAxis','yAxis','origin')

    def __init__(self,
        xAxis: Vec2LikeType|Affine2LikeType|None = None,
        yAxis: Vec2LikeType|None = None,
        origin: Vec2LikeType|None = None
    ):
        '''
        Construction supported from 3 Vec2 or tuple/list of length 2.
        Alternatively, the first arg (xAxis) may be another Affine2 or a
        tuple/list of 6 floats. If given a tuple/list (a,b,c,d,e,f) then it
        constructs with xAxis=Vec2(a,b), yAxis=Vec2(c,d), origin=Vec2(e,f).
        The xAxis and yAxis define the scaling/rotation/skew (linear basis)
        and origin is the center, where the (0,0) point gets mapped to.

        The 3 vectors represent the transformation:
            p' = p.x*xAxis + p.y*yAxis + origin
        The 6 element tuple/list (a,b,c,d,e,f) represents the transformation:
            x' = a*x + c*y + e
            y' = b*x + d*y + f

        The defaults are for the identity transformation.
        Shared defaults are fine since Vec2 is immutable.
        '''
        if isinstance(xAxis,Affine2):
            if yAxis is not None or origin is not None:
                raise ValueError('Affine2 init from Affine2 takes 1 argument')
            affine = xAxis
            valueXAxis = affine.xAxis
            valueYAxis = affine.yAxis
            valueOrigin = affine.origin
        elif isinstance(xAxis,(tuple,list)) and len(xAxis) == 6:
            # xAxis might be a tuple/list for Affine2 (length 6)
            # If the length is not 6, fall back to construction from 3 Vec2
            if yAxis is not None or origin is not None:
                raise ValueError('Affine2 init from length 6 tuple/list takes 1 argument')
            a,b,c,d,e,f = xAxis
            valueXAxis = Vec2(a,b)
            valueYAxis = Vec2(c,d)
            valueOrigin = Vec2(e,f)
        else: # construct from 3 Vec2, make sure defaults are handled
            valueXAxis = Vec2(1.0,0.0) if xAxis is None else Vec2(xAxis)
            valueYAxis = Vec2(0.0,1.0) if yAxis is None else Vec2(yAxis)
            valueOrigin = Vec2(origin) # None gives us (0,0) which is desired
        # bypass the __setattr__ exception for construction
        # Affine2.__setattr__ throws to enforce immutability
        object.__setattr__(self,'xAxis',valueXAxis)
        object.__setattr__(self,'yAxis',valueYAxis)
        object.__setattr__(self,'origin',valueOrigin)

    def __setattr__(self, name, value):
        raise AttributeError('Affine2 is immutable')

    def __delattr__(self, name):
        raise AttributeError('Affine2 is immutable')

    def __repr__(self) -> str:
        return f'Affine2(xAxis={self.xAxis!r},yAxis={self.yAxis!r},origin={self.origin!r})'

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other):
        '''
        True if both objects are Affine2 and exactly equal.
        '''
        if not isinstance(other,Affine2):
            return NotImplemented
        return self.origin == other.origin \
            and self.xAxis == other.xAxis \
            and self.yAxis == other.yAxis

    def __ne__(self, other):
        '''
        True if both objects are not exactly equal Affine2.
        '''
        eqResult = self == other
        return eqResult if eqResult is NotImplemented else not eqResult

    def asTuple(self) -> tuple[float,float,float,float,float,float]:
        '''
        Convert to a 6 element tuple. (a,b,c,d,e,f) describes the transformation
            x' = a*x + c*y + e
            y' = b*x + d*y + f
        '''
        return self.xAxis.asTuple() + self.yAxis.asTuple() + self.origin.asTuple()

    def asList(self) -> list[float]:
        '''
        Convert to a 6 element list. [a,b,c,d,e,f] describes the transformation
            x' = a*x + c*y + e
            y' = b*x + d*y + f
        '''
        return self.xAxis.asList() + self.yAxis.asList() + self.origin.asList()

    def __hash__(self) -> int:
        return hash((self.origin,self.xAxis,self.yAxis))

    def __bool__(self):
        '''
        Affine2 is not convertible to bool. This raises TypeError.
        '''
        raise TypeError('Affine2 is not convertible to bool')

    def isIdentity(self) -> bool:
        '''
        True if this affine is exactly the identity transformation.
        '''
        return (self.xAxis == Vec2(1.0,0.0)
            and self.yAxis == Vec2(0.0,1.0)
            and self.origin == Vec2(0.0,0.0))

    def __reduce__(self):
        '''
        How to reconstruct object, usually for pickle.
        '''
        return (Affine2,(self.xAxis,self.yAxis,self.origin))

    def __copy__(self) -> Affine2:
        '''
        Shallow copy (self because immutable).
        '''
        return self

    def __deepcopy__(self, memo) -> Affine2:
        '''
        Deep copy (self because immutable).
        '''
        return self

    def copy(self) -> 'Affine2':
        '''
        Return self (since Affine2 is immutable).
        '''
        return self

    def apply(self, x: float|Vec2LikeType|None, y: float|None = None) -> Vec2:
        '''
        Apply this transformation to a given point.
        The arguments are converted to Vec2.
        '''
        p = Vec2(x,y)
        return p.x*self.xAxis + p.y*self.yAxis + self.origin

    def __call__(self, x: float|Vec2LikeType|None, y: float|None = None) -> Vec2:
        '''
        Convenience operator for apply().
        '''
        return self.apply(x,y)

    def determinant(self) -> float:
        '''
        Determinant of the linear component.
        '''
        # cross product of columns works for 2x2 matrix
        # note: possible this will throw in pathological cases
        return Vec2.cross(self.xAxis,self.yAxis)

    def isSingular(self, *, tol: float = 1e-9) -> bool:
        '''
        True if the linear part is singular within a tolerance.
        The tolerance is applied to the directions of the xAxis and yAxis.
        '''
        tol = _checkTol(tol)
        # note: possible that magnitude will throw in pathological cases
        mx = self.xAxis.magnitude()
        my = self.yAxis.magnitude()
        if mx == 0.0 or my == 0.0:
            return True
        # normalize to avoid overflow, check cross (equal to determinant)
        # note: possible that cross will throw in pathological cases
        xAxis = self.xAxis / mx
        yAxis = self.yAxis / my
        return abs(Vec2.cross(xAxis,yAxis)) <= tol

    def inverse(self, *, tol: float = 1e-9) -> Affine2:
        '''
        Return the inverse transformation.

        Raises ValueError if the linear part is singular (checked with isSingular(tol)).
        '''
        if self.isSingular(tol=tol):
            raise ValueError('cannot invert a singular Affine2')
        # rearrange x'=Ax+b into x=A'x'-A'b where A' is the inverse of A
        # the new linear part is A' and the new origin is -A'b
        # split up the linear part into
        # [ a b ]
        # [ c d ]
        # (xAxis and yAxis are column vectors)
        # note: possible determinant will throw in pathological cases
        det = self.determinant()
        a,c = self.xAxis
        b,d = self.yAxis
        # compute the inverse
        aI,bI = d/det, -b/det
        cI,dI = -c/det, a/det
        # then the new origin
        ox,oy = self.origin
        oxI = -(aI*ox + bI*oy)
        oyI = -(cI*ox + dI*oy)
        return Affine2(
            Vec2(aI,cI),
            Vec2(bI,dI),
            Vec2(oxI,oyI)
        )

    def isUniform(self, *, tol: float = 1e-9) -> bool:
        '''
        True if the transformation is a translation and uniform scale, no skew.
        This allows transformations that reflect the x/y orientation.
        Returns False for singular and zero scale transformations.
        Checks if transformation is singular with isSingular(tol).
        '''
        tol = _checkTol(tol)
        # note: possible that magnitude will throw in pathological cases
        mx = self.xAxis.magnitude()
        my = self.yAxis.magnitude()
        if mx == 0.0 or my == 0.0:
            return False
        # check that the scaling magnitude is the same in both axes
        if abs(mx-my) > tol*max(mx,my):
            return False
        # check that the axes are orthogonal
        # normalize axis directions to be robust against scaling
        xAxis = self.xAxis / mx
        yAxis = self.yAxis / my
        return abs(xAxis@yAxis) <= tol

    def compose(self, other: Affine2LikeType) -> Affine2:
        '''
        Compose 2 affine transformations. This is in math/matrix order, so
        other is applied before self when used to transform a point.
        Mathematically: self.compose(other)(p) == self(other(p))
        '''
        if isinstance(other,Vec2):
            raise TypeError('cannot compose Affine2 with Vec2, use another Affine2 '
                'or tuple/vector with 6 elements')
        if isinstance(other,(tuple,list)) and len(other) != 6:
            raise ValueError(f'tuple/list length must be 6, not {len(other)}')
        other = Affine2(other)
        # composition requires a little messy algebra
        # if other=Ax+b and self=A'x+b' then the composition is
        # A'(Ax+b)+b' = A'Ax + A'b + b'
        # the new origin is self.apply(other.origin)
        # the new linear component requires matrix multiplication
        return Affine2(
            other.xAxis.x*self.xAxis + other.xAxis.y*self.yAxis,
            other.yAxis.x*self.xAxis + other.yAxis.y*self.yAxis,
            self.apply(other.origin)
        )

    @staticmethod
    def identity() -> Affine2:
        '''
        Identity affine transformation.
        '''
        return Affine2()

    @staticmethod
    def fromBasis(xAxis: Vec2LikeType, yAxis: Vec2LikeType, origin: Vec2LikeType) -> Affine2:
        '''
        Affine transformation from vectors. Same as constructor parameters.
        '''
        return Affine2(xAxis,yAxis,origin)

    @staticmethod
    def translate(tx: float|Vec2LikeType|None, ty: float|None = None) -> Affine2:
        '''
        Translation affine transformation. No scale/skew.
        Arguments are constructed into a Vec2.
        '''
        return Affine2(origin=Vec2(tx,ty))

    @staticmethod
    def scale(sx: float, sy: float|None = None) -> Affine2:
        '''
        Scale axes affine transformation. No translation/skew.
        If given one number, scales both axes equally.
        '''
        if sy is None: # try single float parameter to scale both axes equally
            sx = float(sx)
            return Affine2(Vec2(sx,0.0),Vec2(0.0,sx))
        else:
            return Affine2(Vec2(float(sx),0.0),Vec2(0.0,float(sy)))

    @staticmethod
    def rotateRad(angleRad: float) -> Affine2:
        '''
        Rotation affine transformation (radians).
        For y-up and positive angle, this is counterclockwise.
        For y-down and positive angle, this is clockwise.
        '''
        angleRad = float(angleRad)
        s,c = sincosRad(angleRad)
        return Affine2(Vec2(c,s),Vec2(-s,c))

    @staticmethod
    def rotateDeg(angleDeg: float) -> Affine2:
        '''
        Rotation affine transformation (degrees).
        For y-up and positive angle, this is counterclockwise.
        For y-down and positive angle, this is clockwise.
        '''
        return Affine2.rotateRad(math.radians(angleDeg))

    @staticmethod
    def skewXRad(angleRad: float) -> Affine2:
        '''
        Skew along X axis affine transformation (radians).
        '''
        return Affine2(yAxis=Vec2(math.tan(angleRad),1.0))

    @staticmethod
    def skewXDeg(angleDeg: float) -> Affine2:
        '''
        Skew along X axis affine transformation (degrees).
        '''
        return Affine2.skewXRad(math.radians(angleDeg))

    @staticmethod
    def skewYRad(angleRad: float) -> Affine2:
        '''
        Skew along Y axis affine transformation (radians).
        '''
        return Affine2(xAxis=Vec2(1.0,math.tan(angleRad)))

    @staticmethod
    def skewYDeg(angleDeg: float) -> Affine2:
        '''
        Skew along Y axis affine transformation (degrees).
        '''
        return Affine2.skewYRad(math.radians(angleDeg))
