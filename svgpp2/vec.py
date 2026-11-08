'''
Vector types for points and directions in math calculations

Design notes:
- immutable to be reusable, avoid unexpected changes, and be hashable
- direction tolerances do not depend on scale, use nonzero vectors as is
- reasonably robust for huge and tiny coordinate scales
- strictly avoids infinity and nan to be SVG compatible (using exceptions)
- coordinate scales up to order 1e150 or 1e-150 may work fine since calculations
  require squaring/multiplying, but that is an unexpected use case, SVG scale
  should be much closer to unit scaling in practice
'''

import math
from typing import Iterator,Union

from .helpers import sincosRad

__all__ = [
    'Vec2',
    'Vec2LikeType'
]

# Vec2 and related types that express its quantities.
Vec2LikeType = Union['Vec2',tuple,list]

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

class Vec2:
    '''
    An immutable 2D vector.

    Used for coordinates in math diagrams, SVG canvas coordinates, and
    calculations. Directions are handled independent of scaling, using nonzero
    vectors as is. Client code is responsible for detecting when a near zero
    vector resulting from calculations may have a meaningless direction.
    This is a generic vector that can reasonably tolerate huge/tiny coordinates.

    Construction
    - Supports Vec2 or length 2 tuple/list as a single argument
    - Otherwise 2 floats (or convertible to) must be provided
    - Cannot contain infinity or nan
    '''
    x: float
    y: float
    __slots__ = ('x','y')

    def __init__(self, x: float|Vec2LikeType|None = None, y: float|None = None):
        '''
        Construction supported from
        - 2 scalars which are converted to float
        - another Vec2
        - tuple or list with 2 elements which are converted to float
        - infinity and nan are not allowed
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
                raise ValueError(f'Vec2 init from tuple/list requires length 2, provided {len(x)}')
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
        if not math.isfinite(valueX) or not math.isfinite(valueY):
            raise OverflowError(f'Vec2 value contains inf or nan: x={valueX!r}, y={valueY!r}')
        # bypass the __setattr__ exception for construction
        # Vec2.__setattr__ throws to enforce immutability
        object.__setattr__(self,'x',valueX)
        object.__setattr__(self,'y',valueY)

    @staticmethod
    def fromPolarRad(r: float, thetaRad: float) -> Vec2:
        '''
        Construct from polar coordinates with theta in radians.
        theta=0 is at the +x axis.
        For y-up, the rotation is counterclockwise.
        For y-down, the rotation is clockwise.
        Note that this allows a negative radius.
        '''
        if not math.isfinite(r) or not math.isfinite(thetaRad):
            raise OverflowError(f'Vec2 polar args contains inf or nan: r={r!r}, theta={thetaRad!r}')
        r = float(r)
        thetaRad = float(thetaRad)
        return Vec2(r*math.cos(thetaRad), r*math.sin(thetaRad))

    @staticmethod
    def fromPolarDeg(r: float, thetaDeg: float) -> Vec2:
        '''
        Construct from polar coordinates with theta in degrees.
        theta=0 is at the +x axis.
        For y-up, the rotation is counterclockwise.
        For y-down, the rotation is clockwise.
        Note that this allows a negative radius.
        '''
        return Vec2.fromPolarRad(r,math.radians(thetaDeg))

    def __setattr__(self, name, value):
        raise AttributeError('Vec2 is immutable')

    def __delattr__(self, name):
        raise AttributeError('Vec2 is immutable')

    def __repr__(self) -> str:
        return f'Vec2({self.x!r},{self.y!r})'

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    def __eq__(self, other):
        '''
        Compares Vec2 equality exactly. To avoid surprises with containers,
        we do not support comparing directly to tuple/list.
        '''
        if isinstance(other,Vec2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        '''
        True if both objects are not exactly equal Vec2.
        '''
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
        # this should work ok with +0.0 == -0.0 since hash(+0.0) == hash(-0.0)
        return hash((self.x,self.y))

    def __bool__(self):
        '''
        Vec2 is not convertible to bool. This raises TypeError.
        '''
        # this can be unintuitive so choosing to avoid bool conversion
        raise TypeError('Vec2 is not convertible to bool, consider using isZero()')

    def isZero(self) -> bool:
        '''
        True if this vector is exactly zero.
        '''
        return self.x == 0.0 and self.y == 0.0

    def __iter__(self) -> Iterator[float]:
        '''
        Yields the x and y coordinates.
        '''
        yield self.x
        yield self.y

    def __len__(self) -> int:
        '''
        Vec2 has x and y components.
        '''
        return 2

    def __getitem__(self, index: int) -> float:
        '''
        Vector components can be accessed at indexes 0 and 1.

        Raises IndexError otherwise.
        '''
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError(f'Vec2 has 2 components, invalid index: {index}')

    def __reduce__(self):
        '''
        How to reconstruct object, usually for pickle.
        '''
        return (Vec2,self.asTuple())

    def __copy__(self):
        '''
        Shallow copy (self because immutable).
        '''
        return self

    def __deepcopy__(self, memo):
        '''
        Deep copy (self because immutable).
        '''
        return self

    def __add__(self, other) -> Vec2:
        '''
        Vector addition.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(self.x+other.x, self.y+other.y)

    def __radd__(self, other) -> Vec2:
        '''
        Vector addition.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(other.x+self.x, other.y+self.y)

    def __sub__(self, other) -> Vec2:
        '''
        Vector subtraction.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(self.x-other.x, self.y-other.y)

    def __rsub__(self, other) -> Vec2:
        '''
        Vector subtraction.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        return Vec2(other.x-self.x, other.y-self.y)

    def __mul__(self, other) -> Vec2:
        '''
        Vector multiplication by a scalar.
        '''
        try:
            k = float(other)
        except (TypeError,ValueError):
            return NotImplemented
        if not math.isfinite(k):
            raise ValueError(f'Vec2 multiplication scalar must be finite, not {k!r}')
        return Vec2(self.x*k, self.y*k)

    def __rmul__(self, other) -> Vec2:
        '''
        Vector multiplication by a scalar.
        '''
        try:
            k = float(other)
        except (TypeError,ValueError):
            return NotImplemented
        if not math.isfinite(k):
            raise ValueError(f'Vec2 multiplication scalar must be finite, not {k!r}')
        return Vec2(k*self.x, k*self.y)

    def __truediv__(self, other) -> Vec2:
        '''
        Vector division by a scalar.

        Raises ZeroDivisionError if other is zero.
        '''
        try:
            k = float(other)
        except (TypeError,ValueError):
            return NotImplemented
        if not math.isfinite(k):
            raise ValueError(f'Vec2 division scalar must be finite, not {k!r}')
        if k == 0.0:
            raise ZeroDivisionError('cannot divide a Vec2 by zero')
        return Vec2(self.x/k, self.y/k)

    def __matmul__(self, other) -> float:
        '''
        Computes the dot product of 2 vectors.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        result = self.x*other.x + self.y*other.y
        if not math.isfinite(result):
            # note: unsupported pathological case
            # coordinate scales roughly 10^-150 to 10^150 should be ok
            # possibly more robust by normalizing then multiplying scales
            raise OverflowError(f'Vec2 dot product result is inf/nan: '
                f'{self!r} @ {other!r} = {result!r}')
        return result

    def __rmatmul__(self, other) -> float:
        '''
        Computes the dot product of 2 vectors.
        '''
        try:
            other = Vec2(other)
        except (TypeError,ValueError):
            return NotImplemented
        result = other.x*self.x + other.y*self.y
        if not math.isfinite(result):
            # note: unsupported pathological case
            # coordinate scales roughly 10^-150 to 10^150 should be ok
            # possibly more robust by normalizing then multiplying scales
            raise OverflowError(f'Vec2 dot product result is inf/nan: '
                f'{self!r} @ {other!r} = {result!r}')
        return result

    def __neg__(self) -> Vec2:
        '''
        Negation of a vector (opposite direction).
        '''
        return Vec2(-self.x, -self.y)

    def __pos__(self) -> Vec2:
        '''
        Equal to the same vector.
        '''
        return self

    def __abs__(self) -> float:
        '''
        Euclidean magnitude of the vector.
        '''
        # note: this can overflow in unsupported pathological cases
        return self.magnitude()

    def copy(self) -> Vec2:
        '''
        Return self (since Vec2 is immutable).
        '''
        return self

    def magnitude(self) -> float:
        '''
        Euclidean vector magnitude.
        '''
        result = math.hypot(self.x,self.y)
        if not math.isfinite(result):
            # note: unsupported pathological case
            raise OverflowError(f'Vec2 magnitude overflowed: {self!r}')
        return result

    def magnitudeSquared(self) -> float:
        '''
        Squared Euclidean vector magnitude.
        '''
        result = self.x*self.x + self.y*self.y
        if not math.isfinite(result):
            # note: unsupported pathological case
            # coordinate scales roughly 10^-150 to 10^150 should be ok
            raise OverflowError(f'Vec2 squared magnitude overflowed: {self!r}')
        return result

    @staticmethod
    def cross(left: Vec2LikeType, right: Vec2LikeType) -> float:
        '''
        Cross product (a scalar for 2D vectors).
        This value is the z coordinate when thinking of Vec2 in the x-y plane.
        '''
        left = Vec2(left)
        right = Vec2(right)
        result = left.x*right.y - left.y*right.x
        if not math.isfinite(result):
            # note: this is an unsupported pathological case
            # coordinate scales roughly 10^-150 to 10^150 should be ok
            # possibly more robust by normalizing then multiplying scales
            raise OverflowError(f'Vec2 cross product result is inf or nan: '
                f'{left!r} x {right!r} = {result!r}')
        return result

    @staticmethod
    def distance(left: Vec2LikeType, right: Vec2LikeType) -> float:
        '''
        Distance between 2 vectors.
        '''
        left = Vec2(left)
        right = Vec2(right)
        # note: can overflow in unsupported pathological cases
        return abs(left-right)

    @staticmethod
    def lerp(left: Vec2LikeType, right: Vec2LikeType, t: float) -> Vec2:
        '''
        Linear interpolation of 2 vectors.
        Generally we would use t in [0,1] but it is not restricted to that.
        '''
        left = Vec2(left)
        right = Vec2(right)
        t = float(t)
        if not math.isfinite(t):
            raise OverflowError(f'Vec2 lerp constant not finite: {t!r}')
        # note: can overflow in unsupported pathological cases
        return Vec2(left.x + (right.x-left.x)*t, left.y + (right.y-left.y)*t)

    @staticmethod
    def midpoint(left: Vec2LikeType, right: Vec2LikeType) -> Vec2:
        '''
        Midpoint of 2 vectors.
        '''
        left = Vec2(left)
        right = Vec2(right)
        # note: can overflow in unsupported pathological cases
        # unnecessary but the alternative (0.5*left + 0.5*right) can handle larger numbers
        return Vec2((left.x+right.x)*0.5, (left.y+right.y)*0.5)

    # Some operations can benefit from being able to check if a vector is
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
    def angleBetweenRad(left: Vec2LikeType, right: Vec2LikeType) -> float:
        '''
        Angle between 2 vectors in radians from 0 to pi.

        Raises ValueError if either vector is zero.

        This is not reliable if either vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
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
    def angleBetweenDeg(left: Vec2LikeType, right: Vec2LikeType) -> float:
        '''
        Angle between 2 vectors in degrees from 0 to 180.

        Raises ValueError if either vector is zero.

        This is not reliable if either vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
        '''
        return math.degrees(Vec2.angleBetweenRad(left,right))

    def projectOnto(self, other: Vec2LikeType) -> Vec2:
        '''
        Projection of self onto other vector.
        This is the component parallel to other.

        Raises ZeroDivisionError if vector is zero.

        This is not reliable if other vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
        '''
        other = Vec2(other)
        if other.isZero():
            raise ZeroDivisionError('projectOnto requires a nonzero vector')
        other = other.normalize()
        return (self@other)*other

    def rejectFrom(self, other: Vec2LikeType) -> Vec2:
        '''
        Rejection of self from other vector.
        This is the component orthogonal to other.

        Raises ZeroDivisionError if vector is zero.

        This is not reliable if other vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
        '''
        other = Vec2(other)
        if other.isZero():
            raise ZeroDivisionError('rejectFrom requires a nonzero vector')
        return self - self.projectOnto(other)

    def reflectAcrossPlane(self, normal: Vec2LikeType) -> Vec2:
        '''
        Reflect across a plane given by its normal vector.
        This keeps the same orthogonal component and negates the parallel component.

        Raises ZeroDivisionError if normal vector is zero.

        This is not reliable if normal vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
        '''
        normal = Vec2(normal)
        if normal.isZero():
            raise ZeroDivisionError('reflectAcrossPlane requires a nonzero normal vector')
        return self - 2.0*self.projectOnto(normal)

    def reflectAlongAxis(self, axis: Vec2LikeType) -> Vec2:
        '''
        Reflect along an axis vector.
        This keeps the same parallel component and negates the orthogonal component.

        Raises ZeroDivisionError if axis vector is zero.

        This is not reliable if axis vector is nearly zero due to roundoff
        error. It is fine if a vector is intentionally used for direction only.
        '''
        axis = Vec2(axis)
        if axis.isZero():
            raise ZeroDivisionError('reflectAlongAxis requires a nonzero axis vector')
        return 2.0*self.projectOnto(axis) - self

    def withX(self, x: float) -> Vec2:
        '''
        Return a new Vec2 by changing the x coordinate.
        '''
        return Vec2(float(x), self.y)

    def withY(self, y: float) -> Vec2:
        '''
        Return a new Vec2 by changing the y coordinate.
        '''
        return Vec2(self.x, float(y))

    def normalize(self) -> Vec2:
        '''
        Return a new Vec2 unit vector with the same direction.

        Raises ZeroDivisionError if self is zero.

        This is not reliable if self is nearly zero due to roundoff error.
        '''
        if self.isZero():
            raise ZeroDivisionError('cannot normalize the zero vector')
        # note: can overflow in unsupported pathological cases
        # the largest numbers can be handled by first dividing the max norm
        return self / abs(self)

    def directionAndMagnitude(self) -> tuple[Vec2,float]:
        '''
        Simultaneously compute the direction and magnitude.
        The direction is equivalent to calling .normalize().

        Raises ZeroDivisionError if self is zero.

        This is not reliable if self is nearly zero due to roundoff error.
        '''
        if self.isZero():
            raise ZeroDivisionError('cannot normalize the zero vector')
        # note: magnitude can overflow in unsupported pathological cases
        mag = abs(self)
        return (self/mag, mag)

    def perp(self) -> Vec2:
        '''
        Rotate 90 degrees in the positive direction.
        For y-up, this is counterclockwise.
        For y-down, this is clockwise.
        '''
        return Vec2(-self.y, self.x)

    def angleRad(self) -> float:
        '''
        Polar angle in radians from 0 to 2pi.

        Raises ValueError if vector is zero.

        This is not reliable if self is close to zero due to roundoff error.
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

        Raises ValueError if vector is zero.

        This is not reliable if self is close to zero due to roundoff error.
        '''
        return math.degrees(self.angleRad())

    def signedAngleRad(self) -> float:
        '''
        Polar angle in radians from -pi to +pi.

        Raises ValueError if vector is zero.

        This is not reliable if self is close to zero due to roundoff error.
        '''
        if self.isZero():
            raise ValueError('angle is undefined for the zero vector')
        angle = math.atan2(self.y,self.x)
        return 0.0 if angle == 0.0 else angle

    def signedAngleDeg(self) -> float:
        '''
        Polar angle in degrees from -180 to +180.

        Raises ValueError if vector is zero.

        This is not reliable if self is close to zero due to roundoff error.
        '''
        return math.degrees(self.signedAngleRad())

    def sincos(self) -> tuple[float,float]:
        '''
        Simultaneously compute the sine and cosine of the plane angle.

        Raises ValueError if self is zero.
        '''
        if self.isZero():
            raise ValueError('angle is undefined for the zero vector')
        v = self.normalize()
        return (v.y,v.x)

    def sincosRadius(self) -> tuple[float,float,float]:
        '''
        Simultaneously compute the sine, cosine, and radius.

        Raises ValueError if self is zero.
        '''
        if self.isZero():
            raise ValueError('angle is undefined for the zero vector')
        v,mag = self.directionAndMagnitude()
        return (v.y,v.x,mag)

    def rotateRad(self, thetaRad: float) -> Vec2:
        '''
        Rotate by theta radians.
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        if not math.isfinite(thetaRad):
            raise OverflowError(f'Vec2 rotation angle not finite: {thetaRad!r}')
        s,c = sincosRad(thetaRad)
        return Vec2(self.x*c - self.y*s, self.x*s + self.y*c)

    def rotateDeg(self, thetaDeg: float) -> Vec2:
        '''
        Rotate by theta degrees.
        For y-up and positive theta, this is counterclockwise.
        For y-down and positive theta, this is clockwise.
        '''
        return self.rotateRad(math.radians(thetaDeg))

    @staticmethod
    def areNearlyEqual(left: Vec2LikeType, right: Vec2LikeType, *,
            relTol: float = 1e-9, absTol: float = 0.0) -> bool:
        '''
        Check if 2 vectors are almost equal with provided tolerances.
        Uses the max of the vector magnitudes as the scale for relative error.
        '''
        relTol = _checkTol(relTol)
        absTol = _checkTol(absTol)
        left = Vec2(left)
        right = Vec2(right)
        # note: can overflow in unsupported pathological cases
        dist = Vec2.distance(left,right)
        if dist <= absTol:
            return True
        scale = max(left.magnitude(),right.magnitude())
        return dist <= scale*relTol

    @staticmethod
    def areParallel(left: Vec2LikeType, right: Vec2LikeType, *, tol: float = 1e-9) -> bool:
        '''
        Check if 2 vectors are parallel up to a given tolerance.
        Note that this includes opposite direction (anti parallel) vectors.

        This handles normalized direction only for any nonzero vectors. If an
        input can be close enough to zero to be meaningless, then client code
        must check for and handle that.
        '''
        tol = _checkTol(tol)
        left = Vec2(left)
        right = Vec2(right)
        if left.isZero() or right.isZero():
            return False
        # note: can overflow in unsupported pathological cases
        left = left.normalize()
        right = right.normalize()
        return abs(Vec2.cross(left,right)) <= tol

    @staticmethod
    def areOrthogonal(left: Vec2LikeType, right: Vec2LikeType, *, tol: float = 1e-9) -> bool:
        '''
        Check if 2 vectors are orthogonal up to a given tolerance.

        This handles normalized direction only for any nonzero vectors. If an
        input can be close enough to zero to be meaningless, then client code
        must check for and handle that.
        '''
        tol = _checkTol(tol)
        left = Vec2(left)
        right = Vec2(right)
        if left.isZero() or right.isZero():
            return False
        # note: can overflow in unsupported pathological cases
        left = left.normalize()
        right = right.normalize()
        return abs(left@right) <= tol
