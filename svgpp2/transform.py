'''
2D transformation objects for convenience and SVG serialization

Design notes:
- all are immutable and convertible to Affine2
- construction from Affine2 is supported with tolerance checking
- combines the SVG layer intention with further useful math operations
'''

from .affine import Affine2,Affine2LikeType
from .helpers import numberFormatter,sincosDeg
from .vec import Vec2,Vec2LikeType

from abc import ABC, abstractmethod
import math
from typing import Callable

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

_DEFAULT_NUM_FMT = numberFormatter()

def _checkTolAndScale(tol: float, scale: float, /) -> tuple[float,float]:
    '''
    Checks that tolerance and scale are >= 0.
    Return both tolerance and scale converted to float.
    '''
    tol = float(tol)
    scale = float(scale)
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError(f'tolerance must be finite and >= 0, tol = {tol!r}')
    if not math.isfinite(scale) or scale < 0.0:
        raise ValueError(f'scale must be finite and >= 0, scale = {scale!r}')
    return (tol,scale)

def _checkAffine(affine: Affine2LikeType, /):
    '''
    Ensure a parameter is an affine like type for the fromAffine2 functions.
    '''
    if not isinstance(affine,Affine2) and not isinstance(affine,(tuple,list)):
        raise TypeError('expected an Affine2 or tuple/list with 6 elements')
    if isinstance(affine,(tuple,list)) and len(affine) != 6:
        raise ValueError(f'tuple/list length must be 6, not {len(affine)}')

def _mulIminusR(angleCos: float, angleSin: float, px: float, py: float, /) \
        -> tuple[float,float]:
    '''
    Perform a numerically stable multiplication by I-R for rotation matrix code.
    The I-R matrix is computed in a numerically stable way.
    Returns the product of (I-R)*p where p=(px,py) is the given point/vector.
    '''
    # see _invIminusR for how to do compute the matrix with numerical stability
    if angleCos > 0.0:
        diag = (angleSin*angleSin) / (1.0+angleCos)
    else:
        diag = 1.0-angleCos
    a,b = diag, angleSin
    c,d = -angleSin, diag
    p = Vec2(px,py)
    return (Vec2(a,b)@p, Vec2(c,d)@p)

def _invIminusR(angleCos: float, angleSin: float, ox: float, oy: float, tol: float, /) \
        -> tuple[float,float]|None:
    '''
    Solve the (I-R)c = o system for a rotation (from angleCos and angleSin)
    where R is the rotation matrix, I is the identity, o is the given vector
    (affine origin), and the solution vector is c, the rotation center.

    Returns None if the matrix system is singular (using the tolerance),
    otherwise the found center coordinates (cx,cy).
    '''
    # With rotation matrix R and center c, applied to a point x:
    #     x' = Rx - Rc + c = Rx + (I-R)c
    # So we already have the rotation matrix and need to solve for c,
    # which requires inverting this matrix
    #     [ 1-cos(theta)    sin(theta) ]
    #     [  -sin(theta)  1-cos(theta) ]
    # There is destructive cancellation when cos(theta) ~= 1 so we use an
    # alternative form as well which gives us 2 cases that avoid instability:
    #     when cos(theta) > 0: sin^2(theta) / (1+cos(theta))
    #     when cos(theta) < 0: 1-cos(theta)
    # In both cases, the concerning quantities (1 +- cos(theta)) stay O(1).
    # (not used) but an alternative formula which would add complexity is:
    #     1-cos(theta) = 2 * sin^2(theta/2)
    if angleCos > 0.0:
        diag = (angleSin*angleSin) / (1.0+angleCos)
    else:
        diag = 1.0-angleCos
    a,b = diag, angleSin
    c,d = -angleSin, diag
    det = Vec2.cross(Vec2(a,b),Vec2(c,d))
    if abs(det) < tol*tol:
        # We cannot uniquely solve for a center of a singular matrix.
        # The caller should use the computed angle and the origin.
        return None
    aI,bI = d/det, -b/det
    cI,dI = -c/det, a/det
    # c = (I-R)^-1 * o
    cx = aI*ox + bI*oy
    cy = cI*ox + dI*oy
    return (cx,cy)

