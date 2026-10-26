'''
Vector types

Design notes:
- immutable to be reusable, avoid unexpected changes, and be hashable
'''

import math
from typing import Iterator

__all__ = [
    'Vec2',
]

class Vec2:
    '''
    An immutable 2D vector.
    Used for coordinates in math diagrams and SVG canvases.

    Construction
    - Supports Vec2 or length 2 tuple/list as a single argument
    - Otherwise converts args to float, or 0.0 if None
    '''
    x: float
    y: float
    __slots__ = ('x','y')

    def __init__(self, x = None, y = None):
        if isinstance(x,Vec2):
            if y is not None:
                raise ValueError('Vec2 init from Vec2 only takes one argument')
            valueX = x.x
            valueY = x.y
        elif isinstance(x,(tuple,list)):
            if y is not None:
                raise ValueError('Vec2 init from tuple/list only takes one argument')
            if len(x) != 2:
                raise ValueError('Vec2 init from tuple/list requires length 2')
            valueX = float(x[0])
            valueY = float(x[1])
        else:
            # use unspecified (None) as 0.0, convert to float otherwise
            valueX = 0.0 if x is None else float(x)
            valueY = 0.0 if y is None else float(y)
        # need to do this to avoid the immutability exception
        object.__setattr__(self,'x',valueX)
        object.__setattr__(self,'y',valueY)

    @staticmethod
    def fromPolarRad(r,theta) -> 'Vec2':
        '''
        Construct from polar coordinates with theta in radians.
        '''
        r = float(r)
        theta = float(theta)
        return Vec2(r*math.cos(theta), r*math.sin(theta))

    @staticmethod
    def fromPolarDeg(r,theta) -> 'Vec2':
        '''
        Construct from polar coordinates with theta in degrees.
        '''
        return Vec2.fromPolarRad(r,math.radians(theta))

    def __setattr__(self,name,value):
        raise AttributeError('Vec2 is immutable')

    def __delattr__(self,name):
        raise AttributeError('Vec2 is immutable')

    def __repr__(self) -> str:
        return f'Vec2({self.x},{self.y})'

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    def __eq__(self,other):
        if isinstance(other,Vec2):
            return self.x == other.x and self.y == other.y
        if isinstance(other,(tuple,list)) and len(other) == 2:
            try:
                return self.x == float(other[0]) and self.y == float(other[1])
            except (TypeError,ValueError):
                pass
        return NotImplemented

    def __ne__(self,other):
        eqResult = self == other
        return eqResult if eqResult is NotImplemented else not eqResult

    def asTuple(self) -> tuple[float,float]:
        '''
        Convert to a 2 element tuple.
        '''
        return (self.x,self.y)

    def asList(self) -> list[float]:
        '''
        Convert to a 2 element list.
        '''
        return [self.x,self.y]

    def __hash__(self) -> int:
        return hash(self.asTuple())

    def __bool__(self) -> bool:
        return self.x != 0.0 or self.y != 0.0

    def __iter__(self) -> Iterator[float]:
        return iter(self.asTuple())

    def __len__(self) -> int:
        return 2

    def __getitem__(self,index):
        return self.asTuple()[index]

    def __add__(self,other) -> 'Vec2':
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(self.x+other.x, self.y+other.y)

    def __radd__(self,other) -> 'Vec2':
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(other.x+self.x, other.y+self.y)

    def __sub__(self,other) -> 'Vec2':
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(self.x-other.x, self.y-other.y)

    def __rsub__(self,other) -> 'Vec2':
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(other.x-self.x, other.y-self.y)

    def __mul__(self,other) -> 'Vec2':
        try:
            k = float(other)
            return Vec2(self.x*k, self.y*k)
        except (TypeError,ValueError):
            return NotImplemented

    def __rmul__(self,other) -> 'Vec2':
        try:
            k = float(other)
            return Vec2(k*self.x, k*self.y)
        except (TypeError,ValueError):
            return NotImplemented

    def __truediv__(self,other) -> 'Vec2':
        try:
            k = float(other)
            return Vec2(self.x/k, self.y/k)
        except (TypeError,ValueError):
            return NotImplemented

    def __matmul__(self,other) -> float:
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return self.x*other.x + self.y*other.y

    def __neg__(self) -> 'Vec2':
        return Vec2(-self.x, -self.y)

    def __pos__(self) -> 'Vec2':
        return self

    def __abs__(self) -> float:
        return self.magnitude()

    def copy(self) -> 'Vec2':
        '''
        Return a new object as a copy.
        '''
        return Vec2(self.x,self.y)

    def magnitude(self):
        '''
        Euclidean vector magnitude.
        '''
        return math.hypot(self.x,self.y)

    def magnitudeSquared(self):
        '''
        Squared euclidean vector magnitude.
        '''
        return self.x*self.x + self.y*self.y

    @staticmethod
    def cross(left,right) -> float:
        '''
        Cross product (a scalar for 2D vectors).
        '''
        left = Vec2(left)
        right = Vec2(right)
        return left.x*right.y - left.y*right.x

    @staticmethod
    def distance(left,right) -> float:
        '''
        Distance between 2 vectors.
        '''
        left = Vec2(left)
        right = Vec2(right)
        return abs(left-right)

    @staticmethod
    def lerp(left,right,t) -> 'Vec2':
        '''
        Linear interpolation of 2 vectors.
        '''
        left = Vec2(left)
        right = Vec2(right)
        t = float(t)
        return Vec2(left.x + (right.x-left.x)*t, left.y + (right.y-left.y)*t)

    @staticmethod
    def midpoint(left,right) -> 'Vec2':
        '''
        Midpoint of 2 vectors.
        '''
        left = Vec2(left)
        right = Vec2(right)
        return Vec2((left.x+right.x)*0.5, (left.y+right.y)*0.5)

    @staticmethod
    def angleBetweenRad(left,right) -> float:
        '''
        Angle between 2 vectors in radians from 0 to pi.
        '''
        left = Vec2(left)
        right = Vec2(right)
        # numerically stable atan2 method instead of standard arccos
        return math.atan2(abs(Vec2.cross(left,right)), left@right)

    @staticmethod
    def angleBetweenDeg(left,right) -> float:
        '''
        Angle between 2 vectors in degrees from 0 to 180.
        '''
        return math.degrees(Vec2.angleBetweenRad(left,right))

    def projectOnto(self,other) -> 'Vec2':
        '''
        Projection of self onto other vector.
        This is the component parallel to other.
        May be unreliable or throw if other is near zero.
        '''
        other = Vec2(other)
        scale = (self@other) / other.magnitudeSquared()
        return scale * other

    def rejectFrom(self,other) -> 'Vec2':
        '''
        Rejection of self from other vector.
        This is the component orthogonal to other.
        May be unreliable or throw if other is near zero.
        '''
        other = Vec2(other)
        scale = (self@other) / other.magnitudeSquared()
        return self - scale*other

    def reflectAcrossPlane(self,normal) -> 'Vec2':
        '''
        Reflect across a plane given by its normal vector.
        This keeps the same orthogonal component and negates parallel component.
        May be unreliable or throw if normal is near zero.
        '''
        normal = Vec2(normal)
        scale = (self@normal) / normal.magnitudeSquared()
        return self - 2.0*scale*normal

    def reflectAlongAxis(self,axis) -> 'Vec2':
        '''
        Reflect along an axis vector.
        This keeps the same parallel component and negates orthogonal component.
        May be unreliable or throw if axis is near zero.
        '''
        axis = Vec2(axis)
        scale = (self@axis) / axis.magnitudeSquared()
        return 2.0*scale*axis - self

    def withX(self,x) -> 'Vec2':
        '''
        Return a new Vec2 by changing the x coordinate.
        '''
        return Vec2(float(x),self.y)

    def withY(self,y) -> 'Vec2':
        '''
        Return a new Vec2 by changing the y coordinate.
        '''
        return Vec2(self.x,float(y))

    def normalize(self) -> 'Vec2':
        '''
        Return a new Vec2 unit vector with the same direction.
        If self is 0 or near 0, this may be unreliable or throw.
        '''
        return self / abs(self)

    def perp(self) -> 'Vec2':
        '''
        Rotate 90 degrees in the positive direction.
        For y-up, this is counterclockwise.
        For y-down, this is clockwise.
        '''
        return Vec2(-self.y, self.x)

    def angleRad(self) -> float:
        '''
        Polar angle in radians from 0 to 2*pi.
        '''
        return math.atan2(self.y,self.x)

    def angleDeg(self) -> float:
        '''
        Polar angle in degrees from 0 to 360.
        '''
        return math.degrees(self.angleRad())

    def rotateRad(self,theta) -> 'Vec2':
        '''
        Rotate by theta radians.
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        c = math.cos(theta)
        s = math.sin(theta)
        return Vec2(self.x*c - self.y*s, self.x*s + self.y*c)

    def rotateDeg(self,theta) -> 'Vec2':
        '''
        Rotate by theta degrees.
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        return self.rotateRad(math.radians(theta))
