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

image = svgimage((0,0),(8,8),200,200)
style_line1 = attrs(stroke='black',stroke_width=0.1,fill='none')
style_font1 = attrs(fill='black',font_size='0.1em')

A = vec(0.5,1)
B = A+(6,0)
C = A+(6,6)
D = A+(0,6)
E = A+(4,4)
F = vec.midpoint(C,D)

def tick1(P,Q):
    M = vec.midpoint(P,Q)
    u = (P-Q).normalize().rotated(90)*0.3
    return line(M+u,M-u)
def tick2(P,Q):
    M1 = vec.lerp(P,Q,0.45)
    M2 = vec.lerp(P,Q,0.55)
    u = (P-Q).normalize().rotated(90)*0.3
    return (line(M1-u,M1+u),line(M2-u,M2+u))

image += group([
    polygon([A,B,E],attrs(fill='#7cf')),
    polygon([A,B,C,D]),
    line(A,C),
    line(B,F),
    tick1(A,B),
    tick1(B,C),
    tick1(A,D),
    *tick2(C,F),
    *tick2(F,D)
],style_line1)

image += group([
    text('x',A+(3,2)),
    text('6',A+(6.5,3.5))
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
