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

image = svgimage((0,0),(5,5),250,250)
style_line1 = attrs(stroke='black',stroke_width=0.05,fill='none')
style_font1 = attrs(fill='black',font_size='0.04em')

A = vec(0.5,0.3)
B = A+(4,0)
C = A+(4,4)
D = A+(0,4)

image += polygon([B,vec.midpoint(A,B),vec.midpoint(vec.midpoint(A,B),
    vec.midpoint(A,D)),vec.midpoint(A,C)],attrs(stroke='none',fill='#7cf'))

def tick1(A,B):
    u = (B-A).normalize().rotated(90)*0.2
    M = vec.midpoint(A,B)
    return line(M-u,M+u)
def tick2(A,B):
    u = (B-A).normalize().rotated(90)*0.2
    M1 = vec.lerp(A,B,0.48)
    M2 = vec.lerp(A,B,0.52)
    return (line(M1-u,M1+u),line(M2-u,M2+u))

image += group([
    rect(A,C),
    rect(C-(0.4,0.4),C),
    line(A,C),
    line(B,D),
    line(vec.midpoint(A,B),vec.midpoint(A,D)),
    tick1(A,vec.midpoint(A,B)),
    tick1(vec.midpoint(A,B),B),
    *tick2(B,C),
    *tick2(C,D)
],style_line1)

image += group([
    text('x',A+(2,1.2)),
    text('4',A+(1.4,4.6))
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
