'''
Affine transformations

Design notes:
- immutable to be reusable, avoid unexpected changes, and be hashable
'''

import math
from .vec import Vec2

__all__ = [
    'Affine2',
]

class Affine2:
    '''
    An immutable 2D affine transformation.
    Transformation equation for p (a 2D point):
        p' = p.x*xAxis + p.y*yAxis + origin
    Note: xAxis and yAxis are the columns of a 2x2 matrix.
    The xAxis and yAxis define a basis for the transformation and a given point
    is transformed by converting its coordinates into this new basis.
    '''
    xAxis: Vec2
    yAxis: Vec2
    origin: Vec2
    __slots__ = ('xAxis','yAxis','origin')

    def __init__(self,
        xAxis = Vec2(1,0),
        yAxis = Vec2(0,1),
        origin = Vec2(0,0)
    ):
        xAxis = Vec2(xAxis)
        yAxis = Vec2(yAxis)
        origin = Vec2(origin)
        # need to do this to avoid the immutability exception
        object.__setattr__(self,'xAxis',xAxis)
        object.__setattr__(self,'yAxis',yAxis)
        object.__setattr__(self,'origin',origin)

    def __setattr__(self,name,value):
        raise AttributeError('Affine2 is immutable')

    def __delattr__(self,name):
        raise AttributeError('Affine2 is immutable')

    def __repr__(self) -> str:
        return f'Affine2(origin={self.origin!r},xAxis={self.xAxis!r},yAxis={self.yAxis!r})'

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self,other):
        if not isinstance(other,Affine2):
            return NotImplemented
        return self.origin == other.origin \
            and self.xAxis == other.xAxis \
            and self.yAxis == other.yAxis

    def __hash__(self) -> int:
        return hash((self.origin,self.xAxis,self.yAxis))

    def copy(self) -> 'Affine2':
        '''
        Return a new object as a copy.
        '''
        return Affine2(self.xAxis,self.yAxis,self.origin)

    def apply(self, x, y = None) -> Vec2:
        '''
        Apply this transformation to a given point.
        The arguments are converted to Vec2.
        '''
        p = Vec2(x,y)
        return p.x*self.xAxis + p.y*self.yAxis + self.origin

    def determinant(self) -> float:
        '''
        Determinant of the linear component.
        '''
        return Vec2.cross(self.xAxis,self.yAxis)

    def isSingular(self,tol=1e-9) -> bool:
        '''
        Uses a tolerance to determine if the linear component is singular.
        '''
        # |det| / scale == |sin(theta)|, angle between axes
        scale = self.xAxis.magnitude() * self.yAxis.magnitude()
        return True if scale == 0.0 else abs(self.determinant()) / scale <= tol

    def inverse(self,tol=1e-9) -> 'Affine2':
        '''
        Return the inverse transformation.
        Throws if the linear part is singular.
        '''
        if self.isSingular(tol):
            raise ValueError('cannot invert a singular Affine2')
        # rearrange x'=Ax+b into x=A'x'-A'b where A' is the inverse of A
        # the new linear part is A' and the new origin is -A'b
        # split up the linear part into
        # [ a b ]
        # [ c d ]
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

    def isUniform(self,tol=1e-9) -> bool:
        '''
        True if the transformation is a translation and uniform scale, no skew.
        This allows transformations that reflect the x/y orientation.
        '''
        mx = self.xAxis.magnitude()
        my = self.yAxis.magnitude()
        if mx == 0.0 or my == 0.0:
            return False
        # check that the scaling magnitude is the same in both axes
        # compare ratio to 1.0 to be robust against scaling
        if abs(mx/my - 1.0) > tol:
            return False
        # check that the axes are perpendicular
        # normalize axis directions to be robust against scaling
        xAxisDir = self.xAxis.normalize()
        yAxisDir = self.yAxis.normalize()
        return abs(xAxisDir @ yAxisDir) <= tol

    def compose(self,other) -> 'Affine2':
        '''
        Compose 2 transformations. This is in math order, so other is applied
        before self.
        '''
        if not isinstance(other,Affine2):
            raise ValueError('can only compose Affine2 with another Affine2')
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
    def identity() -> 'Affine2':
        '''
        Identity affine transformation.
        '''
        return Affine2()

    @staticmethod
    def fromBasis(xAxis:Vec2, yAxis:Vec2, origin:Vec2) -> 'Affine2':
        '''
        Affine transformation from vectors. Same as constructor parameters.
        '''
        return Affine2(xAxis,yAxis,origin)

    @staticmethod
    def translate(tx, ty = None) -> 'Affine2':
        '''
        Translation affine transformation. No scale/skew.
        Arguments are constructed into a Vec2.
        '''
        origin = Vec2(tx,ty)
        return Affine2(origin=origin)

    @staticmethod
    def scale(sx, sy = None) -> 'Affine2':
        '''
        Scale axes affine transformation. No translation/skew.
        If given one number, scales both axes equally.
        Otherwise a Vec2 is constructed from the args for axis scales.
        '''
        if sy is None: # try single float parameter to scale both axes equally
            try:
                s = float(sx)
                return Affine2(Vec2(s,0.0),Vec2(0.0,s))
            except (TypeError,ValueError):
                pass
        scales = Vec2(sx,sy)
        return Affine2(Vec2(scales.x,0.0),Vec2(0.0,scales.y))

    @staticmethod
    def rotateRad(theta) -> 'Affine2':
        '''
        Rotation affine transformation (radians).
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        theta = float(theta)
        c = math.cos(theta)
        s = math.sin(theta)
        return Affine2(Vec2(c,s),Vec2(-s,c))

    @staticmethod
    def rotateDeg(theta) -> 'Affine2':
        '''
        Rotation affine transformation (degrees).
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        return Affine2.rotateRad(math.radians(theta))
