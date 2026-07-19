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

image = svgimage((0,0),(10,14),200,280)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.07em')

A = vec(9,13)
B = A+(-8,0)
C = A+(0,-6)
a = atan(4.5/6)
D = C+vec.polarr(7.5,-pi/2-a)
E = C+(0,-6)
s = 1.5
u = vec.polarr(1,-pi/2-a)
uu = u.rotated(-90)

linegroup = group([
    line(B,C,attrs=attrs(stroke='#7cf')),
    polyline([B,A,C]),
    polyline([C,D,B]),
    polyline([C,E,D]),
    circle(0.2,A,attrs=attrs(fill='black')),
    polyline([A+(0,-s),A+(-s,-s),A+(-s,0)]),
    polyline([E+(-s,0),E+(-s,s),E+(0,s)]),
    polyline([C+s*u,C+s*u+s*uu,C+s*uu,C])
],style_line1)
image += linegroup

image += group([
    text('4.5',5.5,2),
    text('6',8.2,4.5),
    text('8',4,12.7),
    text('x',4,10,attrs(fill='#7cf'))
],style_font1)

SVG_STRS.append(str(image))

u1 = vec.polarr(1,0)
v1 = vec.polarr(1,atan(6/4.5))
u2 = vec.polarr(1,pi/2)
v2 = vec.polarr(1,pi/2+atan(8/6))
u3 = vec.polarr(1,0)
v3 = vec.polarr(1,-atan(6/8))
u4 = vec.polarr(1,-pi/2)
v4 = vec.polarr(1,-pi/2-atan(4.5/6))
linegroup += group([
    path(pathseq().M(D+u1).A(D+v1,1,1,sweep=True)),
    path(pathseq().M(C+u2).A(C+v2,1,1,sweep=True)),
    path(pathseq().M(B+u3).A(B+v3,1,1)),
    path(pathseq().M(B+1.25*u3).A(B+1.25*v3,1,1)),
    path(pathseq().M(C+u4).A(C+v4,1,1)),
    path(pathseq().M(C+1.25*u4).A(C+1.25*v4,1,1))
],attrs(stroke='red'))

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
