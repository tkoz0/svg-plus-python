'''
Vector types

Design notes:
- immutable to be reusable, avoid unexpected changes, and be hashable
- no tolerances which depend on scale, to support very large and very small
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
        '''
        Construction supported from
        - 2 scalars which are converted to float
        - another Vec2
        - tuple or list with 2 elements which are converted to float
        '''
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
        elif x is None and y is None:
            # default construction (zero vector)
            valueX = 0.0
            valueY = 0.0
        else:
            if x is None or y is None:
                raise ValueError('Vec2 init from scalars requires both components')
            valueX = float(x)
            valueY = float(y)
        # bypass the __setattr__ exception for construction
        # Vec2.__setattr__ throws to enforce immutability
        object.__setattr__(self,'x',valueX)
        object.__setattr__(self,'y',valueY)

    @staticmethod
    def fromPolarRad(r,theta) -> 'Vec2':
        '''
        Construct from polar coordinates with theta in radians.
        theta=0 is at the +x axis.
        For y-up, the rotation is counter clockwise.
        For y-down, the rotation is clockwise.
        '''
        r = float(r)
        theta = float(theta)
        return Vec2(r*math.cos(theta), r*math.sin(theta))

    @staticmethod
    def fromPolarDeg(r,theta) -> 'Vec2':
        '''
        Construct from polar coordinates with theta in degrees.
        theta=0 is at the +x axis.
        For y-up, the rotation is counter clockwise.
        For y-down, the rotation is clockwise.
        '''
        return Vec2.fromPolarRad(r,math.radians(theta))

    def __setattr__(self,name,value):
        raise AttributeError('Vec2 is immutable')

    def __delattr__(self,name):
        raise AttributeError('Vec2 is immutable')

    def __repr__(self) -> str:
        return f'Vec2({self.x!r},{self.y!r})'

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    def __eq__(self,other):
        if isinstance(other,Vec2):
            return self.x == other.x and self.y == other.y
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

    def __bool__(self):
        # this can be unintuitive so choosing to avoid bool conversion
        raise TypeError('Vec2 is not convertible to bool, consider using isZero()')

    def isZero(self) -> bool:
        '''
        True if this vector is zero.
        '''
        return self.x == 0.0 and self.y == 0.0

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def __getitem__(self,index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError('Vec2 has 2 components')

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
        except (TypeError,ValueError):
            return NotImplemented
        if k == 0.0:
            raise ZeroDivisionError('cannot divide a vector by zero')
        return Vec2(self.x/k, self.y/k)

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
        Return a new object as a copy (self since Vec2 is immutable).
        '''
        return self

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
        This value is the z coordinate when thinking of Vec2 in the x-y plane.
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

    # Some operations would benefit from being able to check if a vector is
    # close to zero to avoid accidental meaningless operations on something
    # that is very likely the zero vector. This requires knowing the scale,
    # and complicates the interface, so it would be better in the SVG classes
    # where the scale is known. The following operations are relevant:
    # - angle between
    # - plane angle
    # - normalizing
    # - projection
    # - rejection
    # - reflection

    @staticmethod
    def angleBetweenRad(left,right) -> float:
        '''
        Angle between 2 vectors in radians from 0 to pi.
        Throws if either vector is zero.
        This is not reliable if either vector is nearly zero.
        '''
        left = Vec2(left)
        right = Vec2(right)
        if left.isZero() or right.isZero():
            raise ValueError('cannot compute angle with a zero vector')
        # numerically stable atan2 method instead of standard:
        #     acos( (left@right) / (left.magnitude()*right.magnitude()) )
        # also normalize vectors first to mitigate overflow
        left = left.normalize()
        right = right.normalize()
        return math.atan2(abs(Vec2.cross(left,right)), left@right)

    @staticmethod
    def angleBetweenDeg(left,right) -> float:
        '''
        Angle between 2 vectors in degrees from 0 to 180.
        Throws if either vector is zero.
        This is not reliable if either vector is nearly zero.
        '''
        return math.degrees(Vec2.angleBetweenRad(left,right))

    def projectOnto(self,other) -> 'Vec2':
        '''
        Projection of self onto other vector.
        This is the component parallel to other.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        other = Vec2(other)
        if other.isZero():
            raise ZeroDivisionError('projectOnto requires a nonzero vector')
        other = other.normalize()
        return (self@other)*other

    def rejectFrom(self,other) -> 'Vec2':
        '''
        Rejection of self from other vector.
        This is the component orthogonal to other.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        other = Vec2(other)
        if other.isZero():
            raise ZeroDivisionError('rejectFrom requires a nonzero vector')
        other = other.normalize()
        return self - (self@other)*other

    def reflectAcrossPlane(self,normal) -> 'Vec2':
        '''
        Reflect across a plane given by its normal vector.
        This keeps the same orthogonal component and negates parallel component.
        Throws if normal vector is zero, not reliable if nearly zero.
        '''
        normal = Vec2(normal)
        if normal.isZero():
            raise ZeroDivisionError('reflectAcrossPlane requires a nonzero normal vector')
        return self - 2.0*self.projectOnto(normal)

    def reflectAlongAxis(self,axis) -> 'Vec2':
        '''
        Reflect along an axis vector.
        This keeps the same parallel component and negates orthogonal component.
        Throws if axis vector is zero, not reliable if nearly zero.
        '''
        axis = Vec2(axis)
        if axis.isZero():
            raise ZeroDivisionError('reflectAlongAxis requires a nonzero axis vector')
        return 2.0*self.projectOnto(axis) - self

    def withX(self,x) -> 'Vec2':
        '''
        Return a new Vec2 by changing the x coordinate.
        '''
        return Vec2(float(x), self.y)

    def withY(self,y) -> 'Vec2':
        '''
        Return a new Vec2 by changing the y coordinate.
        '''
        return Vec2(self.x, float(y))

    def normalize(self) -> 'Vec2':
        '''
        Return a new Vec2 unit vector with the same direction.
        If self is 0 or near 0, this may be unreliable or throw.
        '''
        if self.isZero():
            raise ZeroDivisionError('cannot normalize the zero vector')
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
        Polar angle in radians from 0 to 2pi.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        if self.isZero():
            raise ValueError('angle is undefined for the zero vector')
        angle = math.atan2(self.y,self.x)
        if angle < 0.0:
            angle += 2.0*math.pi
        # ensure we do not return -0.0
        return 0.0 if angle == 0.0 else angle

    def angleDeg(self) -> float:
        '''
        Polar angle in degrees from 0 to 360.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        return math.degrees(self.angleRad())

    def signedAngleRad(self) -> float:
        '''
        Polar angle in radians from -pi to +pi.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        if self.isZero():
            raise ValueError('angle is undefined for the zero vector')
        return math.atan2(self.y,self.x)

    def signedAngleDeg(self) -> float:
        '''
        Polar angle in degrees from -180 to +180.
        Throws if vector is zero, not reliable if nearly zero.
        '''
        return math.degrees(self.signedAngleRad())

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

    @staticmethod
    def areNearlyEqual(left,right,relTol=1e-9,absTol=0.0) -> bool:
        '''
        Check if 2 vectors are almost equal with provided tolerances.
        Uses the max of the vector magnitudes as the scale for relative error.
        '''
        left = Vec2(left)
        right = Vec2(right)
        dist = Vec2.distance(left,right)
        scale = max(left.magnitude(),right.magnitude())
        return dist <= max(scale*relTol, absTol)

    @staticmethod
    def areParallel(left,right,tol=1e-9) -> bool:
        '''
        Check if 2 vectors are parallel up to a given tolerance.
        '''
        left = Vec2(left)
        right = Vec2(right)
        if left.isZero() or right.isZero():
            return False
        left = left.normalize()
        right = right.normalize()
        return abs(Vec2.cross(left,right)) <= tol

    @staticmethod
    def areOrthogonal(left,right,tol=1e-9) -> bool:
        '''
        Check if 2 vectors are orthogonal up to a given tolerance.
        '''
        left = Vec2(left)
        right = Vec2(right)
        if left.isZero() or right.isZero():
            return False
        left = left.normalize()
        right = right.normalize()
        return abs(left@right) <= tol