def _isAngleZero(angleDeg: float, tol: float, /) -> bool:
    '''
    Check if an angle is zero within a tolerance.
    This is used for when rotations are indistinguishable from identity.
    This handles the 360 degree wrap around.
    '''
    # for the tolerance check, use the same matrix determinant check in _invIminusR()
    angleSin,angleCos = sincosDeg(angleDeg % 360.0)
    if angleCos > 0.0:
        det = 2.0*(angleSin*angleSin) / (1+angleCos)
    else:
        det = 2.0*(1.0-angleCos)
    return det <= tol*tol

_NumFmtT = Callable[[float],str]

class TransformBase(ABC):
    '''
    Base for SVG transformations.
    '''

    # Note: if we add __slots__ here then subclasses need to use it:
    # __slots__ = (*TransformBase.__slots__, myArg1, myArg2, ...)
    __slots__ = ()

    @abstractmethod
    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
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
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Convert an affine transformation to a transformation object.
        Raise ValueError if the provided affine transformation is not the
        correct type of transformation within the tolerance.

        If coordinates are at very large or very small scales, then scale
        dependent quantities do not work robustly. In these cases, scale
        can be adjusted to give these quantities a reasonable check.
        '''
        raise NotImplementedError('subclasses should implement fromAffine2()')

    @abstractmethod
    def inverse(self) -> TransformBase:
        '''
        Return the inverse transformation.
        '''
        raise NotImplementedError('subclasses should implement inverse()')

    @abstractmethod
    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Compose with another transformation. Keeps the specific transformation
        type if possible, otherwise falls back to TransformMatrix.

        Tolerance/scale are used:
        - By TransformScale to determine if it is close enough to uniform
          to have the same scale in both axes.
        - By TransformTranslate to determine if the rotation angle is close
          enough to zero to ignore it and if a rotation center is close enough
          to zero to use the origin.
        - By TransformRotate to check if a rotation angle is close enough to
          zero to be ignored and if a rotation center is close enough to zero
          to use the origin.
        '''
        raise NotImplementedError('subclasses should implement compose()')

    def isIdentity(self, *, tol: float = 1e-9, scale: float = 1.0) -> bool:
        '''
        True if the transformation is (within a tolerance) the identity transform.

        If coordinates are at very large or very small scales, then scale
        dependent quantities do not work robustly. In these cases, scale
        can be adjusted to give these quantities a reasonable check.
        '''
        tol,scale = _checkTolAndScale(tol,scale)
        affine = self.toAffine2()
        return (Vec2.areNearlyEqual(affine.origin,Vec2(0,0),relTol=0.0,absTol=tol*scale)
            and Vec2.areNearlyEqual(affine.xAxis,Vec2(1,0),relTol=0.0,absTol=tol)
            and Vec2.areNearlyEqual(affine.yAxis,Vec2(0,1),relTol=0.0,absTol=tol))

    def apply(self, x: float|Vec2LikeType, y: float|None = None) -> Vec2:
        '''
        Apply the transformation to a Vec2 point.
        '''
        return self.toAffine2().apply(x,y)

    def __setattr__(self, name, value):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __delattr__(self, name):
        raise AttributeError(f'{type(self).__name__} is immutable')

    def __bool__(self):
        '''
        Raises TypeError. Avoid conversion to bool.
        '''
        raise TypeError(f'{type(self).__name__} is not convertible to bool, '
            f'consider using isIdentity()')

    def __eq__(self, other):
        '''
        True if transforms have exactly equal Affine2 representations.
        Note that some mathematically equivalent transforms may not compare
        equal due to floating point error, for example the following may fail:
            TransformRotate(0.0) == TransformRotate(360.0)
        '''
        if isinstance(other,TransformBase):
            return self.toAffine2() == other.toAffine2()
        return NotImplemented

    def __ne__(self, other):
        '''
        True if both objects are not exactly equal transforms.
        '''
        eqResult = self == other
        return eqResult if eqResult is NotImplemented else not eqResult

    def __hash__(self) -> int:
        return hash(self.toAffine2())

    def __copy__(self) -> TransformBase:
        '''
        Shallow copy (self because immutable).
        '''
        return self

    def __deepcopy__(self, memo) -> TransformBase:
        '''
        Deep copy (self because immutable).
        '''
        return self

    def copy(self) -> TransformBase:
        '''
        Return self because transforms are immutable.
        '''
        return self

    def __reduce__(self):
        '''
        How to reconstruct object, usually for pickle.
        '''
        # All subclasses follow this pattern where the constructor arguments
        # are ordered the same as the slots. If this changes or a new subclass
        # does not follow the pattern, override __reduce__.
        return (type(self), tuple(getattr(self,slot) for slot in type(self).__slots__))

    @staticmethod
    def areNearlyEqual(left: TransformBase, right: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> bool:
        '''
        Compare 2 transformations for near equality.
        '''
        tol,scale = _checkTolAndScale(tol,scale)
        leftAffine = left.toAffine2()
        rightAffine = right.toAffine2()
        return (
            Vec2.areNearlyEqual(leftAffine.origin,rightAffine.origin,relTol=0.0,absTol=tol*scale)
            and Vec2.areNearlyEqual(leftAffine.xAxis,rightAffine.xAxis,relTol=0.0,absTol=tol)
            and Vec2.areNearlyEqual(leftAffine.yAxis,rightAffine.yAxis,relTol=0.0,absTol=tol))

class TransformTranslate(TransformBase):
    '''
    Translation transformation, for SVG.
    Constructor args are passed to Vec2.
    '''
    offset: Vec2
    __slots__ = ('offset',)

    def __init__(self, ox: float|Vec2LikeType|None = None, oy: float|None = None):
        '''
        Initialize a translation. The arguments are passed to Vec2 so it is
        compatible with floats, Vec2, or tuple/list pairs.
        '''
        object.__setattr__(self,'offset',Vec2(ox,oy))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
        ox,oy = self.offset
        return f'translate({numFmt(ox)} {numFmt(oy)})'

    def toAffine2(self) -> Affine2:
        return Affine2.translate(self.offset)

    @staticmethod
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformTranslate:
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale)
        affine = Affine2(affine)
        if (not Vec2.areNearlyEqual(affine.xAxis,Vec2(1,0),relTol=0.0,absTol=tol)
            or not Vec2.areNearlyEqual(affine.yAxis,Vec2(0,1),relTol=0.0,absTol=tol)):
            raise ValueError(f'Not a translation (linear part is not identity): {affine!r}')
        return TransformTranslate(affine.origin)

    def inverse(self) -> TransformTranslate:
        return TransformTranslate(-self.offset)

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Tolerance is used to check if the rotation is close enough to identity
        to ignore it. Scale is used to determine when a point is close enough
        to the origin to be considered zero.
        '''
        tol,scale = _checkTolAndScale(tol,scale)
        if isinstance(other,TransformTranslate):
            return TransformTranslate(self.offset + other.offset)
        elif isinstance(other,TransformRotate):
            if _isAngleZero(other.angleDeg,tol):
                # rotation is almost zero so just keep the translation part
                return self
            else:
                # let o=(ox,oy) be translation offset (self)
                # let theta be the rotation angle (other)
                # let c=(cx,cy) be the rotation center (other)
                # multiply the translation with the 3 matrices forming the
                # rotation: offset (cx,cy), rotate theta, offset (-cx,-cy)
                # then we find the linear part is R (rotation matrix) and the
                # offset of the resulting affine is:
                #     [ -cx*cos(theta) + cy*sin(theta) + cx + ox ]
                #     [ -cx*sin(theta) - cy*cos(theta) + cy + oy ]
                # equal to: (I-R)c + o
                # solving for rotation center as in TransformRotate.fromAffine2,
                # the resulting rotation center is c + (I-R)^-1 * o
                # we can use _invIminusR to multiply o by (I-R)^-1
                angleSin,angleCos = sincosDeg(other.angleDeg)
                ox,oy = self.offset
                invResult = _invIminusR(angleCos,angleSin,ox,oy,tol)
                if invResult is None: # angle close to zero, use translation only
                    return self
                else:
                    dx,dy = invResult
                    c = other.center if other.center is not None else Vec2()
                    px,py = c.x + dx, c.y + dy
                    if Vec2.areNearlyEqual((px,py),Vec2(),relTol=0.0,absTol=tol*scale):
                        return TransformRotate(other.angleDeg)
                    else:
                        return TransformRotate(other.angleDeg,px,py)
        else:
            return TransformMatrix(self.toAffine2().compose(other.toAffine2()))

    def __repr__(self) -> str:
        return f'TransformTranslate({self.offset!r})'

class TransformRotate(TransformBase):
    '''
    Rotation transformation, optionally around a center point, for SVG.
    The angle is in degrees. The center point is passed to Vec2.
    '''
    angleDeg: float
    center: Vec2|None
    __slots__ = ('angleDeg','center')

    def __init__(self, angleDeg: float = 0.0,
            cx: float|Vec2LikeType|None = None, cy: float|None = None):
        '''
        Initialize a rotation. The angle is in degrees.
        If a center is provided, it is included with the serialization,
        otherwise only the rotation angle is included.
        '''
        if not math.isfinite(angleDeg):
            raise ValueError(f'angle must be finite, not {angleDeg!r}')
        object.__setattr__(self,'angleDeg',float(angleDeg))
        if cx is None and cy is None:
            object.__setattr__(self,'center',None)
        else:
            object.__setattr__(self,'center',Vec2(cx,cy))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
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
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformRotate:
        '''
        If the rotation angle is near zero and the origin is nonzero, the center
        cannot be uniquely determined and this will return a rotation with a
        small angle and origin center.
        '''
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale)
        affine = Affine2(affine)
        # if R is the rotation matrix and c is the center, then applied to x:
        # x' = Rx - Rc + c, so we have the rotation matrix and need c next
        if not math.isclose(affine.xAxis.magnitudeSquared(),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (x axis is not unit length): {affine!r}')
        if not math.isclose(affine.yAxis.magnitudeSquared(),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (y axis is not unit length): {affine!r}')
        if not Vec2.areOrthogonal(affine.xAxis,affine.yAxis,tol=tol):
            raise ValueError(f'Not a rotation (axes are not orthogonal): {affine!r}')
        # compute determinant from cross product
        if not math.isclose(Vec2.cross(affine.xAxis,affine.yAxis),1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a rotation (includes a reflection, det = -1): {affine!r}')
        # xAxis is (cos(theta),sin(theta)) so we can use its plane angle
        angleDeg = affine.xAxis.angleDeg()
        # origin 0 means it is purely a rotation
        if Vec2.areNearlyEqual(affine.origin,Vec2(),relTol=0.0,absTol=tol*scale):
            return TransformRotate(angleDeg)
        # now we need the matrix inverse to solve (-Rc+Ic)=(-R+I)c=o
        # (where R is the matrix part, I is identity, c is center, o is affine.origin)
        angleCos,angleSin = affine.xAxis
        ox,oy = affine.origin
        invResult = _invIminusR(angleCos,angleSin,ox,oy,tol)
        if invResult is None:
            return TransformRotate(angleDeg)
        else:
            return TransformRotate(angleDeg,*invResult)

    def inverse(self) -> TransformRotate:
        if self.center is None:
            return TransformRotate(-self.angleDeg)
        else:
            return TransformRotate(-self.angleDeg,self.center)

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Tolerance is used to check if the rotation is close enough to identity
        to ignore it. Scale is used to determine when a point is close enough
        to the origin to be considered zero.
        '''
        tol,scale = _checkTolAndScale(tol,scale)
        if isinstance(other,TransformRotate):
            # let self be a rotation by a(alpha) around c=(cx,cy)
            # let other be a rotation by b(beta) around d=(dx,dy)
            # consider the multiplication in block matrix form
            #     [ R_a  (I-R_a)c ] [ R_b  (I-R_b)d ]
            #     [ 0^T     1     ] [ 0^T     1     ]
            # the resulting composition is
            #     [ R_a*R_b  R_a(I-R_b)d + (I-R_a)c ]
            #     [   0^T              1            ]
            # so to find the new center, we need to multiply the origin part by
            # the inverse of (I-R_a*R_b), so we use _invIminusR
            # first the alpha+beta angle
            angleDeg = self.angleDeg + other.angleDeg
            if _isAngleZero(angleDeg,tol):
                # the angles cancel and we have a translation remaining
                # the translation part is (I-R)(c-d) where
                #     R = rotation matrix of self
                #     c = center of self
                #     d = center of other
                px,py = ((self.center if self.center is not None else Vec2())
                    - (other.center if other.center is not None else Vec2()))
                # multiply by the rotation matrix for self
                alphaSin,alphaCos = sincosDeg(self.angleDeg)
                tx,ty = _mulIminusR(alphaCos,alphaSin,px,py)
                if Vec2.areNearlyEqual((tx,ty),Vec2(),relTol=0.0,absTol=tol*scale):
                    return TransformTranslate(0.0,0.0)
                else:
                    return TransformTranslate(tx,ty)
            # rotation centers
            cx,cy = self.center if self.center is not None else Vec2()
            dx,dy = other.center if other.center is not None else Vec2()
            # compute cPart = (I-R_a)c
            alphaSin,alphaCos = sincosDeg(self.angleDeg)
            cPartX,cPartY = _mulIminusR(alphaCos,alphaSin,cx,cy)
            # compute dPart = R_a(I-R_b)d
            betaSin,betaCos = sincosDeg(other.angleDeg)
            dPartX,dPartY = _mulIminusR(betaCos,betaSin,dx,dy)
            dPartX,dPartY = dPartX*alphaCos - dPartY*alphaSin, dPartX*alphaSin + dPartY*alphaCos
            # now we multiply dPart+cPart by (I-R_a*R_b)^-1
            angleSin,angleCos = sincosDeg(angleDeg)
            invResult = _invIminusR(angleCos,angleSin, dPartX+cPartX, dPartY+cPartY, tol)
            if invResult is None: # angle close to zero
                # this branch should be unreachable in practice
                return TransformMatrix(self.toAffine2().compose(other.toAffine2()))
            else:
                px,py = invResult
                if Vec2.areNearlyEqual((px,py),Vec2(),relTol=0.0,absTol=tol*scale):
                    return TransformRotate(angleDeg)
                else:
                    return TransformRotate(angleDeg,px,py)
        elif isinstance(other,TransformTranslate):
            if _isAngleZero(self.angleDeg,tol):
                # rotation is almost zero so just keep the translation part
                return other
            else:
                # let o=(ox,oy) be the translation offset (other)
                # let theta be the rotation angle (self)
                # let c=(cx,cy) be the rotation center (self)
                # multiply the 3 matrices forming the rotation with the translation
                # (the 3 for rotation are offset (cx,cy), rotate theta, offset (-cx,-cy))
                # then we find the linear part is R (rotation matrix) and the
                # offset of the resulting affine is:
                #     [ ox*cos(theta) - oy*sin(theta) - cx*cos(theta) + cy*sin(theta) + cx ]
                #     [ ox*sin(theta) + oy*cos(theta) - cx*sin(theta) - cy*cos(theta) + cy ]
                # equal to Ro + (I-R)c
                # solving for rotation center as in TransformRotate.fromAffine2,
                # the resulting rotation center is (I-R)^-1 * R * o + c
                # we can use _invIminusR to multiply R*o by (I-R)^-1
                angleSin,angleCos = sincosDeg(self.angleDeg)
                # let (R*o = p = (px,py))
                ox,oy = other.offset
                px = angleCos*ox - angleSin*oy
                py = angleSin*ox + angleCos*oy
                invResult = _invIminusR(angleCos,angleSin,px,py,tol)
                if invResult is None: # angle close to zero, use translation only
                    return other
                else:
                    dx,dy = invResult
                    c = self.center if self.center is not None else Vec2()
                    qx,qy = dx + c.x, dy + c.y
                    if Vec2.areNearlyEqual((qx,qy),Vec2(),relTol=0.0,absTol=tol*scale):
                        return TransformRotate(self.angleDeg)
                    else:
                        return TransformRotate(self.angleDeg,qx,qy)
        else:
            return TransformMatrix(self.toAffine2().compose(other.toAffine2()))

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

    def __init__(self, sx: float = 1.0, sy: float|None = None):
        '''
        Initialize a scaling. If one arg is provided, the scale is applied
        equally in both axes. If both are provided, axis scales may differ.
        '''
        if not math.isfinite(sx):
            raise ValueError(f'x scale must be finite, not {sx!r}')
        if sy is not None and not math.isfinite(sy):
            raise ValueError(f'y scale must be finite, not {sy!r}')
        object.__setattr__(self,'sx',float(sx))
        object.__setattr__(self,'sy', None if sy is None else float(sy))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
        if self.sy is None:
            return f'scale({numFmt(self.sx)})'
        else:
            return f'scale({numFmt(self.sx)} {numFmt(self.sy)})'

    def toAffine2(self) -> Affine2:
        return Affine2.scale(self.sx,self.sy)

    @staticmethod
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformScale:
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale)
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),relTol=0.0,absTol=tol*scale):
            raise ValueError(f'Not a scale (origin is nonzero): {affine!r}')
        # make sure vectors are axis aligned, negative allowed, zero allowed
        if affine.xAxis.isZero():
            sx = 0.0 # zero x scale
        else:
            # nonzero x scale
            xDir = affine.xAxis.normalize()
            if Vec2.areNearlyEqual(xDir,Vec2(1.0,0.0),relTol=0.0,absTol=tol):
                sx = affine.xAxis.magnitude()
            elif Vec2.areNearlyEqual(xDir,Vec2(-1.0,0.0),relTol=0.0,absTol=tol):
                sx = -affine.xAxis.magnitude()
            else:
                raise ValueError(f'Not a scale (x vector is not axis aligned): {affine!r}')
        if affine.yAxis.isZero():
            sy = 0.0 # zero y scale
        else:
            # nonzero y scale
            yDir = affine.yAxis.normalize()
            if Vec2.areNearlyEqual(yDir,Vec2(0.0,1.0),relTol=0.0,absTol=tol):
                sy = affine.yAxis.magnitude()
            elif Vec2.areNearlyEqual(yDir,Vec2(0.0,-1.0),relTol=0.0,absTol=tol):
                sy = -affine.yAxis.magnitude()
            else:
                raise ValueError(f'Not a scale (y vector is not axis aligned): {affine!r}')
        if math.isclose(sx,sy,rel_tol=tol,abs_tol=0.0):
            return TransformScale(0.5*(sx+sy))
        else:
            return TransformScale(sx,sy)

    def inverse(self) -> TransformScale:
        if self.sx == 0.0:
            raise ZeroDivisionError('cannot invert zero x scale')
        if self.sy is not None and self.sy == 0.0:
            raise ZeroDivisionError('cannot invert zero y scale')
        return TransformScale(1.0/self.sx, None if self.sy is None else 1.0/self.sy)

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Tolerance is used to determine if the scale is close enough to uniform
        to use the same scale in both axes.

        Two TransformScale compose to another TransformScale.
        '''
        tol,scale = _checkTolAndScale(tol,scale) # scale unused
        if isinstance(other,TransformScale):
            osx = other.sx
            osy = other.sx if other.sy is None else other.sy
            # new scale multiplies the 2 together
            sx = self.sx * osx
            sy = (self.sx if self.sy is None else self.sy) * osy
            if math.isclose(sx,sy,rel_tol=tol,abs_tol=0.0):
                return TransformScale(0.5*(sx+sy))
            else:
                return TransformScale(sx,sy)
        else:
            return TransformMatrix(self.toAffine2().compose(other.toAffine2()))

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

    def __init__(self, angleDeg: float = 0.0):
        '''
        Initialize an X skew. The angle is in degrees.
        '''
        if not math.isfinite(angleDeg):
            raise ValueError(f'angle must be finite, not {angleDeg!r}')
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
        return f'skewX({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        t = math.tan(math.radians(self.angleDeg))
        if not math.isfinite(t):
            raise ValueError(f'skew angle tangent is not finite: {self.angleDeg!r}')
        return Affine2(yAxis=Vec2(t,1.0))

    @staticmethod
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformSkewX:
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale)
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),relTol=0.0,absTol=tol*scale):
            raise ValueError(f'Not a skewX (origin is nonzero): {affine!r}')
        if not Vec2.areNearlyEqual(affine.xAxis,Vec2(1.0,0.0),relTol=0.0,absTol=tol):
            raise ValueError(f'Not a skewX (xAxis is not (1,0)): {affine!r}')
        if not math.isclose(affine.yAxis.y,1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a skewX (yAxis.y is not 1): {affine!r}')
        angleRad = math.atan(affine.yAxis.x)
        return TransformSkewX(math.degrees(angleRad))

    def inverse(self) -> TransformSkewX:
        return TransformSkewX(-self.angleDeg)

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Two TransformSkewX compose to another TransformSkewX.
        '''
        tol,scale = _checkTolAndScale(tol,scale) # unused
        if isinstance(other,TransformSkewX):
            tanSum = (math.tan(math.radians(self.angleDeg))
                + math.tan(math.radians(other.angleDeg)))
            return TransformSkewX(math.degrees(math.atan(tanSum)))
        else:
            return TransformMatrix(self.toAffine2().compose(other.toAffine2()))

    def __repr__(self) -> str:
        return f'TransformSkewX({self.angleDeg!r})'

