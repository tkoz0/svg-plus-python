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

image = svgimage((0,0),(16,24),250,300)
style_line1 = attrs(stroke='black',stroke_width=0.2,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

A = vec(15,20)
s1 = 8*sqrt(3)
s2 = 4*sqrt(15)
s3 = 10*sqrt(3)
s4 = 5*sqrt(15)
t = atan(1/2)
rl = 1 # right angle length
ru1 = vec(0,-rl).rotater(t)
rv1 = ru1.rotated(90)
ru2 = vec(0,-rl).rotater(2*t)
rv2 = ru2.rotated(90)
M = A+(-s1,-s1/2)
N = M+vec(0,-s2/2).rotater(t)
T = N+vec(0,-s3/2).rotater(2*t)

def tick(P1,P2,*ts):
    result = []
    u = (P2-P1).normalize().rotated(90)*0.5
    for t in ts:
        M = vec.lerp(P1,P2,t)
        result.append(line(M-u,M+u))
    return result

def angle(P,Q,R):
    u = (P-Q).normalize()
    v = (R-Q).normalize()
    w = (vec.midpoint(Q+u,Q+v)-Q).normalize()
    return path(pathseq().M(Q+3*v).A(Q+3*u,3,3).M(Q+2.5*w).l(1*w))

image += group([
    polygon([A,T,A+(0,-s1)],attrs(fill='#7cf')),
    rect(A,A+(-s1,-s1)),
    polygon([A,M,N]),
    line(N,T),
    # right angles
    rect(A+(-s1,0),A+(-s1+rl,-rl)),
    rect(A+(-s1,-s1),A+(-s1+rl,-s1+rl)),
    rect(A+(0,-s1),A+(-rl,-s1+rl)),
    polyline([M+ru1,M+ru1+rv1,M+rv1]),
    polyline([N+ru2,N+ru2+rv2,N+rv2]),
    # line ticks
    *tick(M,A+(-s1,-s1),0.5),
    *tick(M,A+(-s1,0),0.5),
    *tick(A,A+(0,-s1),0.48,0.52),
    *tick(A,A+(-s1,0),0.48,0.52),
    # angles
    angle(M,A,N),
    angle(N,A,T)
],style_line1)

image += group([
    text('8&radic;3',A+(-12,2)),
    text('x',A+(-1.5,-11))
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
