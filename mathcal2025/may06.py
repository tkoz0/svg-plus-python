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

image = svgimage((0,0),(10,10),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.05em')

def linetick(C,a):
    return line(C+vec.polarr(0.75,a),C+vec.polarr(1.25,a))
def linetick2(C,a):
    return (linetick(C,a-0.15),linetick(C,a+0.15))

v1 = vec(3,-5)
v2 = vec(5,0)
u1 = v1.normalize()
u2 = v2.normalize()
t1 = vec.angler(v1,v2)
t2 = pi - t1
A = vec(1,8)
B = A + v1
C = B + v2
D = C - v1
image += group([
    polygon([A,B,C,D]),
    path(pathseq().M(A+u2).A(A+u1,1,1)),
    path(pathseq().M(B-u1).A(B+u2,1,1)),
    path(pathseq().M(C-u2).A(C-u1,1,1)),
    path(pathseq().M(D+u1).A(D-u2,1,1)),
    linetick(A,-t1/2),
    linetick(C,pi-t1/2),
    *linetick2(B,t2/2),
    *linetick2(D,pi+t2/2)
],style_line1)

image += group([
    text('1000z&deg;',B+(-1.5,-0.5)),
    text('(5y+45)&deg;',C+(-2.5,-0.5)),
    text('10x&deg;',A+(0,1)),
    text('(25x-30)&deg;',D+(-1,1))
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
