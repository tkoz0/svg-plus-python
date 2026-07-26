import os
import sys
sys.path.insert(0,'..')
from svgpp import *
from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, comb, \
    copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, expm1, fabs, \
    factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, \
    isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, \
    log2, modf, nan, nextafter, perm, pi, pow, prod, radians, remainder, \
    sin, sinh, sqrt, tan, tanh, tau, trunc, ulp
from datetime import datetime
from copy import deepcopy
SVG_STRS: list[str] = []
FILE_DATE = os.path.basename(__file__).replace('.py','')
setwhitespace(4)
setprefix(f'{FILE_DATE}_')

################################################################################
# edit here to create svg images and append strings to SVG_STRS

image = svgimage((-5,-5),(5,5),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.06em')

C = vec(0,0)
r = 4
X = C+vec.polard(r,180)
x1 = vec(5,-1).normalize()
x2 = x1.rotated(24)

def circle_intersect(P,Q):
    # try to find the point on a line that intersects our circle
    # this is janky, but P,Q must contain the point and we bisect
    assert abs(P-C) < r
    assert abs(Q-C) > r
    tmin = 0
    tmax = 1
    while True:
        tmid = (tmin+tmax)/2
        if tmid == tmax or tmid == tmin:
            break
        rtmp = abs(vec.lerp(P,Q,tmid)-C)
        if rtmp < r:
            tmin = tmid
        else:
            tmax = tmid
    print(tmid)
    return vec.lerp(P,Q,tmid)

Y1 = circle_intersect(X+r*x1,X+3*r*x1)
Y2 = circle_intersect(X+r*x2,X+3*r*x2)
z = (-x2).rotated(84)
Z = circle_intersect(Y2+0.5*z,Y2+r*z)

# Y1->Z needs to intersect X->Y2
def matinv(a,b,c,d):
    det = 1/(a*d-b*c)
    return tuple(det*x for x in (d,-b,-c,a))
def matmul(a,b,c,d,x,y):
    return (a*x+b*y,c*x+d*y)
def line_intersect(P,u,Q,v):
    # P+a*u = Q+b*v (scalars a,b)
    A = (u[0],-v[0],u[1],-v[1])
    Ainv = matinv(*A)
    PQ = Q-P
    a,b = matmul(*Ainv,*PQ)
    PP = P+a*u
    QQ = Q+b*v
    assert (PP-QQ).magsq() < 1e-20
    return vec.midpoint(PP,QQ)
W = line_intersect(Y1,Z-Y1,X,Y2-X)

assert abs(vec.angled(Z-W,X-W) - 60) < 1e-10
assert abs(vec.angled(X-Y2,Z-Y2) - 84) < 1e-10

# vectors for the angle
g1 = (X-W).normalize()*0.75
g2 = (Y1-W).normalize()*0.75
h1 = (X-Y2).normalize()
h2 = (Z-Y2).normalize()

image += group([
    circle(r,C),
    path(pathseq().M(X).l(x1*3).A(X+x2*3,3,3,sweep=True).Z(),
        attrs(stroke='#49b',fill='#7cf')),
    line(X,Y1),
    #line(X,Y2),
    line(Y2,Z),
    line(X,W),
    line(Y1,W),
    group([
        circle(0.15,X),
        circle(0.15,Y1),
        circle(0.15,Z)
    ],attrs(fill='black')),
    path(pathseq().M(W+g1).A(W+g2,0.75,0.75,sweep=True)),
    path(pathseq().M(Y2+h1).A(Y2+h2,1,1,sweep=True)),
    line(vec.lerp(vec.midpoint(W+g2,W+g1),W,1/3),C+(4,3))
],style_line1)

image += group([
    text('x&deg;',C+(-0.8,0.4)),
    text('84&deg;',C+(2,0.5)),
    text('60&deg;',C+(3.4,3.8))
],style_font1)

SVG_STRS.append(str(image))

################################################################################
# write html file

out = open(f'{FILE_DATE}.html','w')
header = f'''\
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        body {{ background: black; }}
        svg {{ background: white; }}
    </style>
</head>
<body>
<p style="color:white;">{str(datetime.now())}</p>
'''
out.write(header)

for s in SVG_STRS:
    out.write(f'<hr />\n{s}\n')

footer = f'''\
</body>
</html>
'''

out.write(footer)
out.close()