class TransformSkewY(TransformBase):
    '''
    Y axis skew transformation, for SVG.
    The angle is in degrees.
    '''
    angleDeg: float
    __slots__ = ('angleDeg',)

    def __init__(self, angleDeg: float = 0.0):
        '''
        Initialize a Y skew. The angle is in degrees.
        '''
        if not math.isfinite(angleDeg):
            raise ValueError(f'angle must be finite, not {angleDeg!r}')
        object.__setattr__(self,'angleDeg',float(angleDeg))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
        return f'skewY({numFmt(self.angleDeg)})'

    def toAffine2(self) -> Affine2:
        t = math.tan(math.radians(self.angleDeg))
        if not math.isfinite(t):
            raise ValueError(f'skew angle tangent is not finite: {self.angleDeg!r}')
        return Affine2(xAxis=Vec2(1.0,t))

    @staticmethod
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformSkewY:
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale)
        affine = Affine2(affine)
        if not Vec2.areNearlyEqual(affine.origin,Vec2(),relTol=0.0,absTol=tol*scale):
            raise ValueError(f'Not a skewY (origin is nonzero): {affine!r}')
        if not Vec2.areNearlyEqual(affine.yAxis,Vec2(0.0,1.0),relTol=0.0,absTol=tol):
            raise ValueError(f'Not a skewY (yAxis is not (0,1)): {affine!r}')
        if not math.isclose(affine.xAxis.x,1.0,rel_tol=0.0,abs_tol=tol):
            raise ValueError(f'Not a skewY (xAxis.x is not 1): {affine!r}')
        angleRad = math.atan(affine.xAxis.y)
        return TransformSkewY(math.degrees(angleRad))

    def inverse(self) -> TransformSkewY:
        return TransformSkewY(-self.angleDeg)

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        '''
        Two TransformSkewY compose to another TransformSkewY.
        '''
        tol,scale = _checkTolAndScale(tol,scale) # unused
        if isinstance(other,TransformSkewY):
            tanSum = (math.tan(math.radians(self.angleDeg))
                + math.tan(math.radians(other.angleDeg)))
            return TransformSkewY(math.degrees(math.atan(tanSum)))
        else:
            return TransformMatrix(self.toAffine2().compose(other.toAffine2()))

    def __repr__(self) -> str:
        return f'TransformSkewY({self.angleDeg!r})'

