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

image = svgimage((0,0),(25,20),250,200)
style_line1 = attrs(stroke='black',stroke_width=0.25,fill='none')
style_font1 = attrs(fill='black',font_size='0.15em')

A = vec(5,16)
B = A+(0,-12)
C = A+(16,0)
D = B+(12.5,0)

def eqtick(p,q):
    m = vec.midpoint(p,q)
    u = (p-q).normalize().rotated(90)
    return line(m-u,m+u)

image += group([
    polygon([A,B,C]),
    polygon([B,C,D],attrs(fill='#7cf')),
    rect(A,A+(2,-2)),
    rect(B,B+(2,2)),
    eqtick(B,D),
    eqtick(C,D)
],style_line1)

image += group([
    text('12',2,11),
    text('16',11,18),
    text('25x',12,8)
],style_font1)

SVG_STRS.append(str(image))

# mark theta
theta = atan(3/4)
u = vec.polarr(1,theta)
r = 3
v = (C-B).normalize()
vv = v.rotated(-90)
E = vec.midpoint(B,C)
image += group([
    path(pathseq().M(B+(r,0)).A(B+r*u,r,r,sweep=True)),
    path(pathseq().M(C+(-r,0)).A(C-r*u,r,r,sweep=True)),
    line(D,E),
    polyline([E+v,E+v+vv,E+vv])
],style_line1.stroke('red'))
image += group([
    text('&theta;',8.5,6.5),
    text('&theta;',16,15.5),
    text('A',A+(-2,2)),
    text('B',B+(-2,0)),
    text('C',C+(0,2)),
    text('D',D),
    text('E',E+(-2,2))
],style_font1.fill('red'))

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