class TransformMatrix(TransformBase):
    '''
    General affine transformation, for SVG.
    '''
    affine: Affine2
    __slots__ = ('affine',)

    def __init__(self, affine: Affine2LikeType = Affine2()):
        '''
        Initialize a matrix transformation from an affine transformation.
        '''
        _checkAffine(affine)
        object.__setattr__(self,'affine',Affine2(affine))

    @staticmethod
    def fromVectors(xAxis: Vec2LikeType, yAxis: Vec2LikeType, origin: Vec2LikeType) \
            -> TransformMatrix:
        '''
        Construct a TransformMatrix with the 3 vectors as in the Affine2 constructor.
        '''
        return TransformMatrix(Affine2(xAxis,yAxis,origin))

    @staticmethod
    def fromParams(a: float, b: float, c: float, d: float, e: float, f: float) -> TransformMatrix:
        '''
        Construct a TransformMatrix using the 6 parameters in the SVG order.
        '''
        return TransformMatrix(Affine2(Vec2(a,b),Vec2(c,d),Vec2(e,f)))

    def toSvgString(self, *, numFmt: _NumFmtT = _DEFAULT_NUM_FMT) -> str:
        a,b = self.affine.xAxis
        c,d = self.affine.yAxis
        e,f = self.affine.origin
        return (f'matrix({numFmt(a)} {numFmt(b)} {numFmt(c)} {numFmt(d)} {numFmt(e)} {numFmt(f)})')

    def toAffine2(self) -> Affine2:
        return self.affine

    @staticmethod
    def fromAffine2(affine: Affine2LikeType, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformMatrix:
        '''
        Since TransformMatrix can handle any affine transformation, this does
        not raise an exception unlike the other transformations.
        '''
        _checkAffine(affine)
        tol,scale = _checkTolAndScale(tol,scale) # although they are not used
        return TransformMatrix(affine)

    def inverse(self) -> TransformMatrix:
        return TransformMatrix(self.affine.inverse())

    def compose(self, other: TransformBase, *,
            tol: float = 1e-9, scale: float = 1.0) -> TransformBase:
        tol,scale = _checkTolAndScale(tol,scale) # unused
        return TransformMatrix(self.affine.compose(other.toAffine2()))

    def __repr__(self) -> str:
        return f'TransformMatrix({self.affine!r})'
